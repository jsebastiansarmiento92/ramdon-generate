import tkinter as tk
from tkinter import messagebox
import math

class GeneradorCuadradosMedios:
    def __init__(self, semilla):
        self.estado = semilla

    def generar(self):
        cuadrado = str(self.estado ** 2).zfill(8)
        medio = cuadrado[len(cuadrado)//4:3*len(cuadrado)//4]
        self.estado = int(medio)
        return self.estado / 10000

class GeneradorCongruencialLineal:
    def __init__(self, semilla, a, c, m):
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m
        self.estado = semilla

    def generar_uniforme(self):
        self.estado = (self.a * self.estado + self.c) % self.m
        return self.estado / self.m

class DistribucionExponencial:
    def __init__(self, lambda_param, generador_uniforme):
        self.lambda_param = lambda_param
        self.generador_uniforme = generador_uniforme

    def generar(self, n):
        return [-math.log(1 - self.generador_uniforme.generar_uniforme()) / self.lambda_param for _ in range(n)]

class DistribucionNormal:
    def __init__(self, generador_uniforme):
        self.generador_uniforme = generador_uniforme

    def generar(self, n):
        numeros_normales = []
        for _ in range(n // 2):
            u1 = self.generador_uniforme.generar_uniforme()
            u2 = self.generador_uniforme.generar_uniforme()
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            numeros_normales.append(z1)
            numeros_normales.append(z2)
        return numeros_normales

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Números Pseudoaleatorios")
        self.geometry("400x700")
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Método de Generación").pack(pady=10)

        self.var_metodo = tk.StringVar(value="Cuadrados Medios")
        tk.Radiobutton(self, text="Cuadrados Medios", variable=self.var_metodo, value="Cuadrados Medios", command=self.actualizar_parametros).pack()
        tk.Radiobutton(self, text="Congruencial Lineal", variable=self.var_metodo, value="Congruencial Lineal", command=self.actualizar_parametros).pack()
        tk.Radiobutton(self, text="Distribución Uniforme", variable=self.var_metodo, value="Distribución Uniforme", command=self.actualizar_parametros).pack()
        tk.Radiobutton(self, text="Distribución Exponencial", variable=self.var_metodo, value="Distribución Exponencial", command=self.actualizar_parametros).pack()
        tk.Radiobutton(self, text="Distribución Normal", variable=self.var_metodo, value="Distribución Normal", command=self.actualizar_parametros).pack()

        tk.Label(self, text="Semilla (X0)").pack(pady=10)
        self.entrada_semilla = tk.Entry(self)
        self.entrada_semilla.pack()

        tk.Label(self, text="Cantidad de Números a Generar").pack(pady=10)
        self.entrada_cantidad = tk.Entry(self)
        self.entrada_cantidad.pack()

        self.label_a = tk.Label(self, text="Multiplicador (a) / Límite Inferior (a)")
        self.label_a.pack(pady=10)
        self.entrada_a = tk.Entry(self)
        self.entrada_a.pack()

        self.label_c = tk.Label(self, text="Incremento (c) / Límite Superior (b)")
        self.label_c.pack(pady=10)
        self.entrada_c = tk.Entry(self)
        self.entrada_c.pack()

        self.label_m = tk.Label(self, text="Módulo (m)")
        self.label_m.pack(pady=10)
        self.entrada_m = tk.Entry(self)
        self.entrada_m.pack()

        self.label_media = tk.Label(self, text="Media (solo para Distribución Normal)")
        self.label_media.pack(pady=10)
        self.entrada_media = tk.Entry(self)
        self.entrada_media.pack()

        self.label_desviacion = tk.Label(self, text="Desviación Estándar (solo para Distribución Normal)")
        self.label_desviacion.pack(pady=10)
        self.entrada_desviacion = tk.Entry(self)
        self.entrada_desviacion.pack()

        self.label_lambda = tk.Label(self, text="Lambda (solo para Exponencial)")
        self.label_lambda.pack(pady=10)
        self.entrada_lambda = tk.Entry(self)
        self.entrada_lambda.pack()

        tk.Button(self, text="Generar Números", command=self.generar_numeros).pack(pady=20)

        self.resultados_texto = tk.Text(self, height=10, width=40)
        self.resultados_texto.pack()

        self.actualizar_parametros()

    def actualizar_parametros(self):
        metodo = self.var_metodo.get()
        if metodo == "Congruencial Lineal":
            self.entrada_a.delete(0, tk.END)
            self.entrada_a.insert(0, "1664525")
            self.entrada_c.delete(0, tk.END)
            self.entrada_c.insert(0, "1013904223")
            self.entrada_m.delete(0, tk.END)
            self.entrada_m.insert(0, str(2**32))
            self.label_a.config(text="Multiplicador (a)")
            self.label_c.config(text="Incremento (c)")
            self.label_m.config(text="Módulo (m)")

            self.label_media.pack_forget()
            self.entrada_media.pack_forget()
            self.label_desviacion.pack_forget()
            self.entrada_desviacion.pack_forget()
            self.label_lambda.pack_forget()
            self.entrada_lambda.pack_forget()

        elif metodo == "Distribución Uniforme":
            self.entrada_a.delete(0, tk.END)
            self.entrada_a.insert(0, "0") 
            self.entrada_c.delete(0, tk.END)
            self.entrada_c.insert(0, "1")  
            self.entrada_m.delete(0, tk.END)
            self.entrada_m.config(state=tk.DISABLED)  
            self.label_a.config(text="Límite Inferior (a)")
            self.label_c.config(text="Límite Superior (b)")
            self.label_m.config(text="No aplica")

            self.label_media.pack_forget()
            self.entrada_media.pack_forget()
            self.label_desviacion.pack_forget()
            self.entrada_desviacion.pack_forget()
            self.label_lambda.pack_forget()
            self.entrada_lambda.pack_forget()

        elif metodo == "Distribución Normal":
            self.entrada_a.delete(0, tk.END)
            self.entrada_c.delete(0, tk.END)
            self.entrada_m.delete(0, tk.END)
            self.entrada_a.config(state=tk.DISABLED)
            self.entrada_c.config(state=tk.DISABLED)
            self.entrada_m.config(state=tk.DISABLED)
            self.entrada_media.config(state=tk.NORMAL)
            self.entrada_desviacion.config(state=tk.NORMAL)
            self.entrada_media.delete(0, tk.END)
            self.entrada_media.insert(0, "0")  
            self.entrada_desviacion.delete(0, tk.END)
            self.entrada_desviacion.insert(0, "1") 

            
            self.label_lambda.pack_forget()
            self.entrada_lambda.pack_forget()

        elif metodo == "Distribución Exponencial":
            self.entrada_a.config(state=tk.DISABLED)
            self.entrada_c.config(state=tk.DISABLED)
            self.entrada_m.config(state=tk.DISABLED)
            self.entrada_lambda.config(state=tk.NORMAL)
            self.entrada_lambda.delete(0, tk.END)
            self.entrada_lambda.insert(0, "1.5")  

            
            self.label_media.pack_forget()
            self.entrada_media.pack_forget()
            self.label_desviacion.pack_forget()
            self.entrada_desviacion.pack_forget()

    def generar_numeros(self):
        try:
            semilla = int(self.entrada_semilla.get())
            cantidad = int(self.entrada_cantidad.get())
            metodo = self.var_metodo.get()

            self.resultados_texto.delete(1.0, tk.END)

            if metodo == "Cuadrados Medios":
                generador = GeneradorCuadradosMedios(semilla)
                for _ in range(cantidad):
                    numero = generador.generar()
                    self.resultados_texto.insert(tk.END, f"{numero:.4f}\n")

            elif metodo == "Congruencial Lineal":
                a = int(self.entrada_a.get())
                c = int(self.entrada_c.get())
                m = int(self.entrada_m.get())
                generador_uniforme = GeneradorCongruencialLineal(semilla, a, c, m)
                for _ in range(cantidad):
                    numero = generador_uniforme.generar_uniforme()
                    self.resultados_texto.insert(tk.END, f"{numero:.4f}\n")

            elif metodo == "Distribución Uniforme":
                a = float(self.entrada_a.get())
                b = float(self.entrada_c.get())
                generador_uniforme = GeneradorCongruencialLineal(semilla, 1664525, 1013904223, 2**32)
                numeros = [(a + (b - a) * generador_uniforme.generar_uniforme()) for _ in range(cantidad)]
                for numero in numeros:
                    self.resultados_texto.insert(tk.END, f"{numero:.4f}\n")

            elif metodo == "Distribución Exponencial":
                lambda_param = float(self.entrada_lambda.get())
                generador_uniforme = GeneradorCongruencialLineal(semilla, 1664525, 1013904223, 2**32)
                numeros = [-math.log(1 - generador_uniforme.generar_uniforme()) / lambda_param for _ in range(cantidad)]
                for numero in numeros:
                    self.resultados_texto.insert(tk.END, f"{numero:.4f}\n")

            elif metodo == "Distribución Normal":
                media = float(self.entrada_media.get())
                desviacion = float(self.entrada_desviacion.get())
                generador_uniforme = GeneradorCongruencialLineal(semilla, 1664525, 1013904223, 2**32)
                numeros = []
                for _ in range(cantidad // 2):
                    u1 = generador_uniforme.generar_uniforme()
                    u2 = generador_uniforme.generar_uniforme()
                    z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                    z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
                    numeros.append(media + z1 * desviacion)
                    numeros.append(media + z2 * desviacion)
                for numero in numeros:
                    self.resultados_texto.insert(tk.END, f"{numero:.4f}\n")

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores válidos.")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()