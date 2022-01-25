import sys
import time
import mouse
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Clicker(QThread):
    result = pyqtSignal(str)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            mouse.click("left")
            time.sleep(0.01)
            print("Clicked")

    def stop(self):
        self.keepRunning = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.checked = False
        self.clicker = Clicker()
        self.setWindowTitle("SuperClicker v1.0")
        self.setGeometry(600, 300, 400, 400)

        button1 = QPushButton("Start Clicker", self)
        button2 = QPushButton("Stop Clicker", self)
        button2.move(200, 0)
        self.clicker.result.connect(self.resultReceived)
        button1.clicked.connect(self.startClicking)
        button2.clicked.connect(self.stopClicking)

    def startClicking(self):
        if not self.clicker.isRunning():
            self.clicker.start()

    def stopClicking(self):
        self.clicker.stop()

    def resultReceived(self, result):
        print(result)

    def emergencyStop(self):
        self.clicker.stop()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
