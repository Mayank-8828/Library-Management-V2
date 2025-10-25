# Copyright (c) 2025, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, getdate, date_diff, add_days

class Loan(Document):
    def validate(self):
        """Validate loan data"""
        self.validate_dates()
        self.validate_member()
        self.validate_book_availability()
        self.calculate_fine()

    def validate_dates(self):
        """Validate loan dates"""
        if self.issue_date and self.due_date:
            if getdate(self.issue_date) > getdate(self.due_date):
                frappe.throw(_("Issue Date cannot be after Due Date"))

        # Set default due date (14 days from issue date)
        if self.issue_date and not self.due_date:
            self.due_date = add_days(self.issue_date, 14)

        if self.return_date:
            if getdate(self.return_date) < getdate(self.issue_date):
                frappe.throw(_("Return Date cannot be before Issue Date"))

    def validate_member(self):
        """Validate member can borrow books"""
        if self.is_new():
            member = frappe.get_doc("Member", self.member)
            if not member.can_borrow_books():
                frappe.throw(_("Member {0} cannot borrow more books. Check membership status or loan limit.").format(member.full_name))

    def validate_book_availability(self):
        """Check if book is available for loan"""
        if self.is_new():
            book = frappe.get_doc("Book", self.book)
            if book.available_copies <= 0:
                frappe.throw(_("Book {0} is not available for loan").format(book.title))

    def calculate_fine(self):
        """Calculate fine for overdue books"""
        if self.status == "Returned" and self.return_date and self.due_date:
            days_overdue = date_diff(self.return_date, self.due_date)
            if days_overdue > 0:
                # $0.50 per day fine
                self.fine_amount = days_overdue * 0.50

        # Check if currently overdue
        if self.status == "Issued" and self.due_date:
            if getdate(self.due_date) < getdate(today()):
                self.status = "Overdue"
                days_overdue = date_diff(today(), self.due_date)
                self.fine_amount = days_overdue * 0.50

    def on_submit(self):
        """Update book availability when loan is issued"""
        book = frappe.get_doc("Book", self.book)
        book.update_availability(-1)
        frappe.msgprint(_("Book {0} issued to {1}").format(book.title, self.member_name))

    def on_cancel(self):
        """Restore book availability when loan is cancelled"""
        if self.status != "Returned":
            book = frappe.get_doc("Book", self.book)
            book.update_availability(1)

    @frappe.whitelist()
    def return_book(self):
        """Mark book as returned"""
        if self.status == "Returned":
            frappe.throw(_("Book is already returned"))

        if self.docstatus != 1:
            frappe.throw(_("Loan must be submitted before returning"))

        self.status = "Returned"
        self.return_date = today()
        self.calculate_fine()
        self.save()

        # Update book availability
        book = frappe.get_doc("Book", self.book)
        book.update_availability(1)

        frappe.msgprint(_("Book returned successfully. Fine: {0}").format(self.fine_amount or 0))

        return self

# Hook functions called from hooks.py
def validate_loan_dates(doc, method):
    """Additional validation hook"""
    pass

def on_loan_submit(doc, method):
    """Hook called on loan submission"""
    # You can add additional logic here like sending notifications
    pass

def on_loan_cancel(doc, method):
    """Hook called on loan cancellation"""
    # You can add additional logic here
    pass
