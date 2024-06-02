from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QFileDialog, QHBoxLayout
from ui.statusPopup import status_popup
from core.signingMechanism import SigningMechanism

class SignDocumentWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.filename = None
        self.pin = None
        self.main_window = main_window

        layout = QVBoxLayout()
        self.label = QLabel('No file selected (use PDF or TXT files)')

        self.pin_label_text = 'Please enter a 8-digit PIN for encrypting your private key!'
        self.pin_label = QLabel(self.pin_label_text)
        self.pin_label.setStyleSheet("color: black; font-size: 20pt; margin-left:100px")

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter pin")
        self.input_field.setStyleSheet(
            "font-size: 16pt; border: 2px solid black; border-radius: 10px; padding: 5px; width:60%; color:black; margin-left:100px; margin-right: 100px;")
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.textChanged.connect(self.validate_input)


        self.upload_button = QPushButton('Upload')
        self.upload_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin-left: 200px;margin-bottom: 100px;")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.label.setStyleSheet("color: black; font-size: 30pt; margin-left:100px; ")

        self.decrypt_button = QPushButton('Sign file')
        self.decrypt_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin-right: 200px;margin-bottom: 100px;")
        self.decrypt_button.clicked.connect(self.decrypt_file)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.decrypt_button)

        layout.addWidget(self.label)
        layout.addWidget(self.pin_label)
        layout.addWidget(self.input_field)
        layout.addLayout(self.button_layout)

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin: 30px;")
        back_button.clicked.connect(self.go_back_to_home)
        layout.addWidget(back_button)
        self.setLayout(layout)


    def go_back_to_home(self):
        self.main_window.stack.setCurrentWidget(self.main_window.central_widget)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "", "PDF Files (*.pdf);;Text Files (*.txt)",
                                                  options=options)
        if filename:
            self.label.setText('Filepath:' + filename)
            self.filename = filename

    def decrypt_file(self):
        if not self.filename:
            status_popup('Please select a file first')
            return
        if not self.pin:
            status_popup('Please enter a pin first')
            return
        try:
            SigningMechanism(self.pin, self.filename).create_xml_signature()
            status_popup('File signed successfully')
        except Exception as e:
            status_popup('Error happened while signing file')

    def validate_input(self, text):
        self.pin = text
        if len(text) == 8:
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setStyleSheet(
                "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin-right: 200px;margin-bottom: 100px;")
            self.input_field.setStyleSheet(
                "font-size: 16pt; border: 2px solid black; border-radius: 10px; padding: 5px; width:60%; color:black; margin-left:100px; margin-right: 100px;")
        else:
            self.decrypt_button.setEnabled(False)
            self.input_field.setStyleSheet(
                "font-size: 16pt; border: 2px solid red; border-radius: 10px; padding: 5px; width:60%; color:black; margin-left:100px; margin-right: 100px;")
            self.decrypt_button.setStyleSheet(
                "font-size: 30pt; background-color: #919190; color: white; border-radius: 10px; padding: 10px 20px; margin-right: 200px;margin-bottom: 100px;")
