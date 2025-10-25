# Copyright (c) 2025, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Book(Document):
    def validate(self):
        """Validate book data"""
        self.validate_copies()
        self.validate_isbn()

    def validate_copies(self):
        """Ensure available copies doesn't exceed total copies"""
        if not self.is_new():
            if self.available_copies > self.total_copies:
                frappe.throw("Available copies cannot exceed total copies")
        else:
            # For new books, set available copies equal to total copies
            self.available_copies = self.total_copies

    def validate_isbn(self):
        """Basic ISBN validation"""
        if self.isbn:
            # Remove any hyphens or spaces
            isbn_clean = self.isbn.replace("-", "").replace(" ", "")
            if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
                frappe.msgprint("ISBN should be 10 or 13 digits. Please verify.", 
                              indicator="orange", alert=True)

    def update_availability(self, delta):
        """Update available copies count
        Args:
            delta: positive number to increase, negative to decrease
        """
        self.available_copies = self.available_copies + delta

        if self.available_copies < 0:
            frappe.throw("Cannot have negative available copies")

        # Update status based on availability
        if self.available_copies == 0:
            self.status = "Issued"
        elif self.available_copies > 0:
            self.status = "Available"

        self.save()
