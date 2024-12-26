import frappe

def after_install():
    create_custom_fields()

def create_custom_fields():
    frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "Employee Checkin",
        "label": "Bio Log ID",
        "fieldname": "bio_log_id",
        "fieldtype": "Data",
        "read_only": 1,
        "hidden": 1
    }).save()