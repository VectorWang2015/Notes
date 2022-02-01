import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QPushButton, QDialog, QDialogButtonBox, QLabel,
        QVBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400,300))

        button = QPushButton("Press me for a dialog")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("clicked {}".format(s))

        dlg = CustomDialog(self)
        result = dlg.exec()
        if result:
            print("OK!")
        else:
            print("Cancelled!")


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Hello!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        msg_label = QLabel("Something happened, is that OK?")
        self.layout.addWidget(msg_label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
