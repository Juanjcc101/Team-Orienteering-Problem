import numpy as np
import time
from VND import VND
from collections import Counter

def GA_VND(nsol, population, time_limit, num_children, mutation_prob, extra_time, L, 
       edges, weights, num_nodes, busquedas):

    def convert_to_hybrid_representation(grasp_population, num_nodes):
        hybrid_population = []
        for route in grasp_population:
            binary_route = [0] * num_nodes
            for node in route:
                binary_route[int(node)] = 1  # Convertir el string a entero
            hybrid_population.append((route, binary_route))  # Mantener la tupla
        return hybrid_population


    def calcular_long_total(ruta):
        longitud = 0
        if ruta[0] == ruta[1]:
            ruta.pop(0)
        if ruta[-1] == ruta[-2]:
            ruta.pop()
        for i in range(len(ruta) - 1):

            longitud += edges[(f"{ruta[i]}", f"{ruta[i + 1]}")]
        return longitud
    
    def calcular_peso_total(ruta):
        peso = 0
        for node in ruta:
            peso += weights[f'{node}']
        return peso
    
    def fitness(solution):
        total_score = 0
        for route, binary_route in solution:
            if calcular_long_total(route) > L:
                return 0  # Penalizar severamente
            else:
                score = calcular_peso_total(route)
                total_score += score
        return total_score
    
    def selection(population):
        fitness_values = [fitness(ind) for ind in population]
        fitness_sum = sum(fitness_values)

        if fitness_sum == 0:
            # Si la suma de aptitudes es cero, elegir aleatoriamente dos padres
            selected_indices = np.random.choice(len(population), size=2, replace=False)
            return population[selected_indices[0]], population[selected_indices[1]]
        
        # Normalizar las aptitudes para usarlas como probabilidades
        normalized_fitness = [f / fitness_sum for f in fitness_values]
        
        # Filtrar los individuos con aptitud cero
        filtered_population = [ind for ind, fit in zip(population, normalized_fitness) if fit > 0]
        filtered_fitness = [fit for fit in normalized_fitness if fit > 0]

        # Asegurarse de que las probabilidades sumen exactamente a 1
        filtered_fitness = np.array(filtered_fitness)
        filtered_fitness /= filtered_fitness.sum()
        
        # Seleccionar dos individuos basándose en las probabilidades
        selected_indices = np.random.choice(len(filtered_population), size=2, replace=False, p=filtered_fitness)
        
        return filtered_population[selected_indices[0]], filtered_population[selected_indices[1]]
    
    def crossover(parent1, parent2, used_nodes):
        nonlocal L, num_nodes
        max_attempts = 100  # Límite de intentos para ajustar la ruta
        child = []
        for (r1, br1), (r2, br2) in zip(parent1, parent2):
            if len(r1) <= 2:
                break
            attempts = 0
            while attempts < max_attempts:
                crossover_point = np.random.randint(1, len(r1) - 1)  # No incluir el nodo de inicio y fin
                new_route_part = r1[:crossover_point] + [node for node in r2[crossover_point:] if node not in r1[:crossover_point] and node not in used_nodes]
                if new_route_part[0] == '0':
                    if new_route_part[-1] == '31':
                        new_route = new_route_part
                    else:
                        new_route = new_route_part + [str(num_nodes - 1)]
                else:
                    if new_route_part[-1] == '31':
                        new_route = ['0'] + new_route_part
                    else:
                        new_route = ['0'] + new_route_part + [str(num_nodes - 1)]

                if calcular_long_total(new_route) <= L and len(set(new_route)) == len(new_route):
                    break  # Salir del bucle si la ruta es válida
                attempts += 1
            # Si no se encuentra una ruta válida, se usa el primer padre sin nodos repetidos
            if calcular_long_total(new_route) > L or len(set(new_route)) != len(new_route):
                new_route_part = [node for node in r1 if node not in used_nodes]
                new_route = ['0'] + new_route_part + [str(num_nodes - 1)]

            new_binary = [0] * num_nodes
            for node in new_route:
                new_binary[int(node)] = 1  # Convertir el string a entero
            child.append((new_route, new_binary))

            # Actualizar los nodos usados
            used_nodes.update(new_route[1:-1])  # Excluir 0 y num_nodes - 1

        return child

    def mutation(child, used_nodes):
        nonlocal num_nodes, L
        max_attempts = 100  # Límite de intentos para ajustar la ruta
        for route, binary_route in child:
            if len(route) <= 2:
                break
            if np.random.rand() < mutation_prob:
                attempts = 0
                while attempts < max_attempts:
                    point_idx = np.random.randint(1, len(route) - 1)  # No incluir el nodo de inicio y fin
                    # Determinar el índice con el que se intercambiará (swap)
                    if point_idx == len(route) - 2:
                        swap_idx = point_idx - 1  # Intercambiar con el nodo anterior si es el penúltimo nodo
                    else:
                        swap_idx = point_idx + 1  # Intercambiar con el siguiente nodo en otros casos
                    route[point_idx], route[swap_idx] = route[swap_idx], route[point_idx]

                    if calcular_long_total(route) <= L and len(set(route)) == len(route) and all(node not in used_nodes for node in route[1:-1]):
                        break  # Salir del bucle si la ruta es válida

                    # Revertir el cambio si no es válido
                    route[point_idx], route[swap_idx] = route[swap_idx], route[point_idx]
                    attempts += 1


                # Asegurar que la ruta empiece en 0 y termine en num_nodes-1
                route = ['0'] + route[1:-1] + [str(num_nodes - 1)]

                # Actualizar la representación binaria después de la mutación
                for i in range(len(binary_route)):
                    binary_route[i] = 1 if str(i) in route else 0

                # Actualizar los nodos usados
                used_nodes.update(route[1:-1])  # Excluir 0 y num_nodes - 1

        return child

    def update_population(parents, children):
        nonlocal nsol
        combined_population = parents + children
        combined_population = max_valor_cumple_condicion(combined_population)
        if combined_population == 'Hola':
            return parents
        fitness_values = [fitness(ind) for ind in combined_population]
        sorted_indices = np.argsort(fitness_values)[-nsol:]
        new_population = [combined_population[i] for i in sorted_indices]
        return new_population
    
    def genetic_algorithm():
        nonlocal population, num_children, extra_time, edges, weights, L, busquedas, num_nodes
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            total_elapsed_time = elapsed_time + extra_time
            if total_elapsed_time > time_limit:
                return population, total_elapsed_time
            
            children = []
            for _ in range(num_children):
                current_time = time.time()
                elapsed_time = current_time - start_time
                total_elapsed_time = elapsed_time + extra_time
                if total_elapsed_time > time_limit:
                    return population, total_elapsed_time

                used_nodes = set()
                parent1, parent2 = selection(population)
                child = crossover(parent1, parent2, used_nodes)
                used_nodes.update([node for route, _ in child for node in route[1:-1]])  # Actualizar nodos usados excluyendo 0 y num_nodes-1
                child = mutation(child, used_nodes)
                used_nodes.update([node for route, _ in child for node in route[1:-1]])  # Actualizar nodos usados excluyendo 0 y num_nodes-1
                ruta_VND = []
                recorrido_original = fitness(child)
                for hijo in child:
                    ruta_VND.append(hijo[0])
                nuevo_mejorado = VND(ruta_VND, edges, weights, L, busquedas)
                nuevo_mejorado_bin = convert_to_hybrid_representation(nuevo_mejorado, num_nodes)
                #print(nuevo_mejorado_bin)
                recorrido_mejorado = fitness(nuevo_mejorado_bin)
                if recorrido_mejorado > recorrido_original:
                    child = nuevo_mejorado_bin
                children.append(child) 

            population = update_population(population, children)

    def check_exactly_two_common_elements(lists):
        # Convertir cada lista en un conjunto para encontrar los elementos únicos en cada lista
        sets = [set(lst) for lst in lists]
        
        # Encontrar la intersección de todos los conjuntos para obtener los elementos comunes
        common_elements = set.intersection(*sets)
        
        # Verificar que hay exactamente dos elementos comunes
        if len(common_elements) != 2:
            return False
        
        # Contar la frecuencia de todos los elementos en las listas
        all_elements = [elem for lst in lists for elem in lst]
        element_counts = Counter(all_elements)
        
        # Verificar que los elementos comunes tienen una frecuencia de 4 (aparecen en todas las listas)
        for elem in common_elements:
            if element_counts[elem] != len(lists):
                return False
        
        # Verificar que todos los demás elementos tienen una frecuencia de 1 (son únicos)
        for elem, count in element_counts.items():
            if elem not in common_elements and count != 1:
                return False
        
        return True
    
    def max_valor_cumple_condicion(lists):
        # Obtener todos los elementos que cumplen la condición
        elementos_validos = []
        for element in lists:
            final_route = []
            for route_in, binary_route in element:
                final_route.append(route_in)
            if check_exactly_two_common_elements(final_route) == True:
                elementos_validos.append(element)
        # Devolver el máximo de esos elementos
        if elementos_validos:
            best_solution = max(elementos_validos, key=fitness)
            #return best_solution, fitness(best_solution)
            return elementos_validos
        else:
            return 'Hola'  # Si no hay elementos que cumplan la condición
        
    def max_valor_cumple_condicion1(lists):
        # Obtener todos los elementos que cumplen la condición
        elementos_validos = []
        for element in lists:
            final_route = []
            for route_in, binary_route in element:
                final_route.append(route_in)
            if check_exactly_two_common_elements(final_route) == True:
                elementos_validos.append(element)
        # Devolver el máximo de esos elementos
        if elementos_validos:
            best_solution = max(elementos_validos, key=fitness)
            return best_solution, fitness(best_solution)
        else:
            return 'Hola',2  # Si no hay elementos que cumplan la condición
    
    population, total_elapsed_time = genetic_algorithm()
    best_solution, fitness_value = max_valor_cumple_condicion1(population)
    return best_solution, fitness_value, round(total_elapsed_time * 1000)


