frappe.ui.form.on('Loan', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === 'Issued') {
            frm.add_custom_button(__('Return Book'), function() {
                frm.call({
                    method: 'return_book',
                    doc: frm.doc,
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});
