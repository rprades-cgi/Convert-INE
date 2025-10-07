# Convertidor INE - Formato de Vías

Convertidor de archivos de vías del INE de formato nuevo a formato antiguo.

## Características

- Conversión automática de formato INE nuevo a formato antiguo
- Detección automática de codificación de archivos
- Interfaz gráfica intuitiva con barra de progreso
- Validación de formato con reporte de errores

## Requisitos

- Python 3.8+
- Windows (para ejecutables)

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar aplicación
```bash
python src/StreetFormatConverter.py
```

### Construir ejecutable
```bash
python scripts/build.py
```

### Ejecutar tests
```bash
python scripts/run_tests.py
```

### Crear paquete de distribución
```bash
python scripts/create_distribution.py
```

## Instrucciones de uso

1. Seleccionar archivo INE (formato `VIAS.P02.*` o similar)
2. El archivo de salida se genera automáticamente
3. Hacer clic en "Convertir" para iniciar el proceso
4. Revisar el log para ver errores o confirmación de éxito

## Estructura del proyecto

```
src/
├── StreetFormatConverter.py # Punto de entrada principal
├── converter_core.py        # Lógica de conversión
└── gui.py                   # Interfaz gráfica

scripts/
├── build.py                 # Construcción de ejecutable
├── run_tests.py            # Ejecutor de tests
├── create_distribution.py  # Creación de paquetes
└── setup.py                # Configuración de cx_Freeze

tests/
└── test_converter.py       # Tests unitarios
```

## Formatos soportados

- **Entrada**: Archivos INE con formato `VIAS.P02.*` o `VIAS.P28.*`
- **Salida**: Archivo de texto plano con formato legacy
- **Codificaciones**: UTF-8, CP1252, Latin-1, ISO-8859-1