class Shift:
    def __init__(self, user_id, database):
        self.user_id = user_id
        self.database = database

    def register_hours(self, hours, break_time, sick_leave, vacation):
        self.database.submit_hours(self.user_id, hours, break_time, sick_leave, vacation)

    def request_sick_leave(self, sick_leave_reason):
        self.database.submit_leave_request(self.user_id, "sick leave", sick_leave_reason, "pending")

    def request_vacation(self, vacation_reason):
        self.database.submit_leave_request(self.user_id, "vacation", vacation_reason, "pending")
