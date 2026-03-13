"""Entry point de PDF Manager."""

import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.style import APP_STYLE
from ui.merge_tab import MergeTab
from ui.reorder_tab import ReorderTab


def resource_path(relative_path: str) -> str:
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath('.')
    return os.path.join(base, relative_path)


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Manager')
        ico = resource_path('PDF.ico')
        if os.path.exists(ico):
            self.setWindowIcon(QIcon(ico))
        self.resize(1400, 820)

        tabs = QTabWidget()
        tabs.addTab(MergeTab(),   'Unir PDFs')
        tabs.addTab(ReorderTab(), 'Reordenar páginas')

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(tabs)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setStyleSheet(APP_STYLE)

    window = AppWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
