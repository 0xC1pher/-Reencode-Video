# Reencode Video Script

Este script automatiza el proceso de re-encodeo de un video utilizando FFmpeg con parámetros específicos de codificación HEVC 4:2:2 a 10 bits. Además, verifica que el video resultante cumple con ciertos parámetros técnicos y actualiza sus metadatos para reflejar la transformación realizada. En caso de error durante el proceso, se restaura el archivo original utilizando una copia de seguridad.

## Características

- **Copia de Seguridad:** Renombra el archivo original para crear una copia de respaldo.
- **Re-Encodeo con FFmpeg:** Convierte el video al códec HEVC (H.265) con pixel format `yuv422p10le` (4:2:2 a 10 bits) y configura parámetros de color BT.709.
- **Verificación Técnica:** Utiliza FFprobe para validar que los parámetros del video re-encodeado coinciden con los requeridos.
- **Actualización de Metadatos:** Emplea la librería [mutagen](https://mutagen.readthedocs.io/en/latest/) para modificar y actualizar metadatos en el archivo MP4 sin sobreescribir otros datos importantes.
- **Restauración en Caso de Error:** Si ocurre algún fallo a lo largo del proceso, se restaura el archivo original a partir de la copia de seguridad.

## Requisitos

- Python 3.x
- FFmpeg instalado y accesible en el PATH del sistema.
- FFprobe (usualmente incluido con FFmpeg).
- La librería `mutagen` para Python.

## Instalación

1. **Instalar FFmpeg y FFprobe**  
   Dependiendo de tu sistema operativo, puedes utilizar:

   - **En Ubuntu/Debian:**
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

   - **En macOS (usando Homebrew):**
     ```bash
     brew install ffmpeg
     ```

2. **Instalar dependencias de Python:**
   ```bash
   pip install mutagen
