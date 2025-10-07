"""
Módulo central con la lógica de conversión del convertidor INE
"""

import os
import chardet


def verificar_linea(linea, num_linea):
    """Verificar formato de línea"""
    errores = []
    
    if len(linea) < 132:
        errores.append(f"Línea {num_linea}: longitud insuficiente ({len(linea)})")
        return errores
        
    # Verificar campos numéricos
    cpro = linea[0:2]
    cmun = linea[2:5]
    cvia = linea[5:10]
    fvar = linea[38:46]
    
    if not cpro.isdigit():
        errores.append(f"Línea {num_linea}: CPRO no numérico → '{cpro}'")
    if not cmun.isdigit():
        errores.append(f"Línea {num_linea}: CMUN no numérico → '{cmun}'")
    if not cvia.isdigit():
        errores.append(f"Línea {num_linea}: CVIA no numérico → '{cvia}'")
    if not fvar.isdigit():
        errores.append(f"Línea {num_linea}: FVAR no numérico → '{fvar}'")
        
    return errores


def detectar_codificacion(fichero):
    """Detectar la codificación del archivo"""
    try:
        with open(fichero, 'rb') as f:
            raw_data = f.read(10000)  # Leer primeros 10KB
            result = chardet.detect(raw_data)
            return result['encoding']
    except:
        return 'utf-8'  # Fallback

def convertir_fichero_vias(fichero_nuevo, fichero_salida, callback_progreso=None, callback_log=None):
    """Convertir fichero de vías"""
    errores = []
    lineas_procesadas = 0
    lineas_totales = 0
    
    # Detectar codificación
    encoding = detectar_codificacion(fichero_nuevo)
    if callback_log:
        callback_log(f"Codificación detectada: {encoding}")
    
    # Contar líneas totales
    try:
        with open(fichero_nuevo, "r", encoding=encoding) as f:
            lineas_totales = sum(1 for _ in f)
    except UnicodeDecodeError as e:
        if callback_log:
            callback_log(f"Error de codificación: {e}")
        # Intentar con codificaciones alternativas
        for alt_encoding in ['cp1252', 'latin-1', 'iso-8859-1']:
            try:
                with open(fichero_nuevo, "r", encoding=alt_encoding) as f:
                    lineas_totales = sum(1 for _ in f)
                encoding = alt_encoding
                if callback_log:
                    callback_log(f"Usando codificación alternativa: {alt_encoding}")
                break
            except:
                continue
        else:
            errores.append("No se pudo determinar la codificación del archivo")
            return errores
    
    try:
        with open(fichero_nuevo, "r", encoding=encoding) as fin, \
             open(fichero_salida, "w", encoding="utf-8") as fout:
            
            for i, linea in enumerate(fin, start=1):
                linea = linea.rstrip("\n")
                
                # Verificación de formato
                errores.extend(verificar_linea(linea, i))
                
                # Mapear campos del formato NUEVO
                cpro   = linea[0:2]
                cmun   = linea[2:5]
                cvia   = linea[5:10]
                aviac  = linea[10:35]  # no se usa en el formato antiguo
                fvar   = linea[38:46]
                cvia2  = linea[47:52]
                tvia   = linea[52:57]
                nvia   = linea[57:107]
                nviac  = linea[107:132]
                
                # Formato ANTIGUO
                out = ""
                out += cpro.ljust(2)      # CPRO N(2)
                out += cmun.ljust(3)      # CMUN N(3)
                out += cvia.ljust(5)      # CVIA N(5)
                out += " "                # TIPOINF A(1) -> espacio
                out += "  "               # CDEV A(2) -> espacios
                out += fvar.ljust(8)      # FVAR N(8)
                out += " "                # CVAR A(1) -> espacio
                out += cvia2.ljust(5)     # CVIA N(5)
                out += tvia.ljust(5)      # TVIA A(5)
                out += "0"                # POS N(1) -> '0'
                out += nvia.ljust(50)       # NVIA A(50)
                out += nviac.ljust(25)     # NVIAC A(25)
                
                fout.write(out + "\n")
                lineas_procesadas += 1
                
                # Callback de progreso si se proporciona
                if callback_progreso:
                    callback_progreso(lineas_procesadas, lineas_totales)
    
    except Exception as e:
        if callback_log:
            callback_log(f"Error durante la conversión: {e}")
        errores.append(f"Error durante la conversión: {e}")
    
    return errores
