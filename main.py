import sys
import pygetwindow as gw
import pyautogui
import pyperclip
import threading
from pynput import mouse
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGroupBox, QTextEdit, QPushButton
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPixmap,QFont
from PyQt6 import QtCore

import random

WIDTH = 410
HEIGHT = 450

IMAGE = ".\\img\\live_icon_alpha.png"

FREQUENCY = 30

'''
CONTENT_TO_SEND = ['如果有问题问老师，可以关注我~',
                   '如果有问题需要问老师，可以关注我~',
                   '如果有问题问老师，可以先关注我~',
                   '有问题可以发出来，可以关注我~',
                   '有问题可以发在公屏',
                   '如果大家有问题问老师，可以先关注我~'
                   '大家有什么问题，可以积极说出来']
'''

class MAIN_WINDOW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(WIDTH,HEIGHT)
        self.selected_window = None
        self.sending_thread = None
        self.sending = False

        self.UI()

    def UI(self):
        self.Window = QGroupBox(self)
        self.Window.resize(WIDTH,HEIGHT)
        self.Window.setStyleSheet("background-color:white;border-radius: 12px; border: 2px groove;")

        self.layout = QVBoxLayout(self.Window)

        self.Logo = QLabel(self.Window)
        self.image = QPixmap(IMAGE)
        self.image_resize = self.image.scaled(120,120)
        self.Logo.setPixmap(self.image_resize)
        self.Logo.setAlignment(QtCore.Qt.AlignmentFlag(4))
        self.Logo.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")
        self.Logo.resize(WIDTH,100)

        self.Content_Hint = QLabel(self.Window)
        self.Content_Hint.setStyleSheet("background-color:white;border-radius: 12px; border: 0px groove;")
        self.Content_Hint.setText("输入要发送的内容：")
        self.Content_Hint.setFont(QFont("黑体", 13))

        self.Content = QTextEdit(self.Window)
        self.Content.setFixedHeight(100)


        self.Button_Window_Select = QPushButton(self.Window)
        self.Button_Window_Select.setFixedSize(70,30)
        self.Button_Window_Select.setText("选择窗口")
        self.Button_Window_Select.move(170,HEIGHT-90)
        self.Button_Window_Select.clicked.connect(self.select_window)
        self.Button_Window_Select.setStyleSheet("""
            QPushButton:hover {
                background-color: #FC7283;
            }
        """)

        self.Button_Start = QPushButton(self.Window)
        self.Button_Start.setFixedSize(70,30)
        self.Button_Start.setText("开始")
        self.Button_Start.move(WIDTH-120,HEIGHT-90)
        self.Button_Start.clicked.connect(self.start_sending)
        self.Button_Start.setEnabled(False)
        self.Button_Start.setStyleSheet("""
            QPushButton:hover {
                background-color: #FC7283;
            }
        """)

        self.Button_Set_Frequency = QPushButton(self.Window)
        self.Button_Set_Frequency.setFixedSize(70,30)
        self.Button_Set_Frequency.setText("设定内容")
        self.Button_Set_Frequency.move(50,HEIGHT-90)
        self.Button_Set_Frequency.clicked.connect(self.generate_array)
        self.Button_Set_Frequency.setStyleSheet("""
            QPushButton:hover {
                background-color: #FC7283;
            }
        """)

        self.layout.addStretch(1)
        self.layout.addWidget(self.Logo)
        self.layout.addWidget(self.Content_Hint)
        self.layout.addWidget(self.Content)
        self.layout.addStretch(1)
        self.layout.addStretch(1)
        self.layout.addStretch(1)
    
    def generate_array(self):
        input_text = self.Content.toPlainText()
        input_list = input_text.split(",")
        self.content_to_send = [element.strip() for element in input_list if element.strip()]
        self.Content.setReadOnly(True)
        #self.result_text_edit.setPlainText(", ".join(self.generated_array))
    
    def select_window(self):
        self.hide()

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                for window in gw.getWindowsWithTitle(""):
                    if window.left <= x <= window.left + window.width and window.top <= y <= window.top + window.height:
                        self.selected_window = window
                        break
                listener.stop()
                self.Button_Start.setEnabled(True)
                self.show()

        listener = mouse.Listener(on_click=on_click)
        listener.start()
    
    def start_sending(self):
        if not self.sending:
            self.sending = True
            #content_to_send = self.Content.toPlainText()
            frequency = FREQUENCY
            self.sending_thread = threading.Thread(target=self.send_content, args=(frequency,))
            self.sending_thread.start()
            self.Button_Start.setText("运行中..")

    def send_content(self, frequency):
        while self.sending:
            #
            if self.selected_window:
                selected_window = self.selected_window
                # 使用 pyperclip 将内容复制到剪贴板，然后粘贴到窗口
                content = random.choice(self.content_to_send)
                #content = self.content_to_send[random.randint(0,len(self.content_to_send))]
                pyperclip.copy(content)
                selected_window.activate()
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press("enter")
                # 间隔指定的频率
                threading.Event().wait(frequency)
    
    def closeEvent(self, event):
        self.sending = False
        if self.sending_thread:
            self.sending_thread.join()
        super().closeEvent(event)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_px = e.globalPosition().x()
            self.mouse_press_py = e.globalPosition().y()

            self.delta_wx = self.mouse_press_px - self.geometry().x()
            self.delta_wy = self.mouse_press_py - self.geometry().y()
            
    def mouseMoveEvent(self, e):
        self.mouse_px = e.globalPosition().x()
        self.mouse_py = e.globalPosition().y()

        self.move(int(self.mouse_px - self.delta_wx), int(self.mouse_py - self.delta_wy))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MAIN_WINDOW()
    mainWin.show()
    sys.exit(app.exec())