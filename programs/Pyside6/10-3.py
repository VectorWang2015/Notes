from PySide6.QtWidgets import (
        QApplication, QMainWindow, QCheckBox, QWidget,
        QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.label = QLabel('')

        v = QVBoxLayout()
        h = QHBoxLayout()

        for num in range(10):
            button = QPushButton(str(num))
            button.pressed.connect(
                    # this will generate 9 for each click
                    # cuz 'num' is pointer
                    #lambda: self.button_pressed(num)
                    lambda val=num: self.button_pressed(val)
            )
            h.addWidget(button)

        v.addLayout(h)
        v.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(v)

        self.setCentralWidget(widget)

    def button_pressed(self, num):
        self.label.setText(str(num))


    def result(self, v):
        print(v)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
