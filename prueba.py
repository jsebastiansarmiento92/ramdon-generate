import tkinter as tk
from tkinter import filedialog, messagebox
import math
import numpy as np
from collections import Counter

# ====================== Implementación de las pruebas ======================

def prueba_medias(numeros, alpha=0.05):
    n = len(numeros)
    media_observada = np.mean(numeros)
    media_esperada = 0.5
    z0 = (media_observada - media_esperada) * math.sqrt(n) / math.sqrt(1/12)
    
    z_alpha = abs(np.percentile(np.random.normal(0, 1, 100000), [alpha * 100 / 2])[0])

    if -z_alpha <= z0 <= z_alpha:
        return f"Aceptar la hipótesis nula (media = 0.5), z0 = {z0:.4f}"
    else:
        return f"Rechazar la hipótesis nula, z0 = {z0:.4f}"

def prueba_varianza(numeros, alpha=0.05):
    n = len(numeros)
    var_observada = np.var(numeros, ddof=1)
    var_esperada = 1 / 12
    
    chi2_obs = (n - 1) * var_observada / var_esperada
    chi2_alpha_inf = np.percentile(np.random.chisquare(n-1, 100000), alpha * 100 / 2)
    chi2_alpha_sup = np.percentile(np.random.chisquare(n-1, 100000), (1 - alpha / 2) * 100)

    if chi2_alpha_inf <= chi2_obs <= chi2_alpha_sup:
        return f"Aceptar la hipótesis nula (varianza = 1/12), Chi2 observado = {chi2_obs:.4f}"
    else:
        return f"Rechazar la hipótesis nula, Chi2 observado = {chi2_obs:.4f}"

def prueba_ks(numeros, alpha=0.05):
    n = len(numeros)
    numeros_ordenados = np.sort(numeros)
    d_max = 0

    for i in range(n):
        f_observada = (i + 1) / n  # Distribución acumulada observada
        f_teorica = numeros_ordenados[i]  # Distribución teórica (uniforme [0,1])
        d1 = abs(f_observada - f_teorica)
        d2 = abs(f_teorica - i / n)
        d_max = max(d_max, d1, d2)

    d_alpha = 1.36 / math.sqrt(n)  # Valor crítico aproximado para alpha=0.05

    if d_max < d_alpha:
        return f"Aceptar la hipótesis nula (Distribución = Uniforme[0,1]), D_max = {d_max:.4f}"
    else:
        return f"Rechazar la hipótesis nula, D_max = {d_max:.4f}"

def prueba_chi2(numeros, num_intervalos=10, alpha=0.05):
    n = len(numeros)
    frecuencias_observadas, _ = np.histogram(numeros, bins=num_intervalos)
    frecuencias_esperadas = n / num_intervalos

    chi2_obs = sum(((frecuencia - frecuencias_esperadas) ** 2) / frecuencias_esperadas for frecuencia in frecuencias_observadas)
    chi2_alpha = np.percentile(np.random.chisquare(num_intervalos-1, 100000), (1-alpha)*100)

    if chi2_obs < chi2_alpha:
        return f"Aceptar la hipótesis nula (Distribución uniforme), Chi2 observado = {chi2_obs:.4f}"
    else:
        return f"Rechazar la hipótesis nula, Chi2 observado = {chi2_obs:.4f}"


