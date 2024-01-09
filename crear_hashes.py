def crear_hashes(mapa_constelaciones, id_cancion=None):
    frecuencia_maxima = 23_000
    bits_para_frecuencia = 10
    hashes = {}
    # iteramos sobre los pares de la constelacion
    for idx, (tiempo, freq) in enumerate(mapa_constelaciones):
        # Iteramos a lo largo de los siguientes 100 pares
        # (aqui es donde se toma las frecuencias cercanas y se asocia su par con su diferencia de tiempo)
        for este_tiempo, esta_frecuencia in mapa_constelaciones[idx: idx + 100]:
            diferencia_tiempo = este_tiempo - tiempo
            # Si la diferencia de tiempo es menor a 1 o mayor a 10
            # se ignora el par (para evitar parejas con tiempos muy cercanos o muy lejanos)
            if diferencia_tiempo <= 1 or diferencia_tiempo > 10:
                continue
            
            # Se discretiza la frecuencia en 2^10 = 1024 valores el proceso
            # es con el objetivo de producir un hash de 32 bits
            freq_binned = freq / frecuencia_maxima * (2 ** bits_para_frecuencia)
            esta_frecuencia_binned = esta_frecuencia / frecuencia_maxima * (2 ** bits_para_frecuencia)

            # Se genera el hash de 32 bits
            hash = int(freq_binned) | (int(esta_frecuencia_binned) << 10) | (int(diferencia_tiempo) << 20)
            hashes[hash] = (tiempo, id_cancion)  # se guarda el hash con su tiempo y el id de la cancion
    return hashes

