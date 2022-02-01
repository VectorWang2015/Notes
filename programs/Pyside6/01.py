import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

# subclass QMainWindow to customize
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        #self.setFixedSize(QSize(400,300))
        #self.setMaximumSize(QSize(400,300))
        self.setMinimumSize(QSize(400,300))

        button = QPushButton("Press Me!")

        # set the central widget of the window
        self.setCentralWidget(button)


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
