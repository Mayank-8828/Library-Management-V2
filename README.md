# Library Management System

A complete Library Management System built on Frappe Framework v15+.

## Features

- Book Management (cataloging, tracking, searching)
- Member Management (registration, membership tracking)
- Loan Management (issue, return, due date tracking)
- Automated notifications for due dates
- Web portal for members to view their loans
- Librarian dashboard for managing library operations
- Role-based permissions (Librarian, Library Member)

## Installation

### Step 1: Get the app from GitHub

```bash
bench get-app https://github.com/yourusername/library_management.git
```

Or if you have a local copy:
```bash
cd ~/frappe-bench/apps
cp -r /path/to/library_management .
```

### Step 2: Install the app on your site

```bash
bench --site your-site-name install-app library_management
```

### Step 3: Run migrations (if needed)

```bash
bench --site your-site-name migrate
```

## Usage

### For Librarians

1. Navigate to Library Management workspace
2. Add Books to the system
3. Register Members
4. Issue books to members (creates Loan records)
5. Process returns when books come back

### For Members

1. Login to the portal
2. View your active loans at `/library/my-loans`
3. See loan history and due dates

## Roles & Permissions

- **Librarian**: Full access to create, edit, and delete Books, Members, and Loans
- **Library Member**: Can view their own loan records via web portal

## Configuration

Default permissions and roles are created automatically during installation.

## License

MIT
