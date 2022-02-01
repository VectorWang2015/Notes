import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QTabWidget
)

# subclass QMainWindow to customize
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(800,600))

        tabs = QTabWidget()
        # user can move tabs within tab area
        tabs.setMovable(True)

        colors = ['red', 'yellow', 'cyan', 'magenta']
        for color in colors:
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


# need one (and only one) QApp instance per application
app = QApplication(sys.argv)

# Qt Widget, which will be our window
# window = QWidget()
# window = QPushButton("Push me")
window = MainWindow()
window.show() # window are hidden by default

# start event loop
app.exec()

# application will reach here when event exits
# loop stopped
