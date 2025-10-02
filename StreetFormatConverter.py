import os
import tkinter as tk
from tkinter import filedialog, messagebox

def verificar_linea(linea, num_linea):
    # Asegura que el formato del fichero de entrada sea el correcto
    errores = []
    # Los ficheros a partir de julio de 2025 tienen por lo menos 132 caracteres
    if len(linea) < 132:
        errores.append(f"Línea {num_linea}: longitud insuficiente ({len(linea)})")
        return errores
    # Comprobar que estos campos sean numéricos
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

def convertir_fichero_vias(fichero_nuevo, fichero_salida):
    errores = []
    with open(fichero_nuevo, "r", encoding="utf-8") as fin, \
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
            # vector = linea[132:152]  # ignorado si existe

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

    return errores

def main():
    # Crear ventana oculta para Tkinter
    root = tk.Tk()
    root.withdraw()

    # Selección de archivo de entrada
    fichero_entrada = filedialog.askopenfilename(
        title="Selecciona el fichero de VIAS de formato nuevo (a partir de julio de 2025) en .txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not fichero_entrada:
        return  # Cancelado por el usuario

    base, ext = os.path.splitext(fichero_entrada)
    fichero_salida = base + "_convertido.txt"

    errores = convertir_fichero_vias(fichero_entrada, fichero_salida)

    if errores:
        mensaje = "Se encontraron errores en el fichero:\n\n" + "\n".join(errores[:10])
        if len(errores) > 10:
            mensaje += f"\n... y {len(errores) - 10} más."
        messagebox.showwarning("Verificación con errores", mensaje)
    else:
        messagebox.showinfo("Conversión completada",
                            f"El fichero se ha convertido correctamente.\n\n"
                            f"Fichero generado:\n{fichero_salida}")

if __name__ == "__main__":
    main()
