import time
from Intercambio_nodos_no_visitados import Intercambio
from Invertir_pos_en_ruta import Invertir
from Intercambio_entre_rutas import Cambiar_otra_ruta
import copy

def check_no_repeats_except_first_last(list_of_lists):
    seen = set()
    for lst in list_of_lists:
        if len(lst) > 2:  # Solo verificar si hay más de dos elementos
            for value in lst[1:-1]:  # Excluir el primer y último elemento
                if value in seen:
                    return False
                seen.add(value)
    return True

def calcular_long_total(ruta, edges):
    longitud = 0
    for w in ruta:
        i = 0
        while i < len(w)-1:
            longitud = longitud + edges[(f"{w[i]}", f"{w[i+1]}")]
            i+=1
    return longitud

def calcular_peso_total(ruta, weights):
    peso = 0
    for w in ruta:
        i = 0
        while i < len(w)-1:
            peso= peso + weights[f"{w[i]}"]
            i+=1
    return peso

def VND(Solucion_inicial, edges, weights, L, neighborhoods):
    vecinos = copy.deepcopy(neighborhoods)
    if check_no_repeats_except_first_last(Solucion_inicial) == False:
        vecinos.pop()
    nsol= 100
    S = Solucion_inicial
    j = 0
    while j < len(vecinos):
        rutas0 = globals()[vecinos[j]](S, edges, nsol, L, weights)
        if rutas0 == {}:
            j+=1
            continue
        s_prime = []
        for z in range(len(rutas0)-1):
            if calcular_peso_total(rutas0[z], weights) < calcular_peso_total(rutas0[z+1], weights):
                s_prime =  rutas0[z+1]
            else:
                s_prime =  rutas0[z]
        if calcular_peso_total(s_prime, weights) > calcular_peso_total(S, weights) or (calcular_peso_total(s_prime, weights) == calcular_peso_total(S, weights) and calcular_long_total(s_prime, edges) < calcular_long_total(S, edges)):
            j = 0
            S = s_prime
        else:
            j += 1
    return S