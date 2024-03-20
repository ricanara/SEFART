import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from alfabeto import alfabeto

def buscar_archivo():
    nombre_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, nombre_archivo)

def procesar():
    archivo_entrada = entrada_archivo.get()
    if archivo_entrada:
        libro = readBook(archivo_entrada)
        resultados.delete(1.0, tk.END)  # Limpiar cualquier resultado anterior
        resultados_csv = []  # Lista para almacenar los resultados para el archivo CSV
        for linea in libro:
            for palabra in linea:
                gematria_decimal = calcular_gematria(palabra)
                gematria_binaria = '{:012b}'.format(gematria_decimal) if gematria_decimal else ''
                resultado_formateado = ""
                for bit in gematria_binaria:
                    if bit == '1':
                        resultado_formateado += "█"  # Cuadro negro para '1'
                    else:
                        resultado_formateado += " "  # Espacio en blanco para '0'
                # Copia espejo
                resultado_formateado_espejo = resultado_formateado[::-1]
                # Concatenar el resultado original y el espejo sin espacio adicional
                resultado_final = f"{gematria_decimal}: {palabra}: {resultado_formateado}{resultado_formateado_espejo}\n"
                resultados.insert(tk.END, resultado_final, 'right_align')
                resultados_csv.append([palabra, gematria_decimal, ','.join(gematria_binaria)])
        messagebox.showinfo("Éxito", "Procesamiento de Gematría completado exitosamente.")

        # Guardar los resultados en un archivo CSV
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
        if archivo_salida:
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Palabra", "Gematria Decimal", "Gematria Binaria"])
                writer.writerows(resultados_csv)
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo de entrada.")

def calcular_gematria(palabra):
    gematria = 0
    for caracter in palabra:
        if caracter in alfabeto:
            gematria += alfabeto[caracter]
    return gematria

def readBook(fn):
    with open(fn, 'r', encoding='utf-8') as fi:
        book_raw = filter(condi, fi.readlines())
    book = map(clean, book_raw)
    return book

def condi(s):
    return s[1] != 'x'

def clean(l):
    return l.split()[1:-1]

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("SEFART El Software Divino / By Alvaro Ricaurte")

# Configurar la expansión del área de texto junto con la ventana principal
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)

# Crear etiqueta y entrada para el archivo de entrada
etiqueta_entrada = tk.Label(ventana, text="Seleccione un libro de la Biblia:", font=("Arial", 14))
etiqueta_entrada.grid(row=0, column=0, padx=5, pady=5)
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.grid(row=0, column=1, padx=5, pady=5)
boton_buscar = tk.Button(ventana, text="Buscar", command=buscar_archivo)
boton_buscar.grid(row=0, column=2, padx=5, pady=5)

# Crear área de texto para mostrar los resultados
resultados = tk.Text(ventana, wrap='none')
resultados.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Crear barra de desplazamiento vertical
scrollbar = tk.Scrollbar(ventana, command=resultados.yview)
scrollbar.grid(row=1, column=3, sticky='ns')

# Asociar la barra de desplazamiento con el área de texto
resultados.config(yscrollcommand=scrollbar.set)

# Establecer justificación derecha
resultados.tag_configure('right_align', justify='right')

# Crear botón para procesar
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar)
boton_procesar.grid(row=2, column=1, padx=5, pady=5)

# Ejecutar el bucle de eventos principal
ventana.mainloop()
