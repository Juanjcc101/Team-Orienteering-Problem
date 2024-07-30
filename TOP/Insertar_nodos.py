import random
import copy
import itertools
def calcular_long_total(ruta, edges):
    longitud = 0
    i = 0
    while i < len(ruta)-1:
        longitud = longitud + edges[(f"{ruta[i]}", f"{ruta[i+1]}")]
        i+=1
    return longitud

def calcular_long_total_varias_rutas(ruta, edges):
    longitud = 0
    for w in ruta:
        i = 0
        while i < len(w)-1:
            longitud = longitud + edges[(f"{w[i]}", f"{w[i+1]}")]
            i+=1
    return longitud

def calcular_peso_total_varias_rutas(ruta, weights):
    peso = 0
    for w in ruta:
        i = 0
        while i < len(w)-1:
            peso= peso + weights[f"{w[i]}"]
            i+=1
    return peso

def Insertar_Intercambio(ruta_base, edges, L, node_weights):
    vecinos = {}
    todos_los_nodos = [str(nodo) for nodo in range(int(ruta_base[0][0]), int(ruta_base[0][-1]) + 1)]
    nodos_visitados = [nodo for ruta in ruta_base for nodo in ruta]
    nodos_no_visitados = [nodo for nodo in todos_los_nodos if nodo not in nodos_visitados]
    for t in range(len(nodos_no_visitados)):
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
                        if all(n in edges for n in zip(w_aux[:-1], w_aux[1:])) and calcular_long_total(w_aux, edges) <= calcular_long_total(w, edges):
                            nueva_solucion.append(w_aux.copy())
                            intercambio_realizado = True
                            nodos_no_visitados.remove(nodo)     
                            break
                        else:
                            w_aux = w.copy()

            # Try replacing one unvisited node for two or three visited nodes, not touching the last node
            if not intercambio_realizado:
                for num_replaced in range(2, 5):  # Trying for 2 and then 3 visited nodes
                    for nodo in nodos_no_visitados:
                        for pos in range(1, len(w) - num_replaced):  # Adjust the range to keep the last node intact
                            if node_weights[nodo] >= sum(node_weights[w[j]] for j in range(pos, pos + num_replaced)):
                                w_aux[pos:pos + num_replaced] = [nodo] + [''] * (num_replaced - 1)
                                cleaned_route = [node for node in w_aux if node != '']
                                if all(n in edges for n in zip(cleaned_route[:-1], cleaned_route[1:])) and calcular_long_total(cleaned_route, edges) <= calcular_long_total(w, edges):
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
            vecinos[t] = nueva_solucion
    if vecinos != {}:
        ruta_base = vecinos[0]
        for i in range(1, len(vecinos)):
            if calcular_peso_total_varias_rutas(vecinos[i], node_weights) > calcular_peso_total_varias_rutas(ruta_base, node_weights) or (calcular_peso_total_varias_rutas(vecinos[i], node_weights) == calcular_peso_total_varias_rutas(ruta_base, node_weights) and calcular_long_total_varias_rutas(vecinos[i], edges) < calcular_long_total_varias_rutas(ruta_base, edges)):
                ruta_base = vecinos[i]
        vecinos = {}

    cantidad = 0
    for combination in itertools.combinations(range(len(ruta_base)), 2):
        nueva_solucion = ruta_base.copy()
        i, j = combination
        ruta_i = ruta_base[i]
        ruta_j = ruta_base[j]

        # Try to swap each node in ruta_i with each node in ruta_j
        for idx_i in range(1, len(ruta_i) - 1):  # Exclude first and last nodes for swapping
            for idx_j in range(1, len(ruta_j) - 1):
                # Make the swap
                ruta_i_new = ruta_i[:]
                ruta_j_new = ruta_j[:]
                ruta_i_new[idx_i], ruta_j_new[idx_j] = ruta_j_new[idx_j], ruta_i_new[idx_i]

                # Check the new routes against the length constraint
                if calcular_long_total(ruta_i_new, edges) < calcular_long_total(ruta_base[i], edges) and calcular_long_total(ruta_j_new, edges) < calcular_long_total(ruta_base[j], edges):
                    nueva_solucion[i]=ruta_i_new
                    nueva_solucion[j]=ruta_j_new
                    key = cantidad
                    if key not in vecinos:
                        vecinos[key] = []
                    vecinos[key] = nueva_solucion
                    cantidad += 1

    if vecinos != {}:
        ruta_base = vecinos[0]
        for i in range(1, len(vecinos)):
            if calcular_peso_total_varias_rutas(vecinos[i], node_weights) > calcular_peso_total_varias_rutas(ruta_base, node_weights) or (calcular_peso_total_varias_rutas(vecinos[i], node_weights) == calcular_peso_total_varias_rutas(ruta_base, node_weights) and calcular_long_total_varias_rutas(vecinos[i], edges) < calcular_long_total_varias_rutas(ruta_base, edges)):
                ruta_base = vecinos[i]
        vecinos = {}

    for i in range(30):
        nueva_solucion = []
        cambios_realizados = False
        
        for ruta in ruta_base:
            # La nueva solución para esta ruta en particular
            mejor_ruta_local = ruta.copy()
            mejor_longitud = calcular_long_total(ruta, edges)
            
            # Explorar todas las subsecuencias posibles para invertir
            for inicio in range(1, len(ruta) - 2):  # El inicio de la subsecuencia a invertir
                for fin in range(inicio + 1, len(ruta) - 1):  # El final de la subsecuencia a invertir
                    ruta_modificada = ruta.copy()
                    # Invertir la subsecuencia en la ruta copiada
                    ruta_modificada[inicio:fin + 1] = ruta_modificada[inicio:fin + 1][::-1]
                    # Calcular la longitud total de la ruta modificada
                    longitud_modificada = calcular_long_total(ruta_modificada, edges)
                    if longitud_modificada < mejor_longitud:
                        mejor_ruta_local = ruta_modificada.copy()
                        mejor_longitud = longitud_modificada
                        cambios_realizados = True

            # Agregar la mejor ruta local encontrada a la nueva solución
            nueva_solucion.append(mejor_ruta_local)
        
        if cambios_realizados:
            vecinos[i] = nueva_solucion
    if vecinos != {}:
        ruta_base = vecinos[0]
        for i in range(1, len(vecinos)):
            if calcular_peso_total_varias_rutas(vecinos[i], node_weights) > calcular_peso_total_varias_rutas(ruta_base, node_weights) or (calcular_peso_total_varias_rutas(vecinos[i], node_weights) == calcular_peso_total_varias_rutas(ruta_base, node_weights) and calcular_long_total_varias_rutas(vecinos[i], edges) < calcular_long_total_varias_rutas(ruta_base, edges)):
                ruta_base = vecinos[i]
        vecinos = {}

    todos_los_nodos = [str(nodo) for nodo in range(int(ruta_base[0][0]), int(ruta_base[0][-1]) + 1)]
    nodos_visitados = [nodo for ruta in ruta_base for nodo in ruta]
    nodos_no_visitados = [nodo for nodo in todos_los_nodos if nodo not in nodos_visitados]

    solucion_final = []
    for ruta in ruta_base:
        ruta_aux = copy.deepcopy(ruta)
        for nodo in nodos_no_visitados:
            for x in range(1,len(ruta)):
                nueva_ruta = copy.deepcopy(ruta_aux)
                nueva_ruta.insert(x, nodo)
                if calcular_long_total(nueva_ruta, edges) <= L:
                    ruta_aux = copy.deepcopy(nueva_ruta)
                    nodos_no_visitados.remove(nodo)
                    break
        solucion_final.append(ruta_aux)

    return solucion_final

    














    todos_los_nodos = [str(nodo) for nodo in range(int(ruta_base[0][0]), int(ruta_base[0][-1]) + 1)]
    nodos_visitados = [nodo for ruta in ruta_base for nodo in ruta]
    nodos_no_visitados = [nodo for nodo in todos_los_nodos if nodo not in nodos_visitados]
    nueva_solucion =[]
    for ruta in ruta_base:
        for nodo in nodos_no_visitados:
            for x in range(1,len(ruta)):
                nueva_ruta = copy.deepcopy(ruta)
                nueva_ruta.insert(x, nodo)
                print(nueva_ruta)
                if calcular_long_total(nueva_ruta, edges) <= L:
                    nueva_solucion.append(nueva_ruta)
                    nodos_no_visitados.remove(nodo)

    if len(nueva_solucion) < 2:
        return ruta_base
    else:
        return nueva_solucion
