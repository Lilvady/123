import pandas as pd

class Report:
    def __init__(self, database):
        self.database = database

    def generate_excel_report(self):
        data = self.database.get_work_hours()
        df = pd.DataFrame(data, columns=['ФИО', 'Часы'])
        df.to_excel('work_hours_report.xlsx', index=False)