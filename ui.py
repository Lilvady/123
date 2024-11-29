
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QWidget
class LoginWindow(QtWidgets.QDialog):
    def __init__(self, parent, database):
        self.database = database
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle('Вход')
        self.setGeometry(100, 100, 300, 200)

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton('Регистрация', self)
        self.login_button = QPushButton('Войти', self)

        self.register_button.clicked.connect(self.register)
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Логин:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def register(self) -> None:
        username = self.username_input.text()
        password = self.password_input.text()
        if self.database.register_user(username, password):
            QtWidgets.QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким логином уже существует!')

    def login(self) -> None:
        # Connection setup
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.database.login_user(username, password)
        if user:
            if self.parent is not None:
                if user[3] == 'сотрудник':
                    self.parent.show_employee_window()
                else:
                    self.parent.show_admin_window()
            else:
                QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                              'Невозможно открыть следующее окно, так как родительский объект отсутствует.')
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!')

class EmployeeWindow(QWidget):
    def __init__(self, username, database, parent=None):
        super().__init__(parent)
        self.username = username
        self.database = database
        self.setWindowTitle(f"Employee - {self.username}")
        self.setGeometry(100, 100, 400, 300)

        self.hours_input = QSpinBox(self)
        self.break_input = QSpinBox(self)
        self.sick_leave_input = QLineEdit(self)
        self.vacation_input = QLineEdit(self)

        self.submit_button = QPushButton('Отправить данные', self)
        self.report_button = QPushButton('Сгенерировать отчет', self)

        self.submit_button.clicked.connect(self.submit_data)
        self.report_button.clicked.connect(self.generate_report)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Часы работы:'))
        layout.addWidget(self.hours_input)
        layout.addWidget(QLabel('Перерывы (минут):'))
        layout.addWidget(self.break_input)
        layout.addWidget(QLabel('Запрос на больничный (дней):'))
        layout.addWidget(self.sick_leave_input)
        layout.addWidget(QLabel('Запрос на отпуск (дней):'))
        layout.addWidget(self.vacation_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.report_button)
        self.setLayout(layout)

    def submit_data(self):
        hours = self.hours_input.value()
        break_time = self.break_input.value()
        sick_leave_days = int(self.sick_leave_input.text() or 0)
        vacation_days = int(self.vacation_input.text() or 0)
        self.database.record_work_hours(self.username, hours, break_time, sick_leave_days, vacation_days)
        QMessageBox.information(self, 'Успех', 'Данные успешно зарегистрированы!')

class AdminWindow(QWidget):
        # Admin window setup
    def __init__(self, database):
        super(AdminWindow, self).__init__(None)
        self.database_connection = database
        self.setWindowTitle('Администратор')
        self.setGeometry(100, 100, 400, 300)

        self.report_button = QPushButton('Показать отчет', self)
        self.approve_button = QPushButton('Одобрить отпуск/больничный', self)

        self.report_button.clicked.connect(self.show_report)
        self.approve_button.clicked.connect(self.approve_request)

        layout = QVBoxLayout()
        layout.addWidget(self.report_button)
        layout.addWidget(self.approve_button)
        self.setLayout(layout)

    def show_report(self):
        data = self.database.get_work_hours()
        report = "\n".join([f"{row[0]} - {row[1]} часов" for row in data])
        QtWidgets.QMessageBox.information(self, 'Отчет', report)

    def approve_request(self):
        self.database_connection.approve_leave_request(user_id, request_type, 'approved')
        QtWidgets.QMessageBox.information(self, 'Одобрение', 'Запрос на отпуск/больничный одобрен!')

