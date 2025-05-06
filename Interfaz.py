from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
import AnalizadorLexico as analizador
import AnalizadorSintactico

ruta_archivo_actual = None

ventana = tk.Tk()
ventana.title("Analizador Léxico")
ventana.geometry("1000x700")

# Crear imagen de fondo con texto usando PIL
fuente = ImageFont.truetype("MiFuente.otf", 42)
imagen = Image.new("RGB", (1300, 700), color="#ffe2a3")
dibujo = ImageDraw.Draw(imagen)
dibujo.text((500, 10), "Analizador Lexico", font=fuente, fill="#ff6e61")

imagen_tk = ImageTk.PhotoImage(imagen)

# Mostrar imagen de fondo con label y enviar al fondo
fondo = tk.Label(ventana, image=imagen_tk)
fondo.place(x=0, y=0, relwidth=1, relheight=1)
fondo.lower()  # Enviar al fondo

# Crear widgets encima de la imagen
entrada = tk.Text(ventana, height=10, width=100, bg="#ffe6d1", fg="#2c3e50", insertbackground="black")
entrada.place(x=100, y=100)
entrada.config(state=tk.DISABLED)

resultado = tk.Text(ventana, height=10, width=100, bg="#ffe6d1", fg="#2c3e50")
resultado.place(x=100, y=320)

def ejecutar_analisis():
    global ruta_archivo_actual
    entrada.config(state=tk.NORMAL)
    codigo = entrada.get("1.0", tk.END)
    entrada.config(state=tk.DISABLED)
    resultado_analisis = analizador.analizar_codigo(codigo)
    
    if ruta_archivo_actual:
        resultado_sintactico = AnalizadorSintactico.analizar_cpp_palabra_a_palabra(ruta_archivo_actual)
    else:
        resultado_sintactico = "No se ha cargado ningún archivo para análisis sintáctico."              

    resultado.config(state=tk.NORMAL)
    resultado.delete("1.0", tk.END)
    #resultado.insert(tk.END, "Resultado Léxico:\n")
    #resultado.insert(tk.END, resultado_analisis + "\n\n")
    resultado.insert(tk.END, "Resultado Sintáctico:\n")
    resultado.insert(tk.END, resultado_sintactico)
    resultado.config(state=tk.DISABLED)


def cargar_archivo():
    global ruta_archivo_actual
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos C/C++", "*.c *.cpp")],
        defaultextension=".c"
    )
    if archivo:
        ruta_archivo_actual = archivo  # Guarda la ruta aquí
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            entrada.config(state=tk.NORMAL)
            entrada.delete("1.0", tk.END)
            entrada.insert(tk.END, contenido)
            entrada.config(state=tk.DISABLED)
            boton_analizar.config(state=tk.NORMAL)

boton_cargar = tk.Button(ventana, text="Cargar", bg="#ffbaa3", fg="white", font=("Consolas", 14), command=cargar_archivo)
boton_cargar.place(x=100, y=600)

boton_analizar = tk.Button(
    ventana, text="Analizar", bg="#ff9b80", fg="white",
    font=("Consolas", 14), command=ejecutar_analisis, state=tk.DISABLED
)
boton_analizar.place(x=200, y=600)

ventana.mainloop()
