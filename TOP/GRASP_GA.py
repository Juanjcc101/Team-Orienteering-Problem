import numpy as np
import time
from openpyxl import load_workbook
from itertools import islice
import numpy as np
import random

def dist_euclidiana(x1,x2):
    t = np.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)
    return round(t, 3)

def intercambiarNodoEnRuta(nodo, pos, solucion_actual_aux):
    solucion_actual_aux[pos] = f"{nodo}"
    return solucion_actual_aux

def calcular_long_total(ruta, edges):
    longitud = 0
    i = 0
    while i < len(ruta)-1:
        longitud = longitud + edges[(f"{ruta[i]}", f"{ruta[i+1]}")]
        i+=1
    return longitud

def calcular_long_total_rutas(ruta, edges):
    longitud = 0
    for w in ruta:
        i = 0
        while i < len(w)-1:
            longitud = longitud + edges[(f"{w[i]}", f"{w[i+1]}")]
            i+=1
    return longitud

def insertarNodoEnRuta(nodo, pos, ruta):
    ruta = ruta[:pos] + [f"{nodo}"] + ruta[pos:]
    return ruta

def calcularRelacion(ruta, nodo, pos, edges, weights):
    Distancia_Antes = calcular_long_total(ruta, edges)
    ruta = insertarNodoEnRuta(nodo, pos, ruta)
    Distancia_Despues = calcular_long_total(ruta, edges)
    ruta.remove(str(nodo))
    if Distancia_Despues - Distancia_Antes == 0:
        return 0  
    else:
        return weights[str(nodo)] / (Distancia_Despues - Distancia_Antes)

def calcular_peso_total(ruta, weights):
    peso = 0
    i = 0
    while i < len(ruta)-1:
        peso= peso + weights[f"{ruta[i]}"]
        i+=1
    return peso

def ConstruirSolucionGreedyRandomizada(ruta_construida, edges, nodos, K, T_max, weights):
    longitud_total = calcular_long_total(ruta_construida, edges)
    while nodos and (longitud_total <= T_max):
        LRC = GenerarListaRestringidaDeCandidatos(ruta_construida, nodos, edges, weights, K)
        clave_aleatoria = random.choice(list(LRC.keys()))
        if len(ruta_construida) == 2:
            ruta_construida = insertarNodoEnRuta(clave_aleatoria, 1, ruta_construida)
        else:
            ruta_construida = insertarNodoEnRuta(clave_aleatoria, random.choice(range(1,len(ruta_construida)-1)), ruta_construida)
        longitud_total = calcular_long_total(ruta_construida, edges)
        nodos.remove(clave_aleatoria)
        nodo_sol_actual = clave_aleatoria
        break
    return ruta_construida, nodos, nodo_sol_actual


def GenerarListaRestringidaDeCandidatos(ruta_construida, nodos, edges, weights, k):
        if len(ruta_construida) == 2:
            pos = 1
        else:
            pos = random.randrange(1,len(ruta_construida)-1,1)
        relacion = {}
        for nodo in nodos:
             relacion[f"{nodo}"] = calcularRelacion(ruta_construida, nodo, pos, edges, weights)
        relacion_ordenada  = sorted(relacion.items(), key=lambda item: item[1], reverse=True)
        primeros_k = islice(relacion_ordenada, k)
        Mejor_relación = dict(primeros_k)
        return Mejor_relación

def AplicarBusquedaLocal(solucion_actual, nodos, edges, weights, T_max):
    longitud_total = calcular_long_total(solucion_actual, edges)
    while nodos and (longitud_total <= T_max):
        mejorRelacion = -np.inf
        nodoSeleccionado = None
        posicionInsercion = None

        for nodo in nodos:
            i = 0
            while i < len(solucion_actual) - 1:
                i += 1
                relacion = calcularRelacion(solucion_actual, nodo, i, edges, weights)
                ruta_provicional = insertarNodoEnRuta(nodo, i, solucion_actual)
                longitud_provicional = calcular_long_total(ruta_provicional, edges)
                if relacion > mejorRelacion and longitud_provicional <= T_max:
                    mejorRelacion = relacion
                    nodoSeleccionado = nodo
                    posicionInsercion = i
                


        if nodoSeleccionado != None:
            solucion_actual = insertarNodoEnRuta(nodoSeleccionado, posicionInsercion, solucion_actual)
            nodos.remove(nodoSeleccionado)
        else:
            break
    return solucion_actual, nodos

def dist_euclidiana(x1,x2):
    t = np.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)
    return round(t, 3)


def GRASP(n, carros, T_max, dur, id, nsol):
    start_time = time.time()
    k = 10
    edges = {}
    dur_edges = dur[:,0:2].copy()
    dur_weights = dur[:, -1].copy()
    weights = {}
    i = 0

    while i < len(dur_edges):
        j = i + 1
        weights[f"{i}"] = dur_weights[i]
        while j < len(dur_edges):
            edges[(f"{i}", f"{j}")]=(dist_euclidiana(dur_edges[i],dur_edges[j]))
            edges[(f"{j}", f"{i}")]=(dist_euclidiana(dur_edges[i],dur_edges[j]))
            j += 1
        i += 1
    nodos = [str(nodo) for nodo in range(len(dur))]
    rutas = []
    suma_peso_total = 0
    population = [[] for _ in range(nsol)]

    for y in range(nsol):
        longitud_total = 0
        nodos_no_visitados = list(nodos[1:-1])
        nodos_visitados = []
        solucion_actual = []
        soluciones = []
        for _ in range(carros):
            solucion_actual = ['0']
            solucion_actual.append(nodos[-1])
            longitud_total = calcular_long_total(solucion_actual, edges)
            contador = 0
            while nodos_no_visitados and longitud_total <= T_max:
                solucion_provicional, nodos_no_visitados, nodo_sol_actual = ConstruirSolucionGreedyRandomizada(solucion_actual, edges, nodos_no_visitados, k, T_max, weights)
                longitud_total_provicional = calcular_long_total(solucion_provicional, edges)
                if longitud_total_provicional <= T_max:
                    solucion_mejorada, nodos_no_visitados = AplicarBusquedaLocal(solucion_provicional, nodos_no_visitados, edges, weights, T_max)
                    longitud_total = calcular_long_total(solucion_provicional, edges)
                    solucion_actual = solucion_mejorada
                    contador = 0
                else:
                    contador += 1
                    if contador > len(nodos):
                        break

            soluciones.append(solucion_actual)
            nodos_visitados = nodos_visitados + [nodo for nodo in set(nodos[1:-1]) if nodo in solucion_actual]
            nodos_no_visitados = [nodo for nodo in set(nodos[1:-1]) if nodo not in nodos_visitados]
            solucion_actual = []
        population[y] = soluciones
    end_time = time.time()
    elapsed_time = end_time - start_time
    return population, elapsed_time, edges, weights