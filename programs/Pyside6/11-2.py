from PySide6.QtCore import QRunnable, Slot, QThreadPool, QTimer, Signal, QObject
from PySide6.QtWidgets import (
        QVBoxLayout, QLabel, QPushButton,
        QWidget, QMainWindow, QApplication
)

import sys
import time


def thread_sleep(seconds=5):
    print("Thread starts")
    time.sleep(seconds)
    print("Thread ends")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

        self.counter = 0
        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        worker = Worker(thread_sleep, seconds=1)
        worker.signals.finished.connect(self.worker_finished)
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: {}".format(self.counter))

    def worker_finished(self):
        print("Finished signal received")


class WorkerSignal(QObject):
    finished = Signal()


class Worker(QRunnable):
    """
    Worker thread
    Since custom signals can only be defined on objs
    derived from QObjects, while QRunnable is not a QObject,
    we cant define Signal() here directly
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()

    @Slot() #QtCore.Slot
    def run(self):
        """
        Your code goes in this function
        """
        self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit()


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
