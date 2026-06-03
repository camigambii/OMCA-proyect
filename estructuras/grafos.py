"""id :[COLORIMETRIA][][][][]"""
from collections import deque

class Grafo:
    def __init__(self):
        self.adjacencia = {}



    def agregar_nodo(self, nodo):
        if nodo not in self.adjacencia:
            self.adjacencia[nodo] = []



    def agregar_arista(self, nodo_origen, nodo_destino):
        self.agregar_nodo(nodo_origen)
        self.agregar_nodo(nodo_destino)
        
        if nodo_destino not in self.adjacencia[nodo_origen]:
            self.adjacencia[nodo_origen].append(nodo_destino)
        if nodo_origen not in self.adjacencia[nodo_destino]:
            self.adjacencia[nodo_destino].append(nodo_origen)



    def recomendar_bfs(self, tono_seleccionado):
        
        if tono_seleccionado not in self.adjacencia:
            return []

        visitados = set()
        cola = deque([tono_seleccionado])
        visitados.add(tono_seleccionado)
        
        recomendaciones_ids = []

        while cola:
            nodo_actual = cola.popleft()

            if isinstance(nodo_actual, int):
                recomendaciones_ids.append(nodo_actual)

            for vecino in self.adjacencia[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    if isinstance(vecino, int):
                        recomendaciones_ids.append(vecino)
                        
        return list(set(recomendaciones_ids))




    def construir_grafo_inicial(self, lista_productos):
        self.agregar_nodo("calido")
        self.agregar_nodo("frio")

        # 2. Conectar productos según su ID
        for producto in lista_productos:
            
            id_str = str(producto.id)
            if len(id_str) == 5:
                primer_digito = id_str[0]
                
                if primer_digito == '1':                    
                    self.agregar_arista("calido", producto.id)
                elif primer_digito == '2':
                    self.agregar_arista("frio", producto.id)
                elif primer_digito == '3':
                    pass