def puntuar_canciones(hashes, database):
    dic_coincidencias = {}

    # Para cada hash en la cancion, se verifica si hay un match en la base de datos
    # como pueden haber multiples coincidencias, se guarda en un diccionario con el id y el tiempo
    for hash, (tiempo_sampleo, _) in hashes.items():
        if hash in database:
            ocurrencias_coincidentes = database[hash]
            for tiempo_fuente, indice_cancion in ocurrencias_coincidentes:
                if indice_cancion not in dic_coincidencias:
                    dic_coincidencias[indice_cancion] = []
                dic_coincidencias[indice_cancion].append((hash, tiempo_sampleo, tiempo_fuente))

    # para cada cancion se calcula un puntaje, que ve cuantas veces se repite un hash en la cancion
    puntajes = {}
    for indice_cancion, coincidencia in dic_coincidencias.items():
        dic_puntuaciones_cancion_por_diferencia = {}
        for hash, tiempo_sampleo, tiempo_fuente in coincidencia:
            delta = tiempo_fuente - tiempo_sampleo
            if delta not in dic_puntuaciones_cancion_por_diferencia:
                dic_puntuaciones_cancion_por_diferencia[delta] = 0
            dic_puntuaciones_cancion_por_diferencia[delta] += 1

        maximo = (0, 0)
        for difrencia_tiempo, puntaje in dic_puntuaciones_cancion_por_diferencia.items():
            if puntaje > maximo[1]:
                maximo = (difrencia_tiempo, puntaje)
        
        puntajes[indice_cancion] = maximo

    # Ordena una lista con los puntajes de cada cancion y que tantos hashes se repiten
    # x[1][1] es el puntaje de la cancion
    puntajes = list(sorted(puntajes.items(), key=lambda x: x[1][1], reverse=True))

    if puntajes[0][1][1] < 150:
        return None

    return puntajes
