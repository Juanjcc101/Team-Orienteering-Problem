def calcular_long_total(ruta, edges):
    longitud = 0
    i = 0
    while i < len(ruta)-1:
        longitud = longitud + edges[(f"{ruta[i]}", f"{ruta[i+1]}")]
        i+=1
    return longitud


def Invertir(ruta_base, edges, nsol, L, weights):
    vecinos = {}
    for i in range(nsol):
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
                    if longitud_modificada <= L and longitud_modificada < mejor_longitud:
                        mejor_ruta_local = ruta_modificada.copy()
                        mejor_longitud = longitud_modificada
                        cambios_realizados = True

            # Agregar la mejor ruta local encontrada a la nueva solución
            nueva_solucion.append(mejor_ruta_local)
        
        if cambios_realizados:
            vecinos[i] = nueva_solucion
    
    return vecinos