from PySide6.QtWidgets import (
        QApplication, QMainWindow
)
from PySide6.QtCore import Qt

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # SIGNAL: The connected fucniton will be called whenever window
        # title is changed. The new title will be passed to the function
        self.windowTitleChanged.connect(self.on_window_title_changed)

        # SIGNAL: The connected function will be called whenever the window
        # title is changed. The new title is discarded and the
        # function is called without params
        self.windowTitleChanged.connect(lambda x: self.on_window_title_changed_no_params())

        # SIGNAL: The connected funciton will be called whenever the window
        # title is changed. The new title is discarded and the
        # function is called without params
        self.windowTitleChanged.connect(lambda x: self.my_costum_fn())

        # SIGNAL: The connected function will be called whenever the window
        # title is changed. The new title is passed to the function
        # and replaces the default parameter. Extra data is passed from
        # within the lambda
        self.windowTitleChanged.connect(lambda x: self.my_costum_fn(x, 25))

            # This sets the window title, which will trigger all the above signals
        self.setWindowTitle("My Signals App")

    # SLOT: This accepts a string, e.g. the window title, and prints it
    def on_window_title_changed(self, s):
        print(s)

    # SLOT: This is called when the window title changes
    def on_window_title_changed_no_params(self):
        print("Window title changed")

    # SLOT: This has default parameters and can be called without a value
    def my_costum_fn(self, a="Hello", b=5):
        print(a, b)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
