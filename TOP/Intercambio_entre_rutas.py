import itertools

def calcular_long_total(ruta, edges):
    longitud = 0
    i = 0
    while i < len(ruta)-1:
        longitud = longitud + edges[(f"{ruta[i]}", f"{ruta[i+1]}")]
        i+=1
    return longitud

def Cambiar_otra_ruta(ruta_base, edges, nsol, L, weights):
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
                if calcular_long_total(ruta_i_new, edges) <= L and calcular_long_total(ruta_j_new, edges) <= L:
                    nueva_solucion[i]=ruta_i_new
                    nueva_solucion[j]=ruta_j_new
                    key = cantidad
                    if key not in vecinos:
                        vecinos[key] = []
                    vecinos[key] = nueva_solucion
                    cantidad += 1

    return vecinos
