"""Lógica de negocio: renderizado de miniaturas y guardado de PDFs reordenados."""

import pymupdf as fitz  # PyMuPDF (evita conflicto con paquete 'fitz' abandonado)
from PyQt5.QtGui import QIcon, QPixmap, QImage


def render_icon(path: str, page_idx: int, scale: float = 0.35) -> QIcon:
    """
    Renderiza la página *page_idx* del PDF *path* como QIcon.

    Args:
        path:      ruta al archivo PDF.
        page_idx:  índice de página (base 0).
        scale:     factor de escala para la miniatura.

    Returns:
        QIcon con la imagen renderizada.
    """
    doc  = fitz.open(path)
    pix  = doc[page_idx].get_pixmap(matrix=fitz.Matrix(scale, scale))
    qimg = QImage.fromData(pix.tobytes('png'))
    doc.close()
    return QIcon(QPixmap.fromImage(qimg))


def save_reordered(page_order: list[tuple[str, int]], output_path: str) -> None:
    """
    Crea un nuevo PDF combinando las páginas indicadas en *page_order* y lo
    guarda en *output_path*.

    Args:
        page_order:   lista de tuplas (ruta_pdf, índice_página).
        output_path:  ruta de destino del PDF generado.

    Raises:
        Exception: cualquier error de lectura/escritura se propaga al caller.
    """
    new_doc = fitz.open()
    for pdf_path, page_idx in page_order:
        src = fitz.open(pdf_path)
        new_doc.insert_pdf(src, from_page=page_idx, to_page=page_idx)
        src.close()
    new_doc.save(output_path)
    new_doc.close()
