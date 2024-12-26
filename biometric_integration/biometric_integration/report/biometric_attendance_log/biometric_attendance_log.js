// Copyright (c) 2024, eactive and contributors
// For license information, please see license.txt

frappe.query_reports["Biometric Attendance Log"] = {
    
    get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
	
	onload: function(report) {
	    report.page.add_action_item("Reset Log", function() {
			let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => {
			    frappe.call("biometric_integration.biometric_integration.attendance.reset_attendance_log", {
			        "bio_id": report.data[i].name
			    })
			});
		});
		
    },
	
    "filters": [
        {
            "fieldname": "from_date",
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
            "reqd": 1,
            "label": "From Date"
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1,
            "label": "To Date"
        },
        {
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "label": "Employee"
        },
        {
            "fieldname": "is_processed",
            "fieldtype": "Select",
            "options": "\nYes\n\No\nError",
            "label": "Is Processed"
        }
    ]
};