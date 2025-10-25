# Copyright (c) 2025, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, add_years

class Member(Document):
    def validate(self):
        """Validate member data"""
        self.set_full_name()
        self.validate_dates()
        self.validate_email()

    def set_full_name(self):
        """Set full name from first and last name"""
        if self.first_name:
            self.full_name = self.first_name
            if self.last_name:
                self.full_name += " " + self.last_name

    def validate_dates(self):
        """Validate membership dates"""
        if self.membership_start_date and self.membership_end_date:
            if self.membership_start_date > self.membership_end_date:
                frappe.throw(_("Membership Start Date cannot be after End Date"))

        # Set default end date if not provided
        if self.membership_start_date and not self.membership_end_date:
            self.membership_end_date = add_years(self.membership_start_date, 1)

    def validate_email(self):
        """Validate email is unique"""
        if self.email:
            # Check for duplicate email
            existing = frappe.db.exists("Member", {
                "email": self.email,
                "name": ["!=", self.name]
            })
            if existing:
                frappe.throw(_("Member with this email already exists"))

    def after_insert(self):
        """Create user if email is provided"""
        if self.email and not self.user:
            self.create_portal_user()

    def create_portal_user(self):
        """Create a portal user for this member"""
        if frappe.db.exists("User", self.email):
            # Link existing user
            self.user = self.email
            self.save()
            return

        try:
            user = frappe.get_doc({
                "doctype": "User",
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name or "",
                "enabled": 1,
                "send_welcome_email": 1,
                "user_type": "Website User"
            })
            user.insert(ignore_permissions=True)

            # Add Library Member role
            user.add_roles("Library Member")

            # Link user to member
            self.user = user.name
            self.save()

            frappe.msgprint(_("Portal user created for {0}").format(self.full_name))
        except Exception as e:
            frappe.log_error(f"Failed to create user for member {self.name}: {str(e)}")

    def get_active_loans_count(self):
        """Get count of active loans for this member"""
        return frappe.db.count("Loan", {
            "member": self.name,
            "docstatus": 1,
            "status": "Issued"
        })

    def can_borrow_books(self):
        """Check if member can borrow more books"""
        if not self.is_active:
            return False

        if self.membership_end_date < today():
            return False

        active_loans = self.get_active_loans_count()
        return active_loans < self.max_books_allowed
