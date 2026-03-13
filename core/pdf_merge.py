"""Lógica de negocio: unión de múltiples PDFs en uno."""

from PyPDF2 import PdfFileMerger


def merge_pdfs(input_paths: list[str], output_path: str) -> None:
    """
    Une los PDFs de *input_paths* en el orden dado y los guarda en *output_path*.

    Raises:
        Exception: cualquier error de lectura/escritura se propaga al caller.
    """
    merger = PdfFileMerger()
    for path in input_paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()
