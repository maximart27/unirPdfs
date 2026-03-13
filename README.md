# PDF Manager

**Autor:** Máximo Martínez

Aplicación de escritorio para gestionar archivos PDF: unirlos y reordenar sus páginas con una interfaz gráfica moderna.

---

## ¿Qué hace?

### Pestaña "Unir PDFs"
- Arrastra varios archivos PDF a la lista (o ábrelos con el botón)
- Reordénalos arrastrando dentro de la lista
- Pulsa **Unir PDFs** y elige dónde guardar el resultado

### Pestaña "Reordenar páginas"
- Abre uno o varios PDFs
- Verás todas sus páginas como miniaturas
- Arrastra una miniatura encima de otra para cambiarla de posición
- **Ctrl+Z** deshace el último movimiento, **Ctrl+Y** lo rehace
- **Volver al inicio** restaura el orden original
- Pulsa **Guardar PDF** cuando el orden sea el correcto

---

## Requisitos

- Python 3.10 o superior
- Las dependencias del proyecto (ver más abajo)

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd unirPdfs

# 2. Crear el entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install PyQt5 PyPDF2 pymupdf pyinstaller

# 4. Ejecutar
python main.py
```

---

## Estructura del proyecto

```
main.py                 → Entry point, arranca la aplicación
pdf_manager.spec        → Configuración para generar el ejecutable
│
├── ui/                 → Interfaz gráfica
│   ├── style.py        → Tema visual (colores, fuentes, estilos)
│   ├── widgets.py      → Widgets reutilizables (lista de archivos, grid de miniaturas)
│   ├── merge_tab.py    → Pestaña "Unir PDFs"
│   └── reorder_tab.py  → Pestaña "Reordenar páginas"
│
└── core/               → Lógica de negocio (sin UI)
    ├── pdf_merge.py    → Función que une múltiples PDFs en uno
    └── pdf_reorder.py  → Funciones para renderizar miniaturas y guardar PDFs reordenados
```

**¿Por qué esta separación?**
- `core/` no sabe nada de la interfaz gráfica — solo trabaja con archivos PDF
- `ui/` no sabe nada de PyMuPDF ni PyPDF2 — solo dibuja y llama a `core/`
- Si mañana quieres cambiar el aspecto visual, solo tocas `ui/style.py`
- Si quieres cambiar la librería de PDFs, solo tocas `core/`

---

## Generar un ejecutable

Usa el archivo `pdf_manager.spec` que ya está configurado para incluir todos los módulos y recursos necesarios.

### Linux / macOS

```bash
source venv/bin/activate
pip uninstall fitz              # elimina un paquete antiguo que causa conflictos
pip install --upgrade pymupdf pyinstaller
pyinstaller pdf_manager.spec
```

El ejecutable quedará en `dist/pdf-manager`.

### Windows

Mismos pasos pero ejecutados desde una terminal Windows (PowerShell o cmd):

```bat
venv\Scripts\activate
pip uninstall fitz
pip install --upgrade pymupdf pyinstaller
pyinstaller pdf_manager.spec
```

El ejecutable quedará en `dist\pdf-manager.exe`.

> **Importante:** PyInstaller no hace compilación cruzada.
> Para generar el `.exe` de Windows debes ejecutar el comando en Windows.
> Para el binario de Linux debes ejecutarlo en Linux.

### ¿Qué hace el archivo .spec?

`pdf_manager.spec` le dice a PyInstaller exactamente qué incluir en el ejecutable:

- `main.py` como punto de entrada
- Las carpetas `ui/` y `core/` con todos sus módulos
- El icono `PDF.ico`
- Todos los archivos internos de `pymupdf` (necesario porque PyInstaller no los detecta solo)
- `console=False` para que no aparezca una ventana de terminal al ejecutarlo

---

## Dependencias

| Paquete | Versión mínima | Para qué |
|---------|---------------|----------|
| PyQt5 | 5.15 | Interfaz gráfica |
| PyPDF2 | 3.0 | Unir PDFs |
| pymupdf | 1.25 | Renderizar miniaturas y reordenar páginas |
| pyinstaller | 6.0 | Generar el ejecutable (solo para distribuir) |
