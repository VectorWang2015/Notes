import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QLabel, QCheckBox, QComboBox, QLineEdit, QListWidget,
        QSpinBox, QDoubleSpinBox, QSlider
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400,300))

        """
        # qlabel font example
        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        """

        """
        # qlabel picture example
        widget = QLabel()
        widget.setPixmap(QPixmap('./ZhaoWu.jpg'))
        widget.setScaledContents(True)
        """

        """
        # qcheckbox
        widget = QCheckBox()
        widget.setCheckState(Qt.Checked)
        widget.setText("Checkbox")

        widget.stateChanged.connect(self.show_state)
        """

        """
        # qcombobox
        widget = QComboBox()
        widget.addItems(["one", "two", "three"])

        widget.currentIndexChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        widget.setEditable(True)
        widget.setInsertPolicy(QComboBox.InsertAlphabetically)
        widget.setMaxCount(10)
        """

        """
        # qlistwidget
        widget = QListWidget()
        widget.addItems(["one", "two", "three"])

        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)
        """

        """
        # qlineedit
        widget = QLineEdit()
        widget.setMaxLength(20)
        widget.setPlaceholderText("Enter your text")

        # widget.setReadOnly(True)

        widget.returnPressed.connect(self.return_pressed)
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)

        widget.setInputMask('000.000.000.000:_')
        """
        
        """
        # qspinbox supports int while qdoublespinbox supports float
        widget = QSpinBox()

        widget.setRange(-10,3)

        widget.setPrefix("$")
        widget.setSuffix("c")
        # change step for arrows
        widget.setSingleStep(3)
        widget.valueChanged.connect(self.value_changed)
        widget.textChanged.connect(self.value_changed_str)
        """

        widget = QSlider(Qt.Horizontal)

        widget.setRange(-10,3)

        widget.setSingleStep(3)

        widget.valueChanged.connect(self.value_changed)
        widget.sliderMoved.connect(self.slider_position)
        widget.sliderPressed.connect(self.slider_pressed)
        widget.sliderReleased.connect(self.slider_released)

        self.setCentralWidget(widget)

    def show_state(self, s):
        print(s == Qt.Checked)
        print(s)

    def index_changed(self, i):
        print(i)

    def return_pressed(self):
        print("Return pressed")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed")
        print(s)

    def text_edited(self, s):
        print("Text edited")
        print(s)

    def value_changed(self, i):
        print(i)

    def value_changed_str(self, s):
        print(s)

    def slider_position(self, p):
        print("Position {}".format(p))

    def slider_pressed(self):
        print("Pressed")

    def slider_released(self):
        print("Released")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
