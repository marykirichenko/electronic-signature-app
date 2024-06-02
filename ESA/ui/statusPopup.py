from PyQt5.QtWidgets import QMessageBox

def status_popup(message):
    status_popup = QMessageBox()
    status_popup.setText(message)
    status_popup.exec_()
    status_popup.setStandardButtons(QMessageBox.Ok)