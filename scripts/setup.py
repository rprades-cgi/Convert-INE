from cx_Freeze import setup, Executable
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configuration for creating executable
setup(
    name="ConvertidorINE",
    version="1.0.0",
    description="Convertidor de formato de archivos INE",
    author="Ruben Prades",
    executables=[Executable(
        "../src/StreetFormatConverter.py",
        base="Win32GUI",
        target_name="StreetFormatConverter.exe"
    )]
)

