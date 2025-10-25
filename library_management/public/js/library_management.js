// Library Management Custom Scripts

frappe.provide("library_management");

library_management.search_books = function(query) {
    return frappe.call({
        method: "library_management.library_management.api.search_books",
        args: { query: query }
    });
};

library_management.get_book_details = function(book_id) {
    return frappe.call({
        method: "library_management.library_management.api.get_book_details",
        args: { book_id: book_id }
    });
};
