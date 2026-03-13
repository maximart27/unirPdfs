"""Pestaña 'Unir PDFs'."""

import os

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QApplication
)

from core.pdf_merge import merge_pdfs
from ui.widgets import FileListWidget, make_btn


class MergeTab(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Fila: ruta de salida
        output_row = QHBoxLayout()
        output_row.setSpacing(8)
        self.output_file = QLineEdit()
        self.output_file.setPlaceholderText('Ruta del archivo PDF resultante...')
        self.output_file.setReadOnly(True)
        self.output_file.setToolTip('Ruta donde se guardará el PDF final unido')
        self.btn_save_to = make_btn('Guardar en', 'primary',
                                    'Selecciona dónde guardar el PDF resultante')
        self.btn_save_to.clicked.connect(self._choose_save_path)
        output_row.addWidget(self.output_file)
        output_row.addWidget(self.btn_save_to)

        # Instrucción
        hint = QLabel('Arrastra PDFs a la lista o usa el botón. '
                      'Reordénalos arrastrando. Pulsa Unir cuando estén listos.')
        hint.setStyleSheet('color: #6b7099; font-size: 13px; padding: 2px 0;')
        hint.setWordWrap(True)

        # Lista de archivos
        self.pdf_list = FileListWidget(self)

        # Botones de acción
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_delete = make_btn('Eliminar', 'danger',
                                   'Elimina los archivos seleccionados de la lista\n'
                                   '(no borra el archivo del disco)')
        self.btn_delete.clicked.connect(self._delete_selected)
        self.btn_merge = make_btn('Unir PDFs', 'primary',
                                  'Une todos los PDFs de la lista en el orden mostrado')
        self.btn_merge.clicked.connect(self._merge)
        self.btn_reset = make_btn('Limpiar', 'ghost',
                                  'Vacía la lista y borra la ruta de salida')
        self.btn_reset.clicked.connect(self._clear_all)
        self.btn_close = make_btn('Cerrar', 'ghost', 'Cierra la aplicación')
        self.btn_close.clicked.connect(QApplication.quit)

        btn_row.addWidget(self.btn_delete)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_merge)
        btn_row.addWidget(self.btn_reset)
        btn_row.addWidget(self.btn_close)

        layout.addLayout(output_row)
        layout.addWidget(hint)
        layout.addWidget(self.pdf_list)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    # ---------------------------------------------------------------- slots --

    def _choose_save_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self, 'Guardar PDF', os.getcwd(), 'PDF (*.pdf)')
        if path:
            self.output_file.setText(path)

    def _delete_selected(self):
        for item in self.pdf_list.selectedItems():
            self.pdf_list.takeItem(self.pdf_list.row(item))

    def _clear_all(self):
        self.pdf_list.clear()
        self.output_file.clear()

    def _merge(self):
        if not self.output_file.text():
            self._choose_save_path()
            if not self.output_file.text():
                return
        if self.pdf_list.count() == 0:
            QMessageBox.warning(self, 'PDF Manager', 'La lista está vacía.')
            return
        paths = [self.pdf_list.item(i).text() for i in range(self.pdf_list.count())]
        try:
            merge_pdfs(paths, self.output_file.text())
            self.pdf_list.clear()
            QMessageBox.information(self, 'PDF Manager', 'PDFs unidos correctamente.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
