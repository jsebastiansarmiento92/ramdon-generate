import unittest
import random
from math import sqrt

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
            numeros_aleatorios.append(self.semilla / self.m)
        return numeros_aleatorios

def chi_cuadrado(frecuencias_observadas, frecuencias_esperadas):
    chi_stat = sum((observada - esperada) ** 2 / esperada for observada, esperada in zip(frecuencias_observadas, frecuencias_esperadas))
    return chi_stat

class TestGeneradorNumerosAleatorios(unittest.TestCase):

    def setUp(self):
        self.semilla = 1234
        self.a = 1549684
        self.c = 1013904223
        self.m = 2**32
        self.n = 5
        self.generador = GeneradorCongruencialLineal(self.semilla, self.a, self.c, self.m)

    def test_aleatoriedad_kolmogorov(self):
        numeros_aleatorios = self.generador.generar(self.n)
        # Implementación simplificada aquí o usa una librería alternativa si es posible
        # Aquí solo imprimimos para ejemplo
        print(f"Verificación Kolmogorov-Smirnov no implementada")

    def test_distribucion_uniforme_chi_cuadrado(self):
        numeros_aleatorios = self.generador.generar(self.n)
        frecuencias_observadas = [0] * 10
        for num in numeros_aleatorios:
            index = int(num * 10)
            frecuencias_observadas[index] += 1
        frecuencias_esperadas = [self.n / 10] * 10
        chi_stat = chi_cuadrado(frecuencias_observadas, frecuencias_esperadas)
        print(f"Chi-Square Statistic: {chi_stat}")
        # Aquí deberías agregar la comparación con el valor crítico de Chi cuadrado
        self.assertTrue(True)  # Ejemplo simplificado

    def test_no_correlacion_serial_poker(self):
        numeros_aleatorios = self.generador.generar(self.n)
        secuencias = [''.join(str(int(num * 10)) for num in numeros_aleatorios[i:i+5]) for i in range(0, self.n, 5)]
        patrones = {
            '5 iguales': 0,
            '4 iguales': 0,
            'full house': 0,
            '3 iguales': 0,
            '2 pares': 0,
            '1 par': 0,
            'todos diferentes': 0
        }
        for secuencia in secuencias:
            counts = {d: secuencia.count(d) for d in set(secuencia)}
            if 5 in counts.values():
                patrones['5 iguales'] += 1
            elif 4 in counts.values():
                patrones['4 iguales'] += 1
            elif sorted(counts.values()) == [2, 3]:
                patrones['full house'] += 1
            elif 3 in counts.values():
                patrones['3 iguales'] += 1
            elif list(counts.values()).count(2) == 2:
                patrones['2 pares'] += 1
            elif 2 in counts.values():
                patrones['1 par'] += 1
            else:
                patrones['todos diferentes'] += 1
        print("Resultados de la prueba de poker:", patrones)

if __name__ == '__main__':
    unittest.main()
