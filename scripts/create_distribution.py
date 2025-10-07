#!/usr/bin/env python3
"""
Script para crear paquete de distribución
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_distribution():
    """Crear paquete de distribución"""
    print("Creando paquete de distribucion...")
    
    # Directorio de distribución
    dist_dir = Path("dist/ConvertidorINE")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Directorio fuente del ejecutable
    source_dir = Path("scripts/build/exe.win-amd64-3.12")
    
    if not source_dir.exists():
        print("Error: No se encontro el ejecutable. Ejecuta primero: python scripts/build.py")
        return False
    
    # Copiar archivos necesarios
    files_to_copy = [
        "StreetFormatConverter.exe",
        "python312.dll",
        "lib/",
        "share/"
    ]
    
    for item in files_to_copy:
        src = source_dir / item
        dst = dist_dir / item
        
        if src.is_file():
            shutil.copy2(src, dst)
            print(f"Copiado: {item}")
        elif src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copiado directorio: {item}")
    
    # Crear README para el usuario
    readme_content = """INSTRUCCIONES DE USO

1. Descomprimir el archivo ConvertidorINE_Portable.zip
2. Entrar en la carpeta ConvertidorINE
3. Ejecutar StreetFormatConverter.exe
4. Seleccionar archivo INE (formato VIAS.P02.* o similar)
5. Hacer clic en "Convertir Fichero"
6. El archivo convertido se genera automáticamente

FORMATOS SOPORTADOS:
- VIAS.*
- *.txt

NOTAS:
- No requiere instalación
- Funciona en Windows
- Detecta automáticamente la codificación del archivo
"""
    
    with open(dist_dir / "README_USUARIO.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\nPaquete de distribucion creado en: {dist_dir}")
    print("Contenido:")
    for item in dist_dir.rglob("*"):
        if item.is_file():
            print(f"   {item.relative_to(dist_dir)}")
    
    # Crear ZIP
    zip_path = "dist/ConvertidorINE_Portable.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_dir)
                zipf.write(file_path, arcname)
    
    print(f"\nArchivo ZIP creado: {zip_path}")
    print("Para distribuir: Enviar el archivo ZIP a tus compañeros")
    return True

if __name__ == "__main__":
    create_distribution()


