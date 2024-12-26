# Copyright (c) 2024, eactive and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	employee = filters.get("employee")
	is_processed = filters.get("is_processed")

	if is_processed:
		if is_processed == "Yes":
			is_processed = "Y"
		if is_processed == "No":
			is_processed = "N"
		if is_processed == "Error":
			is_processed = "E"

	columns = [
		{
			"fieldtype": "Link",
			"options": "Employee",
			"fieldname": "employee_id",
			"label": "Employee Id"
		},
		{
			"fieldtype": "Date",
			"fieldname": "punch_date",
			"label": "Punch Date"
		},
		{
			"fieldtype": "Data",
			"fieldname": "punch_time",
			"label": "Punch Time"
		},
		{
			"fieldtype": "Data",
			"fieldname": "area",
			"label": "Area"
		},
		{
			"fieldtype": "Data",
			"fieldname": "terminal_id",
			"label": "Machine Id"
		},
		{
			"fieldtype": "Data",
			"fieldname": "punch_direction",
			"label": "Punch Direction"
		},
		{
			"fieldtype": "Data",
			"fieldname": "is_processed",
			"label": "Is Processed"
		},
		{
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"fieldname": "message",
			"label": "Message"
		}
		
	]

	conditions = ""
	employee_cond = ""
	is_processed_cond = ""

	if employee:
		employee_cond = f" AND employee_id = '{employee}'"

	if is_processed:
		is_processed_cond = f" AND is_processed = '{is_processed}'"

	conditions = f"{conditions} {employee_cond} {is_processed_cond}"

	sql = f"""
		SELECT
			name,
			employee_id,
			punch_time,
			punch_date,
			area,
			terminal_id,
			punch_direction,
			is_processed,
			message
		FROM
			bio_attendance_log
		WHERE
			punch_date_time between '{from_date} 00:00:00' and '{to_date} 59:59:59' {conditions}
		"""

	result = frappe.db.sql(sql, as_dict=True)

	return columns, result
