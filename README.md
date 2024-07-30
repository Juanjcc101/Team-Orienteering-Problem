# Solución del Problema de Orientación de Equipos (TOP)

Este repositorio contiene el código y los archivos necesarios para resolver el Problema de Orientación de Equipos (TOP) utilizando una combinación de técnicas de optimización: GRASP (Greedy Randomized Adaptive Search Procedure), Algoritmos Genéticos (GA) y Búsqueda por Vecindades Variables (VND).

## Descripción General del Problema

El Problema de Orientación de Equipos (TOP) es una variante del problema de ruteo de vehículos en la que el objetivo es maximizar las ganancias acumuladas por un equipo de vehículos al visitar un conjunto de puntos, respetando las limitaciones de tiempo y capacidad. En el TOP, cada punto tiene una ganancia asociada, y los vehículos deben decidir qué puntos visitar para maximizar la ganancia total sin exceder sus límites operacionales.

## Modelos Utilizados

### 1. GRASP (Greedy Randomized Adaptive Search Procedure)

GRASP es una metaheurística multi-arranque que construye soluciones factibles de manera iterativa y luego aplica una búsqueda local para mejorar dichas soluciones. Este modelo es útil para generar una población inicial diversa de soluciones factibles para el problema TOP. Los pasos principales incluyen:

- **Construcción**: Generar soluciones iniciales utilizando un enfoque codicioso que selecciona aleatoriamente los puntos a visitar basándose en una función de ganancia.
- **Búsqueda Local**: Refinar las soluciones construidas mediante la exploración de su vecindario para encontrar mejoras locales.

### 2. Algoritmo Genético (GA)

Los Algoritmos Genéticos son técnicas de optimización basadas en los principios de la selección natural y genética. Este modelo es utilizado para evolucionar la población de soluciones generada por GRASP. Los pasos principales incluyen:

- **Selección**: Elegir las soluciones más aptas de la población actual para ser padres de la próxima generación.
- **Cruzamiento (Crossover)**: Combinar pares de soluciones padres para producir hijos que heredan características de ambos padres.
- **Mutación**: Introducir cambios aleatorios en los hijos para mantener la diversidad genética en la población.

### 3. Algoritmo Genético combinado con Búsqueda por Vecindades Variables (GA-VND)

GA-VND es una variante del Algoritmo Genético que incorpora técnicas de Búsqueda por Vecindades Variables para mejorar aún más las soluciones generadas. La Búsqueda por Vecindades Variables aplica diferentes operadores de búsqueda local para explorar múltiples vecindarios de una solución. Los pasos principales incluyen:

- **Cruzamiento y Mutación**: Igual que en el GA estándar.
- **Búsqueda por Vecindades Variables (VND)**: Aplicar una secuencia de operadores de búsqueda local en diferentes vecindarios de cada solución, mejorando iterativamente la calidad de las soluciones.

## Contenidos del Repositorio

1. **Código Fuente**:
    - `TOP_solver.py`: Script principal que implementa la solución al problema TOP.
    - `GRASP_GA.py`: Implementación del algoritmo GRASP combinado con Algoritmos Genéticos.
    - `GA.py`: Implementación del Algoritmo Genético.
    - `GA_VND.py`: Implementación del Algoritmo Genético combinado con Búsqueda por Vecindades Variables (VND).

2. **Archivos de Entrada**:
    - `TOP{id}.txt`: Archivos de datos para cada instancia del problema, donde `{id}` es el identificador de la instancia.
    - `TimeLimit.xlsx`: Archivo Excel que contiene los límites de tiempo para cada instancia.

3. **Archivos de Salida**:
    - `TOP_Castrillon_correa_{criterio}.xlsx`: Archivos Excel generados con los resultados de las diferentes pruebas.
