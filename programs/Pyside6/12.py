from PySide6.QtWidgets import (
        QApplication, QMainWindow, QPushButton,
        QPlainTextEdit, QVBoxLayout, QWidget)
from PySide6.QtCore import QProcess
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.p = None

        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.start_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode('utf-8')
        self.message(stdout)

    def message(self, s):
        self.text.appendPlainText(s)

    def process_finished(self):
        self.message("Process finished")
        self.p = None

    def start_process(self):
        if not self.p:
            self.message("Executing process.")
            self.p = QProcess()
            self.p.finished.connect(self.process_finished)
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.start("python", ['12-dummy-script.py'])


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
