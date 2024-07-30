import random

def calcular_long_total(ruta, edges):
    longitud = 0
    i = 0
    while i < len(ruta)-1:
        longitud = longitud + edges[(f"{ruta[i]}", f"{ruta[i+1]}")]
        i+=1
    return longitud

def Intercambio(ruta_base, edges, nsol, L, node_weights):
    vecinos = {}
    todos_los_nodos = [str(nodo) for nodo in range(int(ruta_base[0][0]), int(ruta_base[0][-1]) + 1)]
    nodos_visitados = [nodo for ruta in ruta_base for nodo in ruta]
    nodos_no_visitados = [nodo for nodo in todos_los_nodos if nodo not in nodos_visitados]

    for i in range(nsol):
        nueva_solucion = []
        for w in ruta_base:
            w_aux = w.copy()
            intercambio_realizado = False

            # Only consider positions that are not the first or the last in the route
            for nodo in nodos_no_visitados:
                if intercambio_realizado:
                    break
                for pos in range(1, len(w) - 2):  # Exclude the last node from being swapped
                    if node_weights[nodo] >= node_weights[w[pos]]:
                        w_aux[pos] = nodo
                        if all(n in edges for n in zip(w_aux[:-1], w_aux[1:])) and calcular_long_total(w_aux, edges) <= L:
                            nueva_solucion.append(w_aux.copy())
                            intercambio_realizado = True
                            nodos_no_visitados.remove(nodo)     
                            break
                        else:
                            w_aux = w.copy()

            # Try replacing one unvisited node for two or three visited nodes, not touching the last node
            if not intercambio_realizado:
                for num_replaced in range(2, 4):  # Trying for 2 and then 3 visited nodes
                    for nodo in nodos_no_visitados:
                        for pos in range(1, len(w) - num_replaced):  # Adjust the range to keep the last node intact
                            if node_weights[nodo] >= sum(node_weights[w[j]] for j in range(pos, pos + num_replaced)):
                                w_aux[pos:pos + num_replaced] = [nodo] + [''] * (num_replaced - 1)
                                cleaned_route = [node for node in w_aux if node != '']
                                if all(n in edges for n in zip(cleaned_route[:-1], cleaned_route[1:])) and calcular_long_total(cleaned_route, edges) <= L:
                                    nueva_solucion.append(cleaned_route)
                                    intercambio_realizado = True
                                    nodos_no_visitados.remove(nodo)
                                    break
                                else:
                                    w_aux = w.copy()
                        if intercambio_realizado:
                            break
                    if intercambio_realizado:
                        break
            
            if not intercambio_realizado:
                nueva_solucion.append(w)

        if nueva_solucion != ruta_base:
            vecinos[i] = nueva_solucion

    return vecinos
