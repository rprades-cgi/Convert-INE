"""
Tests unitarios para el convertidor INE
"""

import unittest
import os
import sys
import tempfile

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from converter_core import verificar_linea, convertir_fichero_vias


class TestStreetFormatConverter(unittest.TestCase):

    def test_verificar_linea_corta(self):
        """Test para una línea con longitud insuficiente"""
        linea = "01001000001AVENIDA DE LA PAZ"
        errores = verificar_linea(linea, 1)
        self.assertGreater(len(errores), 0)
        self.assertIn("longitud insuficiente", errores[0])

    def test_verificar_cpro_no_numerico(self):
        """Test para CPRO no numérico"""
        linea = "A1001000001AVENIDA DE LA PAZ                 202507010000100001CALLE DE LA PAZ                                                  PAZ                      " + " " * 20
        errores = verificar_linea(linea, 1)
        self.assertIn("CPRO no numérico", errores[0])

    def test_verificar_cmun_no_numerico(self):
        """Test para CMUN no numérico"""
        linea = "01A01000001AVENIDA DE LA PAZ                 202507010000100001CALLE DE LA PAZ                                                  PAZ                      " + " " * 20
        errores = verificar_linea(linea, 1)
        self.assertIn("CMUN no numérico", errores[0])

    def test_verificar_cvia_no_numerico(self):
        """Test para CVIA no numérico"""
        linea = "01001A00001AVENIDA DE LA PAZ                 202507010000100001CALLE DE LA PAZ                                                  PAZ                      " + " " * 20
        errores = verificar_linea(linea, 1)
        self.assertIn("CVIA no numérico", errores[0])

    def test_convertir_fichero_valido(self):
        """Test conversión de archivo válido"""
        # Crear archivo de prueba con líneas válidas
        test_content = "0100100001AVENIDA DE LA PAZ           20250701 0000100001CALLE DE LA PAZ                                   PAZ                      \n"
        test_content += "0200200002CALLE MAYOR                 20250701 0000200002AVENIDA MAYOR                                     MAYOR                    \n"
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as f:
            f.write(test_content)
            input_file = f.name
        
        output_file = input_file.replace('.txt', '_output.txt')
        
        try:
            errores = convertir_fichero_vias(input_file, output_file)
            
            # Verificar que no hay errores
            self.assertEqual(len(errores), 0)
            
            # Verificar que el archivo de salida existe
            self.assertTrue(os.path.exists(output_file))
            
            # Verificar contenido del archivo de salida
            with open(output_file, 'r', encoding='utf-8') as f:
                output_content = f.read()
                self.assertIn("0100100001", output_content)
                self.assertIn("0200200002", output_content)
        finally:
            for file_path in [input_file, output_file]:
                if os.path.exists(file_path):
                    os.unlink(file_path)


if __name__ == '__main__':
    unittest.main()