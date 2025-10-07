#!/usr/bin/env python3
"""
Script para ejecutar tests del convertidor INE
"""

import unittest
import sys
import os


def run_tests():
    """Ejecutar tests unitarios"""
    print("Ejecutando tests unitarios...")

    try:
        # Ejecutar tests directamente
        sys.path.insert(0, 'tests')
        sys.path.insert(0, 'src')
        import test_converter
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_converter)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("Todos los tests pasaron exitosamente!")
            return True
        else:
            print("Algunos tests fallaron")
            return False

    except Exception as e:
        print(f"Error ejecutando tests: {e}")
        return False


def main():
    """Función principal"""
    print("Ejecutando tests del proyecto...")

    if run_tests():
        print("\nTodos los tests completados exitosamente!")
    else:
        print("\nLos tests fallaron")
        sys.exit(1)


if __name__ == "__main__":
    main()
