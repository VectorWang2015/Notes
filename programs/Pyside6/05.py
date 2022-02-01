import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QLabel, QToolBar, QStatusBar
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400,300))

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        # qaction is an abstraction for user commands
        # here self is the parent for the action
        button_action = QAction(QIcon('./bug.png'), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.tool_bar_button_clicked)
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(button_action)
        toolbar.addSeparator()

        button_action2 = QAction(QIcon('./bug.png'), "Your button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.tool_bar_button_clicked)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        # set status bar
        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        # no & works too, why? c++?
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()
        file_menu.addAction(button_action2)

    def tool_bar_button_clicked(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
