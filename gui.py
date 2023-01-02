import sys, os, functools
from PIL import Image

from PySide6.QtCore import QSize, Qt, QObject, QEvent
from PySide6.QtGui import QPixmap, QIcon, QAction, QFont
from PySide6.QtWidgets import *

from utils import *

class Task(object) :
    def __init__(self, name = None, desc = None, action = None) :
        self.name, self.desc, self.action = name, desc, action

    def info(self) :
        return "[Task name = %s]" % self.name

def create_frame(name, style, width, sheet, layout) :
    frame = QFrame()
    frame.setObjectName(name)
    frame.setFrameStyle(style)
    frame.setLineWidth(width)
    frame.setStyleSheet("#%s{%s}" % (name, sheet));
    frame.setLayout(layout)
    return frame

def create_panel(app, task, name, style, sheet, layout) :
    panel = QFrame()
    panel.setObjectName(name)
    panel.setFrameStyle(style)
    panel.setStyleSheet("#%s{%s}" % (name, sheet));
    panel.setFrameShadow(QFrame.Shadow.Raised)
    # shadow = QGraphicsDropShadowEffect()
    # shadow.setBlurRadius(15)
    # panel.setGraphicsEffect(shadow)
    panel.setFixedHeight(150)
    layout.setContentsMargins(0, 0, 0, 0)
    panel.setLayout(layout)
    column_frames = [
        create_frame(
            name = "line_frame_1", style = 1, width = 1,
            sheet = "border: 0px solid lightgray;",
            layout = QVBoxLayout()),
        create_frame(
            name = "line_frame_2", style = 1, width = 1,
            sheet = "border: 0px solid lightgray;",
            layout = QVBoxLayout()),
    ]
    column_frames[0].setFixedWidth(500)
    column_frames[1].setFixedWidth(100)
    column_frames[1].layout().setContentsMargins(0, 0, 0, 0)
    for frame in column_frames :
        layout.addWidget(frame)

    name_label = QLabel("Name: %s" % task.name)
    column_frames[0].layout().addWidget(name_label)
    desc = QTextEdit(task.desc)
    column_frames[0].layout().addWidget(desc)

    accept_bt = QPushButton("Accept")
    accept_bt.clicked.connect(functools.partial(app.accept_task, task, desc.toPlainText()))
    abort_bt = QPushButton("Abort")
    abort_bt.clicked.connect(functools.partial(app.abort_task, task))
    reset_bt = QPushButton("Reset")
    reset_bt.clicked.connect(functools.partial(app.reset_task, task, desc))
    for bt in [accept_bt, abort_bt, reset_bt] :
        column_frames[1].layout().addWidget(bt)

    return panel

class MagicPromptMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font = QFont()
        self.font.setPointSize(15)
        self.init_actions()
        self.init_window()
        self.init_menu()
        self.add_log("Started.")

    def init_menu(self) :
        rs_menu = self.menuBar().addMenu('Magic Prompt')
        rs_menu.addAction(self.actions["quit"])


    def init_window(self) :
        self.setWindowTitle('Magic Prompt v0.1 (c) UltraX AI')
        self.setFixedSize(QSize(1350, 750))
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        tab_widget = QTabWidget()
        tab_layout = QVBoxLayout()
        tab_widget.setLayout(tab_layout)
        tab_widget.setTabPosition(QTabWidget.South)
        main_layout.addWidget(tab_widget)
        self.init_spell()
        self.init_log()
        tab_widget.addTab(self.spell_widget, "Spell")
        tab_widget.addTab(self.log_widget, "Logs")
        self.setCentralWidget(main_widget)

    def init_actions(self) :
        self.actions = {}
        self.actions["quit"] = QAction('Quit', self)
        self.actions["quit"].setShortcut('Ctrl+Q')
        self.actions["quit"].setStatusTip('Quit')
        self.actions["quit"].triggered.connect(self.close)

    def init_spell(self) :
        self.spell_widget = QWidget()
        spell_layout = QHBoxLayout()
        self.spell_widget.setLayout(spell_layout)
        line_frames = [
            create_frame(
                name = "line_frame_1", style = 1, width = 1,
                sheet = "border: 1px solid lightgray;",
                layout = QHBoxLayout()),
            create_frame(
                name = "line_frame_2", style = 1, width = 1,
                sheet = "border: 1px solid lightgray;",
                layout = QHBoxLayout()),
        ]
        for frame in line_frames :
            spell_layout.addWidget(frame)
            frame.layout().setContentsMargins(0, 0, 0, 0)
            frame.layout().setSpacing(0)
        line_frames[0].setFixedWidth(400)

    def init_log(self) :
        self.logs = []
        self.log_widget = QWidget()
        log_layout = QVBoxLayout()
        self.log_widget.setLayout(log_layout)
        self.log_output = QTextEdit("")
        self.log_output.setFont(self.font)
        self.log_output.setReadOnly(1)
        self.log_output.verticalScrollBar().rangeChanged.connect(lambda x,y: self.log_output.verticalScrollBar().setValue(y))
        log_layout.addWidget(self.log_output)

    def add_log(self, msg) :
        line = "[%s] %s" % (get_datetime(), msg)
        self.logs.append(line)
        self.log_output.setText(self.log_output.toPlainText() + line + "\n")
        self.statusBar().showMessage(line)

    def trayicon_activated_action(self, reason) :
        for reason in [QSystemTrayIcon.Trigger, ] :
           self.showNormal()

    def accept_task(self, task, desc_text) :
        print("accept_task:", task.name, desc_text)

    def abort_task(self, task) :
        print("abort_task:", task.name)

    def reset_task(self, task, desc) :
        desc.setText(task.desc)

    def eventFilter(self, obj, event) :
        if event.type() == QEvent.KeyPress and obj is self.chat_input :
            if event.key() == Qt.Key_Return and self.chat_input.hasFocus() :
                self.handle_chat_input()
                return True
        return super().eventFilter(obj, event)

