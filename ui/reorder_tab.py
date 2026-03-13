"""Pestaña 'Reordenar páginas'."""

import os

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt

from core.pdf_reorder import render_icon, save_reordered
from ui.widgets import PageThumbnailList, make_btn


class ReorderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self._icon_cache = {}   # {(path, page_idx): QIcon}
        self._undo_stack = []   # lista de estados [(path, idx), ...]
        self._undo_index = -1
        self._init_ui()

    # ------------------------------------------------------------------ UI --

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Fila: cargar PDFs
        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        self.input_label = QLineEdit()
        self.input_label.setPlaceholderText('Arrastra PDFs aquí o usa "Añadir PDFs"...')
        self.input_label.setReadOnly(True)
        self.input_label.setToolTip('Muestra los archivos PDF cargados actualmente')
        self.btn_open = make_btn('Añadir PDFs', 'primary',
                                 'Abre uno o varios PDFs para reordenar sus páginas.\n'
                                 'También puedes arrastrar archivos directamente a esta ventana.')
        self.btn_open.clicked.connect(self._open_pdfs)
        input_row.addWidget(self.input_label)
        input_row.addWidget(self.btn_open)

        # Instrucción
        hint = QLabel(
            '  Arrastra una miniatura encima de otra para moverla a esa posición  ·  '
            'Ctrl+Z deshacer  ·  Ctrl+Y rehacer'
        )
        hint.setStyleSheet(
            'color: #6b7099; font-size: 12px; '
            'background: #16172a; border-radius: 6px; padding: 6px 12px;'
        )
        hint.setWordWrap(True)

        # Grid de miniaturas
        self.page_list = PageThumbnailList()
        self.page_list.orderChanged.connect(self._on_order_changed)

        # Fila: eliminar páginas
        page_row = QHBoxLayout()
        page_row.setSpacing(8)
        self.btn_delete_pages = make_btn('Eliminar página(s)', 'danger',
                                         'Elimina las páginas seleccionadas del resultado final.\n'
                                         'Usa Ctrl+Z para recuperarlas.')
        self.btn_delete_pages.clicked.connect(self._delete_selected_pages)
        page_row.addWidget(self.btn_delete_pages)
        page_row.addStretch()

        # Fila: ruta de salida
        output_row = QHBoxLayout()
        output_row.setSpacing(8)
        self.output_file = QLineEdit()
        self.output_file.setPlaceholderText('Ruta del PDF de salida...')
        self.output_file.setReadOnly(True)
        self.output_file.setToolTip('Ruta donde se guardará el PDF con las páginas reordenadas')
        self.btn_save_to = make_btn('Guardar como...', 'primary',
                                    'Elige dónde guardar el PDF resultante')
        self.btn_save_to.clicked.connect(self._choose_save_path)
        output_row.addWidget(self.output_file)
        output_row.addWidget(self.btn_save_to)

        # Fila: acciones principales
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_undo  = make_btn('↩  Deshacer', 'ghost',
                                  'Deshace el último movimiento o eliminación  (Ctrl+Z)')
        self.btn_redo  = make_btn('↪  Rehacer',  'ghost',
                                  'Rehace la última acción deshecha  (Ctrl+Y)')
        self.btn_save  = make_btn('Guardar PDF', 'primary',
                                  'Guarda el PDF con el orden actual de páginas')
        self.btn_reset = make_btn('Volver al inicio', 'ghost',
                                  'Restaura el orden original de las páginas\n'
                                  'tal como estaban al cargar los archivos')
        self.btn_undo.clicked.connect(self.undo)
        self.btn_redo.clicked.connect(self.redo)
        self.btn_save.clicked.connect(self._save)
        self.btn_reset.clicked.connect(self._reset)

        btn_row.addWidget(self.btn_undo)
        btn_row.addWidget(self.btn_redo)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_reset)

        layout.addLayout(input_row)
        layout.addWidget(hint)
        layout.addWidget(self.page_list)
        layout.addLayout(page_row)
        layout.addLayout(output_row)
        layout.addLayout(btn_row)
        self.setLayout(layout)
        self._update_undo_buttons()

    # -------------------------------------------------------- Undo / Redo ---

    def _get_state(self) -> list:
        return [self.page_list.item(i).data(Qt.UserRole)
                for i in range(self.page_list.count())]

    def _push_state(self):
        state = self._get_state()
        self._undo_stack = self._undo_stack[:self._undo_index + 1]
        self._undo_stack.append(state)
        self._undo_index = len(self._undo_stack) - 1
        self._update_undo_buttons()

    def _restore_state(self, state: list):
        self.page_list.clear()
        for path, page_idx in state:
            icon = self._icon_cache.get((path, page_idx)) or render_icon(path, page_idx)
            self._icon_cache[(path, page_idx)] = icon
            fname = os.path.basename(path)
            item  = QListWidgetItem(icon, f'Pág. {page_idx + 1}')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            item.setData(Qt.UserRole, (path, page_idx))
            item.setToolTip(f'{fname}  –  página {page_idx + 1}')
            self.page_list.addItem(item)
        self._update_undo_buttons()

    def _on_order_changed(self):
        self._push_state()

    def _update_undo_buttons(self):
        self.btn_undo.setEnabled(self._undo_index > 0)
        self.btn_redo.setEnabled(self._undo_index < len(self._undo_stack) - 1)

    def undo(self):
        if self._undo_index > 0:
            self._undo_index -= 1
            self._restore_state(self._undo_stack[self._undo_index])

    def redo(self):
        if self._undo_index < len(self._undo_stack) - 1:
            self._undo_index += 1
            self._restore_state(self._undo_stack[self._undo_index])

    def keyPressEvent(self, event):
        mods, key = event.modifiers(), event.key()
        if key == Qt.Key_Z and mods == Qt.ControlModifier:
            self.undo()
        elif key == Qt.Key_Y and mods == Qt.ControlModifier:
            self.redo()
        elif key == Qt.Key_Z and mods == (Qt.ControlModifier | Qt.ShiftModifier):
            self.redo()
        else:
            super().keyPressEvent(event)

    # ---------------------------------------------------- Carga de PDFs ---

    def dragEnterEvent(self, event):
        event.accept() if event.mimeData().hasUrls() else event.ignore()

    def dropEvent(self, event):
        loaded = False
        for url in event.mimeData().urls():
            if url.isLocalFile() and url.toString().lower().endswith('.pdf'):
                self._load_pdf(str(url.toLocalFile()))
                loaded = True
        if loaded:
            self._push_state()

    def _open_pdfs(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, 'Abrir PDFs', os.getcwd(), 'PDF (*.pdf)')
        for path in paths:
            self._load_pdf(path)
        if paths:
            self._push_state()

    def _load_pdf(self, path: str):
        try:
            import pymupdf as fitz
            doc   = fitz.open(path)
            fname = os.path.basename(path)
            for i in range(len(doc)):
                icon = render_icon(path, i)
                self._icon_cache[(path, i)] = icon
                item = QListWidgetItem(icon, f'Pág. {i + 1}')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
                item.setData(Qt.UserRole, (path, i))
                item.setToolTip(f'{fname}  –  página {i + 1}')
                self.page_list.addItem(item)
            doc.close()
            loaded = sorted({os.path.basename(self.page_list.item(idx).data(Qt.UserRole)[0])
                             for idx in range(self.page_list.count())})
            self.input_label.setText(', '.join(loaded))
        except Exception as e:
            QMessageBox.critical(self, 'Error al cargar', str(e))

    # ---------------------------------------------------- Acciones ---

    def _delete_selected_pages(self):
        for item in self.page_list.selectedItems():
            self.page_list.takeItem(self.page_list.row(item))
        self._push_state()

    def _choose_save_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self, 'Guardar PDF', os.getcwd(), 'PDF (*.pdf)')
        if path:
            self.output_file.setText(path)

    def _save(self):
        if self.page_list.count() == 0:
            QMessageBox.warning(self, 'Aviso', 'No hay páginas para guardar.')
            return
        output = self.output_file.text()
        if not output:
            self._choose_save_path()
            output = self.output_file.text()
            if not output:
                return
        page_order = [self.page_list.item(i).data(Qt.UserRole)
                      for i in range(self.page_list.count())]
        try:
            save_reordered(page_order, output)
            QMessageBox.information(self, 'PDF Manager', 'PDF guardado correctamente.')
        except Exception as e:
            QMessageBox.critical(self, 'Error al guardar', str(e))

    def _reset(self):
        if self._undo_stack:
            self._undo_index = 0
            self._restore_state(self._undo_stack[0])