def prueba_poker(numeros, alpha=0.05):

    n = len(numeros)
    categorias = {
        "todos_diferentes": 0,
        "un_par": 0,
        "dos_pares": 0,
        "trio": 0,
        "full_house": 0,
        "poker": 0
    }
    
    # Clasificar los números en categorías basadas en los primeros 4 dígitos
    for num in numeros:
        num_str = f"{num:.4f}"[2:6]  # Usar los primeros 4 dígitos decimales
        conteo = Counter(num_str)
        valores = list(conteo.values())
        
        if valores.count(2) == 2:
            categorias["dos_pares"] += 1
        elif 3 in valores and 2 in valores:
            categorias["full_house"] += 1
        elif 4 in valores:
            categorias["poker"] += 1
        elif 3 in valores:
            categorias["trio"] += 1
        elif 2 in valores:
            categorias["un_par"] += 1
        else:
            categorias["todos_diferentes"] += 1

    # Frecuencias esperadas para cada categoría (distribución uniforme)
    frecuencias_esperadas = {
        "todos_diferentes": 0.3024 * n,
        "un_par": 0.5040 * n,
        "dos_pares": 0.1080 * n,
        "trio": 0.0720 * n,
        "full_house": 0.0090 * n,
        "poker": 0.0045 * n
    }

    # Cálculo del estadístico Chi2
    chi2_obs = sum(((categorias[cat] - frecuencias_esperadas[cat]) ** 2) / frecuencias_esperadas[cat] for cat in categorias)
    chi2_alpha = np.percentile(np.random.chisquare(5, 100000), (1-alpha)*100)

    # Veredicto
    if chi2_obs < chi2_alpha:
        return f"Aceptar la hipótesis nula (Distribución uniforme), Chi2 observado = {chi2_obs:.4f}"
    else:
        return f"Rechazar la hipótesis nula, Chi2 observado = {chi2_obs:.4f}"
# ====================== Interfaz gráfica con Tkinter ======================

class GeneradorInterfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validación de Números Pseudoaleatorios")
        self.geometry("600x400")

        # Crear menú para cargar archivos
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Cargar archivo...", command=self.cargar_archivo)

        # Label y lista de números cargados
        self.label_archivo = tk.Label(self, text="Ningún archivo cargado", pady=10)
        self.label_archivo.pack()

        # Selección de prueba
        self.var_prueba = tk.StringVar(value="Prueba de Medias")
        tk.Radiobutton(self, text="Prueba de Medias", variable=self.var_prueba, value="Prueba de Medias").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Prueba de Varianza", variable=self.var_prueba, value="Prueba de Varianza").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Prueba KS", variable=self.var_prueba, value="Prueba KS").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Prueba Chi2", variable=self.var_prueba, value="Prueba Chi2").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Prueba de Póker", variable=self.var_prueba, value="Prueba de Póker").pack(anchor=tk.W)

        # Botón para ejecutar la prueba
        tk.Button(self, text="Ejecutar Prueba", command=self.ejecutar_prueba).pack(pady=20)

        # Resultado de la prueba
        self.resultados_texto = tk.Text(self, height=10, width=60)
        self.resultados_texto.pack()

        self.numeros = []

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            self.label_archivo.config(text=f"Archivo cargado: {archivo}")
            self.numeros = self.leer_numeros(archivo)

    def leer_numeros(self, archivo):
        try:
            with open(archivo, "r") as f:
                numeros = [float(linea.strip()) for linea in f]
            return numeros
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {e}")
            return []

    def ejecutar_prueba(self):
        if not self.numeros:
            messagebox.showerror("Error", "Primero debe cargar un archivo.")
            return

        prueba_seleccionada = self.var_prueba.get()

        if prueba_seleccionada == "Prueba de Medias":
            resultado = prueba_medias(self.numeros)
        elif prueba_seleccionada == "Prueba de Varianza":
            resultado = prueba_varianza(self.numeros)
        elif prueba_seleccionada == "Prueba KS":
            resultado = prueba_ks(self.numeros)
        elif prueba_seleccionada == "Prueba Chi2":
            resultado = prueba_chi2(self.numeros)
        elif prueba_seleccionada == "Prueba de Póker":
            resultado = prueba_poker(self.numeros) 
        else:
            resultado = "Prueba no implementada aún."

        self.resultados_texto.delete(1.0, tk.END)
        self.resultados_texto.insert(tk.END, resultado)

# Inicializa la interfaz
if __name__ == "__main__":
    app = GeneradorInterfaz()
    app.mainloop()
