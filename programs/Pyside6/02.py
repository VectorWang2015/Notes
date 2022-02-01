import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow,\
        QVBoxLayout, QLineEdit, QLabel, QWidget, QMenu
from random import choice


window_titles = [
        'My App',
        'Still My App',
        'What on Earth',
        'This is Surprising',
        'Something Went Wrong'
]


# subclass QMainWindow to customize
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        """
        self.button_is_checked = True
        self.button = QPushButton("Press Me!")
        self.label = QLabel()
        self.input = QLineEdit()

        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("My App")
        #self.setFixedSize(QSize(400,300))
        #self.setMaximumSize(QSize(400,300))
        self.setMinimumSize(QSize(400,300))
        """
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

    def contextMenuEvent(self, e):
        """
        e.ignore() to bubble up the hierarchy
        """
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())

    def mouseMoveEvent(self, e):
        # only triggers when mouse hold
        # change behavior here
        self.setMouseTracking(True)
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText("mousePressEvent LEFT")
        elif e.button() == Qt.RightButton:
            self.label.setText("mousePressEvent RIGHT")
        elif e.button() == Qt.MiddleButton:
            self.label.setText("mousePressEvent MIDDLE")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")

    """
        # button is not checkable by default
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        #self.button.clicked.connect(self.button_toggled)
        #self.button.released.connect(self.button_released)

        self.windowTitleChanged.connect(self.window_title_changed)
        # set the central widget of the window
        self.setCentralWidget(self.button)

    # a simple custom slot, any method / function can be slot
    def button_clicked(self):
        print("Clicked!")
        new_window_title = choice(window_titles)
        print("Setting title: {}".format(new_window_title))
        self.setWindowTitle(new_window_title)

    def button_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", self.button_is_checked)

    def button_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)

    def window_title_changed(self, window_title):
        print("Window title changed: {}".format(window_title))
        
        if window_title == 'Something Went Wrong':
            self.button.setEnabled(False)
    """


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
