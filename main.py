import sys, os

from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QPixmap, QCloseEvent
from PySide6.QtCore import QObject, QEvent, Qt

from utils import *
from gui import MagicPromptMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap(os.path.join(get_rsc_path(), "magic-prompt.png"))))
    window = MagicPromptMainWindow()
    window.show()
    app.exec()
    sys.exit()
