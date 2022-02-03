from PySide6.QtWidgets import (
        QApplication, QMainWindow, QCheckBox
)
from PySide6.QtCore import Qt

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        checkbox = QCheckBox("Check?")

        # option1: conversion function
        def checkstate_to_bool(state):
            if state == Qt.Checked:
                return self.result(True)
            return self.result(False)

        checkbox.stateChanged.connect(checkstate_to_bool)

        # option2: lut
        _convert = {
                Qt.Checked: True,
                Qt.Unchecked: False
        }

        checkbox.stateChanged.connect(
                lambda v: self.result(_convert[v])
        )

        self.setCentralWidget(checkbox)


    def result(self, v):
        print(v)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
