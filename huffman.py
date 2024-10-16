from heapq import heappush, heappop, heapify
from collections import Counter

class Huffman:
    def __init__(self, simbolo, probabilidad):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.probabilidad < otro.probabilidad

def calcular_probabilidades(texto):
    frecuencia = Counter(texto)
    total_caracteres = len(texto)
    probabilidades = {caracter: freq / total_caracteres for caracter, freq in frecuencia.items()}
    return probabilidades

def construir_huffman(probabilidades):
    heap = [Huffman(simbolo, probabilidad) for simbolo, probabilidad in probabilidades.items()]
    heapify(heap)

    while len(heap) > 1:
        nodo1 = heappop(heap)  
        nodo2 = heappop(heap) 
        nuevo_nodo = Huffman(None, nodo1.probabilidad + nodo2.probabilidad)
        nuevo_nodo.izquierda = nodo1
        nuevo_nodo.derecha = nodo2
        heappush(heap, nuevo_nodo)
    
    return heappop(heap) 

def generar_codigos(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return
    
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual
    
    generar_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos(nodo.derecha, codigo_actual + "1", codigos)

    return codigos

def comprimir_huffman(texto):
    probabilidades = calcular_probabilidades(texto)

    arbol_huffman = construir_huffman(probabilidades)

    codigos_huffman = generar_codigos(arbol_huffman)

    texto_comprimido = "".join([codigos_huffman[caracter] for caracter in texto])

    return texto_comprimido, codigos_huffman

# Ejemplo de uso
texto = input("Ingresar texto: ")
texto_comprimido, codigos = comprimir_huffman(texto)

print(f"Texto original: {texto} - Tamaño en bits: {len(texto) * 8}")
print(f"Texto comprimido: {texto_comprimido} - Tamaño en bits: {len(texto_comprimido)}")
print(f"Códigos de Huffman: {codigos}")
