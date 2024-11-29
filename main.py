import sys
import PyQt6
from PyQt6.QtWidgets import QApplication
from auth import Auth
import database as DatabaseModule
from ui import LoginWindow, EmployeeWindow, AdminWindow


class MainApp(PyQt6.QtWidgets.QApplication):
    def __init__(self, sys_argv: list):
        super(MainApp, self).__init__(sys_argv)
        self.sys_argv = sys_argv
        self.database = DatabaseModule.Database()
        self.auth = Auth(self.database)
        self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginWindow(database=self.database, parent=None)
        self.login_window.show()

    def show_employee_window(self) -> None:
        username = self.login_window.username_input.text()
        employee_window = self.create_window(EmployeeWindow, username)
        employee_window.show()

    def show_admin_window(self) -> None:
        admin_window = self.create_window(AdminWindow)
        admin_window.show()

    def create_window(self, window_class, *args):
        return window_class(*args, self.database, parent=None)


if __name__ == '__main__':
    app = MainApp(sys.argv if hasattr(sys, 'argv') else [])
    sys.exit(app.exec())
