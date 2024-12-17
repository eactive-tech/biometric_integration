import frappe

def process_attendance_log():

	attendance_logs = frappe.db.sql(
		"""
		SELECT 
			*
		FROM
			bio_attendance_log
		WHERE 
			(is_processed in ('N', '', Null) or is_processed is Null)
			AND LENGTH(employee_id) > 3
		ORDER by
			employee_id, punch_date, punch_time
		LIMIT 1000
	""", as_dict=True)
	frappe.log_error("attendance_logs", attendance_logs)
	for log in attendance_logs:

		try:

			if not frappe.db.exists("Employee", log.employee_id):
				sql = f"UPDATE bio_attendance_log set is_processed = 'E', message = 'Employee ID Does not exists' where name = '{log.name}'"
				frappe.db.sql(sql)
			else:
				log_type = ""
				time = f"{log.punch_date} {log.punch_time}"
				
				# if log.punch_direction == "I":
				# 	log_type = "IN" 

				allowed_shifts = []
				# check shift from employee master

				shift = frappe.db.get_value("Employee", log.employee_id, "default_shift")
				allowed_shifts.append(shift)

				## check shift from shift assignment 

				shift_assignments = frappe.db.sql("""
					SELECT 
						*
					FROM `tabShift Assignment`
					WHERE employee = %s
					and %s between start_date and end_date
					and docstatus=1
					ORDER BY start_date desc limit 1
				""", (log.employee_id, log.punch_date), as_dict=True)

				if shift_assignments:
					shift = shift_assignments[0].shift_type
					allowed_shifts.append(shift)

				checkin = frappe.get_doc({
					"doctype": "Employee Checkin",
					"employee": log.employee_id,
					"log_type": log_type,
					"time": time,
					"device_id": log.terminal_id,
					"custom_area": log.area,
					"shift": shift,
					"custom_bio_log_id": log.name				})

				checkin.save()
				sql = f"UPDATE bio_attendance_log set is_processed = 'Y', message = '{checkin.name}' where name = '{log.name}'"
				frappe.db.sql(sql)

		except Exception as e:
			frappe.log_error('bio_attendance_exception')
			sql = f"UPDATE bio_attendance_log set is_processed = 'E', message = '{str(e)}' where name = '{log.name}'"
			frappe.db.sql(sql)

@frappe.whitelist()
def reset_attendance_log(bio_id):
	frappe.db.sql(
		f"""
		UPDATE
			bio_attendance_log
			set is_processed = 'N', message = null
		WHERE 
			name = '{bio_id}'
	""", as_dict=True)

	bio = frappe.db.sql("SELECT * from bio_attendance_log where name = %s", bio_id)
	if bio:
		check_ins = frappe.db.get_all("Employee Checkin", filters={"custom_bio_log_id":  bio_id})
		for check_in in check_ins:
			frappe.delete_doc("Employee Checkin", check_in.get("name"))

	frappe.db.commit()
