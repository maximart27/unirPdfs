"""Widgets reutilizables compartidos entre pestañas."""

from PyQt5.QtWidgets import QPushButton, QListWidget, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QBrush

from ui.style import HIGHLIGHT_COLOR, NORMAL_BG


def make_btn(text: str, role: str = 'default', tooltip: str = '') -> QPushButton:
    """Crea un QPushButton con rol visual y tooltip opcionales."""
    btn = QPushButton(text)
    if role != 'default':
        btn.setProperty('role', role)
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


class FileListWidget(QListWidget):
    """
    Lista de archivos PDF para la pestaña Unir PDFs.
    Acepta drag & drop de archivos desde el explorador y reordenación interna.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setToolTip(
            'Arrastra archivos PDF aquí desde el explorador.\n'
            'También puedes reordenarlos arrastrando dentro de la lista.'
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toString().lower().endswith('.pdf'):
                    self.addItem(str(url.toLocalFile()))
        else:
            super().dropEvent(event)


class PageThumbnailList(QListWidget):
    """
    Grid de miniaturas de páginas PDF con drag & drop explícito:
    - Arrastras página A sobre página B → A ocupa la posición de B.
    - El destino se resalta en azul mientras arrastras.
    - Emite orderChanged tras cada movimiento.
    """
    orderChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(120, 155))
        self.setResizeMode(QListWidget.Adjust)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSpacing(8)
        self.setMinimumHeight(300)
        self.setToolTip('Arrastra una miniatura encima de otra para cambiarla de posición')
        self.setStyleSheet("""
            QListWidget {
                background-color: #1e2030;
                border: 1px solid #2f3349;
                border-radius: 8px;
            }
            QListWidget::item {
                color: #a9b1d6;
                font-size: 12px;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #2a3a5a;
                border: 2px solid #4a90d9;
                color: #7dc4e4;
            }
            QListWidget::item:hover:!selected {
                background-color: #24283b;
                border: 1px solid #3a4060;
            }
        """)
        self._highlighted  = None
        self._drag_src_row = -1

    def _clear_highlight(self):
        if self._highlighted is not None:
            self._highlighted.setBackground(QBrush(NORMAL_BG))
            self._highlighted = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        self._drag_src_row = self.row(item) if item else -1
        super().mousePressEvent(event)

    def dragMoveEvent(self, event):
        self._clear_highlight()
        target = self.itemAt(event.pos())
        if target is not None and self._drag_src_row >= 0:
            if self.row(target) != self._drag_src_row:
                target.setBackground(QBrush(HIGHLIGHT_COLOR))
                self._highlighted = target
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def dragLeaveEvent(self, event):
        self._clear_highlight()
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self._clear_highlight()
        if event.source() is not self or self._drag_src_row < 0:
            event.ignore()
            return

        target   = self.itemAt(event.pos())
        from_idx = self._drag_src_row
        to_idx   = self.row(target) if target is not None else self.count() - 1
        self._drag_src_row = -1

        if from_idx != to_idx:
            item = self.takeItem(from_idx)
            self.insertItem(to_idx, item)
            self.setCurrentItem(item)
            self.orderChanged.emit()

        event.accept()
