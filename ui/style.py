"""Tema visual global de la aplicación."""

from PyQt5.QtGui import QColor

HIGHLIGHT_COLOR = QColor('#4a90d9')
NORMAL_BG       = QColor(0, 0, 0, 0)

APP_STYLE = """
QWidget {
    background-color: #1a1b26;
    color: #c0caf5;
    font-family: 'Segoe UI', 'Ubuntu', 'Noto Sans', sans-serif;
    font-size: 14px;
}

/* ── Pestañas ── */
QTabWidget::pane {
    border: 1px solid #2f3349;
    border-radius: 0 8px 8px 8px;
    background: #1a1b26;
}
QTabBar::tab {
    background: #16172a;
    color: #6b7099;
    border: 1px solid #2f3349;
    border-bottom: none;
    padding: 10px 32px;
    font-size: 14px;
    font-weight: 600;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 3px;
    min-width: 160px;
}
QTabBar::tab:selected {
    background: #1a1b26;
    color: #c0caf5;
    border-bottom: 2px solid #4a90d9;
}
QTabBar::tab:hover:!selected {
    background: #24283b;
    color: #a9b1d6;
}

/* ── Botones base ── */
QPushButton {
    background-color: #2f3349;
    color: #c0caf5;
    border: 1px solid #3a4060;
    border-radius: 7px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: 600;
    min-width: 130px;
    min-height: 40px;
}
QPushButton:hover   { background-color: #3a4060; border-color: #4a90d9; color: #ffffff; }
QPushButton:pressed { background-color: #4a90d9; border-color: #4a90d9; color: #ffffff; }
QPushButton:disabled { background-color: #1c1d2e; color: #3d4060; border-color: #252535; }

QPushButton[role="primary"] { background-color: #4a90d9; border-color: #4a90d9; color: #ffffff; }
QPushButton[role="primary"]:hover   { background-color: #5ba3eb; border-color: #5ba3eb; }
QPushButton[role="primary"]:pressed { background-color: #3478c0; }

QPushButton[role="danger"] { background-color: #2a1a22; border-color: #f7768e; color: #f7768e; }
QPushButton[role="danger"]:hover   { background-color: #f7768e; color: #ffffff; }
QPushButton[role="danger"]:pressed { background-color: #d45e74; color: #ffffff; }

QPushButton[role="ghost"] { background-color: transparent; border-color: #3a4060; color: #a9b1d6; min-width: 110px; }
QPushButton[role="ghost"]:hover   { border-color: #4a90d9; color: #c0caf5; background-color: #24283b; }
QPushButton[role="ghost"]:pressed { background-color: #2f3349; }
QPushButton[role="ghost"]:disabled { color: #3d4060; border-color: #252535; background: transparent; }

/* ── Inputs ── */
QLineEdit {
    background-color: #24283b;
    color: #c0caf5;
    border: 1px solid #2f3349;
    border-radius: 7px;
    padding: 6px 14px;
    font-size: 14px;
    selection-background-color: #4a90d9;
    min-height: 38px;
}
QLineEdit:focus    { border-color: #4a90d9; background-color: #252640; }
QLineEdit:read-only { background-color: #1e2030; color: #6b7099; }

/* ── Listas ── */
QListWidget {
    background-color: #1e2030;
    border: 1px solid #2f3349;
    border-radius: 8px;
    padding: 6px;
    outline: 0;
    font-size: 13px;
}
QListWidget::item { color: #c0caf5; border-radius: 5px; padding: 5px 10px; min-height: 28px; }
QListWidget::item:selected { background-color: #2a3a5a; color: #7dc4e4; border: 1px solid #4a90d9; }
QListWidget::item:hover:!selected { background-color: #24283b; }

/* ── Scroll ── */
QScrollBar:vertical   { background: transparent; width: 8px; margin: 4px 2px; }
QScrollBar:horizontal { background: transparent; height: 8px; margin: 2px 4px; }
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #3a4060; border-radius: 4px; min-height: 20px; min-width: 20px;
}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover { background: #4a90d9; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical   { height: 0; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Tooltips ── */
QToolTip {
    background-color: #24283b;
    color: #c0caf5;
    border: 1px solid #4a90d9;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 13px;
}

/* ── Diálogos ── */
QMessageBox        { background-color: #1a1b26; }
QMessageBox QLabel { color: #c0caf5; font-size: 14px; }

/* ── Labels ── */
QLabel { background: transparent; }
"""
