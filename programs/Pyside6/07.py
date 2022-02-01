import sys
from random import randint
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QPushButton, QDialog, QDialogButtonBox, QLabel,
        QVBoxLayout, QWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = None
        self.setWindowTitle("Main Window")
        self.setMinimumSize(QSize(400,300))

        button = QPushButton("Press me for another window")
        button.clicked.connect(self.toggle_new_window)
        self.setCentralWidget(button)

    def button_clicked(self, checked):
        # if use local variable, windows will be cleared
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

    def toggle_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
        elif self.w.isVisible():
            self.w.hide()
            #self.w.close()
            #self.w = None
        else:
            self.w.show()


class AnotherWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Another window {}".format(randint(0,100)))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
