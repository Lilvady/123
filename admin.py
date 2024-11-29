class Admin:
    def __init__(self, database):
        self.database = database

    def view_reports(self):
        return self.database.get_work_hours()

    def approve_request(self, user_id, request_type, comment):
        # Логика для одобрения отпусков/больничных
        self.database.update_request_status(user_id, request_type, 'approved')
