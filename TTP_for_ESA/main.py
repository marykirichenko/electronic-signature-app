import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox

import errorDefinitions
import keyGenerator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle('Trusted Third Party s192425')
        self.setGeometry(50, 50, 1000, 600)
        self.setStyleSheet("background-color: white;")

        self.welcome_label_text = 'Generate private key'
        self.welcome_label = QLabel(self.welcome_label_text)
        self.welcome_label.setStyleSheet("color: black; font-size: 44pt;")
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)

        self.initials_text = 'By Mariia Kyrychenko, 192425'
        self.initials_label = QLabel(self.initials_text)
        self.initials_label.setStyleSheet("color: black; font-size: 20px;")
        self.initials_label.setAlignment(QtCore.Qt.AlignCenter)

        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet(
            "font-size: 36pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.start_button.clicked.connect(self.start_button_clicked)

        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.initials_label)
        self.layout.addWidget(self.start_button, alignment=QtCore.Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def start_button_clicked(self):
        self.welcome_label.setText('')
        self.initials_label.setText('')
        self.start_button.setParent(None)
        self.enter_pin_page()

    def enter_pin_page(self):
        self.pin_label_text = 'Please enter a 8-digit PIN for encrypting your private key!'
        self.pin_label = QLabel(self.pin_label_text)
        self.pin_label.setStyleSheet("color: black; font-size: 34pt;")
        self.pin_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create a sub-layout for the enter PIN page elements
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(self.pin_label, alignment=QtCore.Qt.AlignCenter)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter pin")
        self.input_field.setStyleSheet(
            "font-size: 16pt; border: 2px solid black; border-radius: 10px; padding: 5px; width:100%; color:black")
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.textChanged.connect(self.validate_input)

        self.submit_button = QPushButton('Generate keys')
        self.submit_button.clicked.connect(self.submit_button_clicked)
        self.submit_button.setStyleSheet(
            "font-size: 36pt; background-color: #919190; color: white; border-radius: 10px; padding: 10px 20px;")
        self.submit_button.setEnabled(False)  # Disable submit button initially

        sub_layout.addWidget(self.input_field, alignment=QtCore.Qt.AlignCenter)
        sub_layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignCenter)

        # Add the sub-layout to the main layout (ensuring full window stretch)
        self.layout.addLayout(sub_layout, stretch=1)

    def validate_input(self, text):
        if len(text) == 8:
            self.submit_button.setEnabled(True)
            self.submit_button.setStyleSheet(
                "font-size: 36pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
            self.input_field.setStyleSheet(
                "font-size: 16pt; border: 2px solid black; border-radius: 10px; padding: 5px; width:100%; color:black;")
        else:
            self.submit_button.setEnabled(False)
            self.input_field.setStyleSheet(
                "font-size: 16pt; border: 2px solid red; border-radius: 10px; padding: 5px; width:100%; color:black;")
            self.submit_button.setStyleSheet(
                "font-size: 36pt; background-color: #919190; color: white; border-radius: 10px; padding: 10px 20px;")

    def status_popup(self, message):
        status_popup = QMessageBox()
        status_popup.setText(message)
        status_popup.exec_()
        status_popup.setStandardButtons(QMessageBox.Ok)

    def submit_button_clicked(self):
        pin = self.input_field.text()
        generator = keyGenerator.KeyGenerator(pin)
        try:
            generator.write_keys_to_file()
            # encrypted private key loaded to the NO NAME usb stick, public key is stored on Desktop
            self.status_popup('Keys generation finished successfully.')
        except errorDefinitions.NoValidUSBDevice:
            self.status_popup('No valid USB dongle device has been inserted into the computer. Try again!')
        except errorDefinitions.PrivateKeyDontExist:
            self.status_popup('Private key generation error. Try again!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
