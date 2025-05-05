from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog
import AnalizadorLexico as analizador
import AnalizadorSintactico

ventana = tk.Tk()
ventana.title("Analizador Léxico")
ventana.geometry("1000x700")


# Crear imagen de fondo con texto usando PIL
fuente = ImageFont.truetype("MiFuente.otf", 42)
imagen = Image.new("RGB", (1300, 700), color="#FCFFE0")
dibujo = ImageDraw.Draw(imagen)
dibujo.text((500, 10), "Analizador Lexico", font=fuente, fill="#75A47F")

imagen_tk = ImageTk.PhotoImage(imagen)

# Mostrar imagen de fondo con label y enviar al fondo
fondo = tk.Label(ventana, image=imagen_tk)
fondo.place(x=0, y=0, relwidth=1, relheight=1)
fondo.lower()  # Enviar al fondo

# Crear widgets encima de la imagen
entrada = tk.Text(ventana, height=10, width=100, bg="#FFF8E8", fg="#2c3e50", insertbackground="black")
entrada.place(x=100, y=100)
entrada.config(state=tk.DISABLED)

resultado = tk.Text(ventana, height=10, width=100, bg="#F7EED3", fg="#2c3e50")
resultado.place(x=100, y=320)

def ejecutar_analisis():
    entrada.config(state=tk.NORMAL)
    codigo = entrada.get("1.0", tk.END)
    entrada.config(state=tk.DISABLED)
    resultado_analisis = analizador.analizar_codigo(codigo)
    AnalizadorSintactico.analizar_cpp_palabra_a_palabra("archivo.cpp")
    resultado.config(state=tk.NORMAL)
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, resultado_analisis)
    resultado.config(state=tk.DISABLED)


def cargar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos C/C++", "*.c *.cpp")],
        defaultextension=".c"
    )
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            entrada.config(state=tk.NORMAL)     # Habilitar para escribir
            entrada.delete("1.0", tk.END)
            entrada.insert(tk.END, contenido)
            entrada.config(state=tk.DISABLED)   # Deshabilitar de nuevo
            boton_analizar.config(state=tk.NORMAL) # Hablitiar boton de Analizar

boton_cargar = tk.Button(ventana, text="Cargar", bg="#F5DAD2", fg="black", font=("Consolas", 14), command=cargar_archivo)
boton_cargar.place(x=100, y=600)

boton_analizar = tk.Button(
    ventana, text="Analizar", bg="#BACD92", fg="white",
    font=("Consolas", 14), command=ejecutar_analisis, state=tk.DISABLED
)
boton_analizar.place(x=200, y=600)

ventana.mainloop()
