import subprocess
from mutagen.mp4 import MP4, MP4FreeForm
import os

def reencode_video(input_path, output_path):
    """Re-encoda el video con parámetros HEVC 4:2:2 10-bit usando FFmpeg"""
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx265',          # Códec HEVC
        '-pix_fmt', 'yuv422p10le',   # 4:2:2 a 10 bits
        '-color_primaries', 'bt709',
        '-color_trc', 'bt709',
        '-colorspace', 'bt709',
        '-crf', '23',               # Calidad ajustable (18-28 recomendado)
        '-c:a', 'aac',              # Re-encodear audio para compatibilidad
        '-b:a', '192k',             # Bitrate de audio
        '-movflags', '+faststart',  # Para streaming
        '-y',                       # Sobrescribir
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en FFmpeg: {e.stderr.decode()}")
        raise

def verify_encoding(output_path):
    """Verifica que el encodeo cumpla con los parámetros técnicos requeridos"""
    print("🔍 Verificando parámetros técnicos...")
    expected = {
        'codec_name': 'hevc',
        'pix_fmt': 'yuv422p10le',
        'color_space': 'bt709',
        'color_primaries': 'bt709',
        'color_transfer': 'bt709'
    }
    
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,pix_fmt,color_space,color_primaries,color_transfer',
        '-of', 'default=noprint_wrappers=1',
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Mostrar reporte de verificación
    print("\n📋 Reporte de verificación:")
    print(result.stdout)
    
    # Validar cada parámetro
    for line in result.stdout.split('\n'):
        if '=' in line:
            key, value = line.strip().split('=')
            if key in expected and expected[key] != value:
                raise ValueError(f"❌ ERROR: {key} es '{value}' (debe ser '{expected[key]}')")

def update_metadata(file_path):
    """Actualiza metadatos técnicos preservando los originales"""
    video = MP4(file_path)
    
    # Si no existen etiquetas, se crean
    if video.tags is None:
        video.add_tags()
    
    # Actualizar directamente el objeto MP4Tags sin sobrescribirlo
    video.tags["\xa9too"] = ["HEVC h.265 4:2:2 10-bit"]
    video.tags["----:com.apple.quicktime:ChromaSubsampling"] = [MP4FreeForm(b'4:2:2')]
    video.tags["----:com.apple.quicktime:BitsPerComponent"] = [MP4FreeForm(b'10')]
    
    # Usar clave freeform personalizada para el perfil de color en lugar de "colr"
    video.tags["----:com.apple.quicktime:ColorProfile"] = [MP4FreeForm(bytes.fromhex('6E636C7801010101010100'))]
    
    video.save()

def main():
    original_file = "DJI_20250206165918_0257_D.MP4"
    temp_file = "TEMP_REENCODED.mp4"
    backup_file = original_file + ".bak"

    try:
        # 1. Crear copia de seguridad
        print(f"📂 Creando copia de seguridad: {backup_file}")
        os.rename(original_file, backup_file)
        
        # 2. Re-encodear video
        print("🔄 Re-encodendo video con HEVC 4:2:2 10-bit...")
        reencode_video(backup_file, temp_file)
        
        # 3. Verificar encodeo
        verify_encoding(temp_file)
        
        # 4. Actualizar metadatos
        print("📝 Actualizando metadatos técnicos...")
        update_metadata(temp_file)
        
        # 5. Reemplazar archivo original
        print(f"✅ ¡Proceso completado! Reemplazando archivo original")
        os.replace(temp_file, original_file)
        os.remove(backup_file)
        
    except Exception as e:
        # Restaurar estado original en caso de error
        print(f"\n❌ Error crítico: {str(e)}")
        if os.path.exists(backup_file):
            print("🔄 Restaurando archivo original desde copia de seguridad...")
            os.replace(backup_file, original_file)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise

if __name__ == "__main__":
    main()

