import sys
from PySide6 import QtWidgets as QW

from source import Ui_MainWindow

class MainWindow(QW.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


app = QW.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
