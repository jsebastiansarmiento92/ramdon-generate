class GeneradorCongruencialLineal:
    def __init__(self, semilla, a, c, m):
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m

    def generar(self, n):
        numeros_aleatorios = []
        for _ in range(n):
            self.semilla = (self.a * self.semilla + self.c) % self.m
            numeros_aleatorios.append(self.semilla / self.m)  # Normalizando a [0, 1)
            print(f"Número aleatorio generado (LCG): {self.semilla / self.m}")
        return numeros_aleatorios

# Función principal para ejecutar la clase
def main():
    # Configuración inicial
    semilla = 1234  # Semilla inicial
    a = 1664525  # Multiplicador
    c = 1013904223  # Incremento
    m = 2**32  # Módulo
    n = 15  # Cantidad de números a generar

    # Crear instancia de la clase
    generador = GeneradorCongruencialLineal(semilla, a, c, m)

    # Generar números
    print("Generando números usando el método de Congruencia Lineal:")
    numeros_aleatorios = generador.generar(n)

if __name__ == "__main__":
    main()
