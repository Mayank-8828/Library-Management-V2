import frappe
from frappe import _

def get_context(context):
    """Get context for library member portal"""
    context.no_cache = 1

    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to view your loans"), frappe.PermissionError)

    # Get member linked to current user
    member = frappe.db.get_value("Member", {"user": frappe.session.user}, "name")

    if not member:
        context.show_sidebar = False
        context.error_message = "You are not registered as a library member"
        return context

    # Get member details
    member_doc = frappe.get_doc("Member", member)
    context.member = member_doc

    # Get active loans
    active_loans = frappe.get_all("Loan",
        filters={
            "member": member,
            "docstatus": 1,
            "status": ["in", ["Issued", "Overdue"]]
        },
        fields=["name", "book", "book_title", "issue_date", "due_date", "status", "fine_amount"],
        order_by="issue_date desc"
    )

    # Get loan history
    loan_history = frappe.get_all("Loan",
        filters={
            "member": member,
            "docstatus": 1,
            "status": "Returned"
        },
        fields=["name", "book", "book_title", "issue_date", "due_date", "return_date", "fine_amount", "fine_paid"],
        order_by="return_date desc",
        limit=10
    )

    context.active_loans = active_loans
    context.loan_history = loan_history
    context.total_active = len(active_loans)
    context.can_borrow_more = member_doc.can_borrow_books()

    return context
