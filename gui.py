from main import *
from endpoint import *
from discovery import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow): #instance of new window
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)

        self.setWindowTitle("Network Diagnostics Interface")
        self.setFixedSize(800,500)

        discovery_button = QPushButton("Discover Endpoints", self)
        discovery_button.move(1,1)
        discovery_button.clicked.connect(self.open_console(self.wrapper_discover))

        exit_window = QPushButton("EXIT", self)
        exit_window.move(700,470)
        exit_window.clicked.connect(lambda:self.close())

    def open_console(self, func_call): #generates console window output from passed function

        self.console = QTextEdit(readOnly=True)

        self.console.move(QDesktopWidget().availableGeometry().center())
        self.console.resize(800,500)
        self.console.show()
        self.process = QProcess(self)

        func_call()
        self.process.start()
        self.process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)

    def wrapper_discover(self):
        get_internal_endpoints(self.process)

    @pyqtSlot()
    def on_readyReadStandardOutput(self):
        text = self.process.readAllStandardOutput().data().decode()
        self.console.append(text)

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec_()

