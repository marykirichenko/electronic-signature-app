from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from core.encryptionMechanism import EncryptionMechanism
from ui.statusPopup import status_popup

# filepath of public key is predefined
class EncryptDocumentWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.filename = None
        self.main_window = main_window

        layout = QVBoxLayout()
        self.label = QLabel('No file selected')

        self.upload_button = QPushButton('Upload')
        self.upload_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin-left: 200px;margin-bottom: 100px;")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.label.setStyleSheet("color: black; font-size: 30pt; margin-left:100px")

        self.encrypt_button = QPushButton('Encrypt file')
        self.encrypt_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px; margin-right: 200px;margin-bottom: 100px;")
        self.encrypt_button.clicked.connect(self.encrypt_file)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.encrypt_button)

        layout.addWidget(self.label)
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
        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if filename:
            self.label.setText('Filepath:' + filename)
            self.filename = filename

    def encrypt_file(self):
        if not self.filename:
            status_popup('Please select a file first')
            return
        try:
            EncryptionMechanism().encrypt(self.filename)
            status_popup('File encrypted successfully')
        except Exception as e:
            status_popup('Error encrypting file: ' + str(e))

