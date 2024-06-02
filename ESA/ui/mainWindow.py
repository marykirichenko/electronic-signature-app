from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QLabel, QVBoxLayout, QStackedWidget, QWidget, QPushButton, QComboBox
from ui.signingPage import SignDocumentWindow
from ui.signatureVerification import VerifySignatureWindow
from ui.encryptionPage import EncryptDocumentWindow
from ui.decryptionPage import DecryptDocumentWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        self.layout = QVBoxLayout()
        self.setWindowTitle('Mariia Kyrychenko s192425')
        self.setGeometry(50, 50, 1000, 600)
        self.setStyleSheet("background-color: white;")

        self.user_dropdown = QComboBox()
        self.user_dropdown.addItems(['User A', 'User B'])
        self.user_dropdown.setStyleSheet(
            "font-size: 20pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;margin-left:600px; background-color: #4CAF50;")
        self.user_dropdown.currentIndexChanged.connect(self.update_button_visibility)

        self.layout.addWidget(self.user_dropdown)

        self.welcome_label_text = 'Your security tool'
        self.welcome_label = QLabel(self.welcome_label_text)
        self.welcome_label.setStyleSheet("color: black; font-size: 44pt;")
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)

        self.initials_text = 'By Mariia Kyrychenko, 192425'
        self.initials_label = QLabel(self.initials_text)
        self.initials_label.setStyleSheet("color: black; font-size: 20px;")
        self.initials_label.setAlignment(QtCore.Qt.AlignCenter)

        self.sign_doc_button = QPushButton('Sign a document/file')
        self.sign_doc_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.sign_doc_button.clicked.connect(self.open_sign_doc_window)

        self.verify_doc_button = QPushButton('Verify signature')
        self.verify_doc_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.verify_doc_button.clicked.connect(self.open_verify_doc_window)

        self.encrypt_doc_button = QPushButton('Encrypt a document/file')
        self.encrypt_doc_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.encrypt_doc_button.clicked.connect(self.open_encrypt_doc_window)

        self.decrypt_doc_button = QPushButton('Decrypt a document/file')
        self.decrypt_doc_button.setStyleSheet(
            "font-size: 30pt; background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.decrypt_doc_button.clicked.connect(self.open_decrypt_doc_window)

        self.button_layout_top = QHBoxLayout()
        self.button_layout_top.addWidget(self.sign_doc_button)
        self.button_layout_top.addWidget(self.verify_doc_button)

        self.button_layout_bottom = QHBoxLayout()
        self.button_layout_bottom.addWidget(self.encrypt_doc_button)
        self.button_layout_bottom.addWidget(self.decrypt_doc_button)

        self.layout.addWidget(self.welcome_label)
        self.layout.addLayout(self.button_layout_top)
        self.layout.addLayout(self.button_layout_bottom)
        self.layout.addWidget(self.initials_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.stack.addWidget(self.central_widget)

        self.sign_doc_window = None
        self.verify_doc_window = None
        self.encrypt_doc_window = None
        self.decrypt_doc_window = None

        self.update_button_visibility()

    def update_button_visibility(self):
        selected_user = self.user_dropdown.currentText()
        if selected_user == 'User A':
            self.sign_doc_button.show()
            self.verify_doc_button.show()
            self.encrypt_doc_button.show()
            self.decrypt_doc_button.show()
        elif selected_user == 'User B':
            self.sign_doc_button.hide()
            self.verify_doc_button.show()
            self.encrypt_doc_button.show()
            self.decrypt_doc_button.show()

    def open_sign_doc_window(self):
        if not self.sign_doc_window:
            self.sign_doc_window = SignDocumentWindow(self)
            self.stack.addWidget(self.sign_doc_window)
        self.stack.setCurrentWidget(self.sign_doc_window)

    def open_verify_doc_window(self):
        if not self.verify_doc_window:
            self.verify_doc_window = VerifySignatureWindow(self)
            self.stack.addWidget(self.verify_doc_window)
        self.stack.setCurrentWidget(self.verify_doc_window)

    def open_encrypt_doc_window(self):
        if not self.encrypt_doc_window:
            self.encrypt_doc_window = EncryptDocumentWindow(self)
            self.stack.addWidget(self.encrypt_doc_window)
        self.stack.setCurrentWidget(self.encrypt_doc_window)

    def open_decrypt_doc_window(self):
        if not self.decrypt_doc_window:
            self.decrypt_doc_window = DecryptDocumentWindow(self)
            self.stack.addWidget(self.decrypt_doc_window)
        self.stack.setCurrentWidget(self.decrypt_doc_window)
