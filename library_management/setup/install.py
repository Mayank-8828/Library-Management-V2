import frappe
from frappe import _

def after_install():
    """Called after app installation"""
    create_roles()
    setup_permissions()
    frappe.db.commit()
    print("Library Management app installed successfully!")

def create_roles():
    """Create custom roles if they don't exist"""
    roles = [
        {
            "role_name": "Librarian",
            "desk_access": 1,
        },
        {
            "role_name": "Library Member",
            "desk_access": 0,
        }
    ]

    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "desk_access": role_data["desk_access"]
            })
            role.insert(ignore_permissions=True)
            print(f"Created role: {role_data['role_name']}")

def setup_permissions():
    """Setup default permissions for Library Management doctypes"""

    # Book permissions
    add_permission("Book", "Librarian", 0, {
        "read": 1, "write": 1, "create": 1, "delete": 1,
        "submit": 0, "cancel": 0, "amend": 0,
        "print": 1, "email": 1, "report": 1, "export": 1
    })

    add_permission("Book", "Library Member", 0, {
        "read": 1, "write": 0, "create": 0, "delete": 0
    })

    # Member permissions
    add_permission("Member", "Librarian", 0, {
        "read": 1, "write": 1, "create": 1, "delete": 1,
        "submit": 0, "cancel": 0, "amend": 0,
        "print": 1, "email": 1, "report": 1, "export": 1
    })

    add_permission("Member", "Library Member", 0, {
        "read": 1, "write": 0, "create": 0, "delete": 0,
        "if_owner": 1
    })

    # Loan permissions (submittable doctype)
    add_permission("Loan", "Librarian", 0, {
        "read": 1, "write": 1, "create": 1, "delete": 1,
        "submit": 1, "cancel": 1, "amend": 1,
        "print": 1, "email": 1, "report": 1, "export": 1
    })

    add_permission("Loan", "Library Member", 0, {
        "read": 1, "write": 0, "create": 0, "delete": 0,
        "if_owner": 1
    })

    print("Permissions setup completed")

def add_permission(doctype, role, level, perms):
    """Helper to add permission if it doesn't exist"""
    if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": role, "permlevel": level}):
        perm = frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": doctype,
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": role,
            "permlevel": level,
            **perms
        })
        perm.insert(ignore_permissions=True)
