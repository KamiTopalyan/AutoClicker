import sys
import time

import keyboard
import mouse
import pyautogui
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QCheckBox, \
    QGridLayout, QLabel

pyautogui.FAILSAFE = False


class Clicker(QThread):
    result = pyqtSignal(int)

    def run(self):
        if not checked:
            self.keepRunning = True
            while self.keepRunning:
                mouse.click("left")
                time.sleep(float(textboxValue))
                print("Clicked")
        elif checked:
            self.keepRunning = True
            while self.keepRunning:
                pyautogui.moveTo(int(xValue), int(yValue), duration=0)
                mouse.click("left")
                time.sleep(float(textboxValue))
                print("Clicked at", xValue, yValue)

    def stop(self):
        self.keepRunning = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Create the window
        super().__init__()
        self.checked = False
        self.clicker = Clicker()
        self.setWindowTitle("SuperClicker v1.0")
        self.setGeometry(600, 300, 400, 400)
        self.setWindowIcon(QtGui.QIcon('Icon.png'))

        # Create textbox for delay
        self.textbox = QLineEdit(self)
        self.textbox.move(75, 100)
        self.textbox.resize(58, 40)
        self.onlyInt = QDoubleValidator()
        self.textbox.setValidator(self.onlyInt)
        # Labels

        self.delay = QLabel('Delay per click (Seconds)', self)
        self.delay.move(135, 105)
        self.xLabel = QLabel('X Axis', self)
        self.yLabel = QLabel('Y Axis', self)
        self.xLabel.move(258, 245)
        self.yLabel.move(108, 245)

        # CheckBoxes
        layout = QGridLayout()
        self.setLayout(layout)
        self.b1 = QCheckBox("Specific Clicking", self)
        self.b1.setChecked(False)
        self.b1.move(85, 200)
        self.b1.resize(100, 50)
        layout.addWidget(self.b1, 0, 0)

        # Create textbox for accurate clicking
        self.x = QLineEdit("0", self)
        self.y = QLineEdit("0", self)
        self.x.move(75, 250)
        self.x.resize(30, 20)
        self.x.setValidator(self.onlyInt)
        self.y.move(225, 250)
        self.y.resize(30, 20)
        self.y.setValidator(self.onlyInt)

        # Setup Buttons
        button1 = QPushButton("Start Clicker (F5)", self)
        button2 = QPushButton("Stop Clicker (F6)", self)
        button1.move(75, 300)
        button2.move(225, 300)
        button1.clicked.connect(self.startClicking)
        button2.clicked.connect(self.stopClicking)
        keyboard.add_hotkey("F6", self.stopClicking)
        keyboard.add_hotkey("F5", self.startClicking)

    # Functions for button click actions
    def startClicking(self):
        if not self.clicker.isRunning():
            global textboxValue
            global xValue
            global yValue
            global checked
            textboxValue = self.textbox.text()
            xValue = self.x.text()
            yValue = self.y.text()
            self.clicker.start()
            if self.b1.isChecked() and float(textboxValue) != 0:
                checked = True
            elif not self.b1.isChecked() and float(textboxValue) != 0:
                checked = False
            else:
                print("Try a value except 0 like 0.1 for the delay.")

    def stopClicking(self):
        self.clicker.stop()
        print("stopped")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
