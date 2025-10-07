#!/usr/bin/env python3
"""
Script para construir el ejecutable del convertidor INE
"""

import os
import sys
import subprocess
import shutil


def clean_build():
    """Limpiar archivos de construcción anteriores"""
    print("Limpiando archivos de construcción anteriores...")
    
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Directorio {dir_name} eliminado")


def build_executable():
    """Construir ejecutable"""
    print("Construyendo ejecutable...")
    
    # Cambiar al directorio de scripts
    original_dir = os.getcwd()
    os.chdir('scripts')
    
    try:
        result = subprocess.run([
            sys.executable, 'setup.py', 'build'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Ejecutable construido exitosamente!")
            return True
        else:
            print("Error al construir ejecutable:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("El proceso tardó demasiado tiempo")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        os.chdir(original_dir)


def copy_to_dist():
    """Copiar ejecutable a dist/"""
    # Buscar el ejecutable en diferentes ubicaciones posibles
    possible_paths = [
        "build/exe.win-amd64-3.12/StreetFormatConverter.exe",
        "build/exe.win-amd64-3.11/StreetFormatConverter.exe",
        "build/exe.win-amd64-3.10/StreetFormatConverter.exe",
        "build/exe.win-amd64/StreetFormatConverter.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            os.makedirs("dist", exist_ok=True)
            shutil.copy2(path, "dist/")
            print("Ejecutable copiado a dist/")
            return True
    
    print("No se encontró el ejecutable construido")
    return False


def main():
    """Función principal"""
    print("Iniciando proceso de construcción...")
    
    # Limpiar
    clean_build()
    
    # Construir
    if build_executable():
        copy_to_dist()
        print("Proceso completado exitosamente!")
    else:
        print("Error en el proceso de construcción")


if __name__ == "__main__":
    main()

