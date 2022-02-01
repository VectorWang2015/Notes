import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout
)

# subclass QMainWindow to customize
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(800,600))

        """
        # combined layouts
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('blue'))
        layout2.addWidget(Color('green'))

        layout3.addWidget(Color('yellow'))
        layout3.addWidget(Color('cyan'))
        layout3.addWidget(Color('magenta'))

        layout1.addWidget(Color('purple'))
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(10)
        """

        """
        # grid layout
        layout1 = QGridLayout()
        layout1.addWidget(Color('red'), 0, 0)
        layout1.addWidget(Color('green'), 1, 0)
        layout1.addWidget(Color('blue'), 0, 1)
        layout1.addWidget(Color('purple'), 2, 1)
        """

        layout1 = QStackedLayout()

        layout1.addWidget(Color('red'))
        layout1.addWidget(Color('green'))
        layout1.addWidget(Color('blue'))
        layout1.addWidget(Color('cyan'))

        layout1.setCurrentIndex(3)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


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
