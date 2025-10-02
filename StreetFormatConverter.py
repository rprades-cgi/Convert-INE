def convertir_fichero_vias(fichero_nuevo, fichero_salida):
    """
    Convierte el fichero de vías del formato nuevo (INE) al formato antiguo.
    Ambos ficheros son de ancho fijo en texto plano.
    """
    with open(fichero_nuevo, "r", encoding="utf-8") as fin, \
         open(fichero_salida, "w", encoding="utf-8") as fout:
        
        for linea in fin:
            # Cortar campos según las longitudes del formato NUEVO
            cpro   = linea[0:2]
            cmun   = linea[2:5]
            cvia   = linea[5:10]
            aviac  = linea[10:35]
            tipoinf= linea[35:36]
            cdev   = linea[36:38]
            fvar   = linea[38:46]
            cvar   = linea[46:47]
            cvia2  = linea[47:52]
            tvia   = linea[52:57]
            nvia   = linea[57:107]
            nviac  = linea[107:132]
            # vector = linea[132:152]  # ignorado

            # Formato ANTIGUO (respetando posiciones y longitudes)
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
            out += nvia.ljust(50)     # NVIA A(50)
            out += nviac.ljust(25)    # NVIAC A(25)

            fout.write(out + "\n")


# Ejemplo de uso
convertir_fichero_vias("formato nuevo.txt", "formato antiguo_salida.txt")
