# Copyright (c) 2025, Your Name and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestBook(FrappeTestCase):
    def test_book_creation(self):
        """Test basic book creation"""
        book = frappe.get_doc({
            "doctype": "Book",
            "isbn": "978-0-123456-78-9",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
        })
        book.insert()

        self.assertEqual(book.available_copies, 5)
        self.assertEqual(book.status, "Available")

        # Cleanup
        book.delete()
