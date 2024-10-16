from collections import defaultdict, Counter
import heapq

# Función para construir la matriz de transición de Markov de orden 2
def construir_matriz_transicion_orden_2(texto):
    contexto_pares = defaultdict(Counter)

    # Recorrer el texto y contar las transiciones
    for i in range(len(texto) - 2):
        contexto = (texto[i], texto[i+1])
        siguiente_caracter = texto[i+2]
        contexto_pares[contexto][siguiente_caracter] += 1

    # Convertir los conteos en probabilidades
    matriz_transicion = {}
    for contexto, conteos in contexto_pares.items():
        total = sum(conteos.values())
        matriz_transicion[contexto] = {caracter: conteo / total for caracter, conteo in conteos.items()}
    
    print("Matriz de transiciones:", matriz_transicion)
    return matriz_transicion

# Clase Nodo para la construcción de códigos binarios basado en la probabilidad
class NodoHuffman:
    def __init__(self, simbolo, probabilidad):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro):
        return self.probabilidad < otro.probabilidad

# Generar los códigos binarios de Huffman para cada transición
def generar_codigos_huffman(nodo, codigo_actual="", codigos=None):
    if codigos is None:
        codigos = {}
    
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual
    
    if nodo.izquierda:
        generar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigos)
    
    if nodo.derecha:
        generar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigos)

    return codigos

# Función para asignar códigos binarios a las transiciones
def asignar_codigos(matriz_transicion):
    codigos_transicion = {}

    for contexto, transiciones in matriz_transicion.items():
        # Crear un heap de Huffman para cada conjunto de transiciones
        heap = [NodoHuffman(simbolo, probabilidad) for simbolo, probabilidad in transiciones.items()]
        heapq.heapify(heap)

        # Si hay una única transición posible, asignar '0' para ella
        if len(heap) == 1:
            unico_nodo = heapq.heappop(heap)
            codigos_transicion[contexto] = {unico_nodo.simbolo: '0'}
        else:
            # Construir el árbol de Huffman
            while len(heap) > 1:
                nodo1 = heapq.heappop(heap)
                nodo2 = heapq.heappop(heap)
                nuevo_nodo = NodoHuffman(None, nodo1.probabilidad + nodo2.probabilidad)
                nuevo_nodo.izquierda = nodo1
                nuevo_nodo.derecha = nodo2
                heapq.heappush(heap, nuevo_nodo)

            arbol_huffman = heapq.heappop(heap)
            codigos_transicion[contexto] = generar_codigos_huffman(arbol_huffman)
    
    # Mostrar los códigos binarios generados para cada transición
    for contexto, codigos in codigos_transicion.items():
        print(f"Códigos para el contexto {contexto}: {codigos}")
    
    return codigos_transicion

# Función para codificar el texto utilizando los códigos de las transiciones
def codificar_markov_orden_2(texto, codigos_transicion):
    # Empezamos codificando los dos primeros caracteres en ASCII
    codigo_binario = ''.join(format(ord(c), '08b') for c in texto[:2])

    # Recorrer el texto desde el tercer carácter y codificar usando los códigos binarios asignados a las transiciones
    for i in range(2, len(texto)):
        contexto = (texto[i-2], texto[i-1])
        caracter_actual = texto[i]
        # Verificamos que el contexto tenga un código asignado
        if contexto in codigos_transicion and caracter_actual in codigos_transicion[contexto]:
            codigo_binario += codigos_transicion[contexto][caracter_actual]
        else:
            print(f"Error: No se encontró código para la transición {contexto} -> {caracter_actual}")
    
    return codigo_binario

# Ejemplo de uso
texto = input("Introduce una cadena de texto: ")

# 1. Construir la matriz de transición
matriz_transicion = construir_matriz_transicion_orden_2(texto)

# 2. Asignar códigos binarios a cada transición
codigos_transicion = asignar_codigos(matriz_transicion)

# 3. Codificar el texto usando el modelo de Markov de orden 2
texto_codificado = codificar_markov_orden_2(texto, codigos_transicion)

print(f"Texto original: {texto}")
print(f"Texto codificado en binario: {texto_codificado}")
