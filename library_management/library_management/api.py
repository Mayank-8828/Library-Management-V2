import frappe
from frappe import _

@frappe.whitelist()
def get_member_loans(member_id=None):
    """Get loans for a specific member"""
    if not member_id:
        # Get member linked to current user
        member_id = frappe.db.get_value("Member", {"user": frappe.session.user}, "name")

        if not member_id:
            frappe.throw(_("No member found for current user"))

    loans = frappe.get_all("Loan",
        filters={
            "member": member_id,
            "docstatus": 1
        },
        fields=["name", "book", "book_title", "issue_date", "due_date", "return_date", "status", "fine_amount"],
        order_by="issue_date desc"
    )

    return loans

@frappe.whitelist()
def search_books(query):
    """Search books by title, author, or ISBN"""
    books = frappe.get_all("Book",
        filters={
            "status": "Available"
        },
        or_filters=[
            ["title", "like", f"%{query}%"],
            ["author", "like", f"%{query}%"],
            ["isbn", "like", f"%{query}%"]
        ],
        fields=["name", "isbn", "title", "author", "category", "available_copies"],
        limit=20
    )

    return books

@frappe.whitelist()
def get_book_details(book_id):
    """Get detailed information about a book"""
    book = frappe.get_doc("Book", book_id)

    return {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "publication_year": book.publication_year,
        "category": book.category,
        "language": book.language,
        "pages": book.pages,
        "description": book.description,
        "status": book.status,
        "available_copies": book.available_copies,
        "total_copies": book.total_copies
    }
