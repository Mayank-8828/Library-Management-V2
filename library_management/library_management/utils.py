import frappe
from frappe import _
from frappe.utils import today, getdate

def get_overdue_loans():
    """Get all overdue loans"""
    overdue_loans = frappe.get_all("Loan",
        filters={
            "docstatus": 1,
            "status": "Issued",
            "due_date": ["<", today()]
        },
        fields=["name", "member", "member_name", "book", "book_title", "due_date"]
    )

    return overdue_loans

def update_overdue_status():
    """Update status of overdue loans - can be called from scheduler"""
    overdue_loans = get_overdue_loans()

    for loan_data in overdue_loans:
        loan = frappe.get_doc("Loan", loan_data.name)
        loan.status = "Overdue"
        loan.calculate_fine()
        loan.save()
        frappe.db.commit()

    return len(overdue_loans)

def send_due_date_reminders():
    """Send reminders for books due soon - can be scheduled"""
    from frappe.utils import add_days

    # Get loans due in 2 days
    upcoming_due = frappe.get_all("Loan",
        filters={
            "docstatus": 1,
            "status": "Issued",
            "due_date": add_days(today(), 2)
        },
        fields=["name", "member", "member_name", "book_title", "due_date"]
    )

    for loan in upcoming_due:
        member = frappe.get_doc("Member", loan.member)
        if member.email:
            # Send reminder email
            frappe.sendmail(
                recipients=[member.email],
                subject=f"Book Due Reminder: {loan.book_title}",
                message=f"""Dear {loan.member_name},

                This is a reminder that the book "{loan.book_title}" is due on {frappe.utils.formatdate(loan.due_date)}.

                Please return it on time to avoid late fees.

                Thank you,
                Library Management System
                """
            )

    return len(upcoming_due)
