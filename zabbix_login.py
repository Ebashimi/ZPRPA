import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from zabbix_utils import ZabbixAPI

class ZabbixLoginForm(QWidget):

    login_successful = pyqtSignal(object)  # Сигнал для успешной авторизации с одним аргументом

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Zabbix Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.url_label = QLabel("Zabbix URL:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.user_label = QLabel("Username:")
        self.user_input = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.api = None  # Инициализируем переменную для API

    def login(self):

        url = self.url_input.text()
        user = self.user_input.text()
        password = self.password_input.text()

        try:

            self.api = ZabbixAPI(url=url)  # Сохраняем экземпляр API
            self.api.login(user=user, password=password)
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_successful.emit(self.api)  # Испускаем сигнал о успешной авторизации с передачей API
            self.close()  # Закрываем форму авторизации

        except Exception as e:

            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
            print(f"Error during login: {str(e)}")