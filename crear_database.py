import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
import pickle
from scipy.io.wavfile import read
from crear_constelacion import crear_constelacion
from crear_hashes import crear_hashes


def crear_base_de_datos():
    canciones = glob.glob('canciones/*.wav')

    dic_canciones = {}
    database: Dict[int, List[Tuple[int, int]]] = {}

    for indice, nom_archivo in enumerate(tqdm(sorted(canciones))):
        dic_canciones[indice] = nom_archivo
        Fs, audio_input = read(nom_archivo)
        constellation = crear_constelacion(audio_input, Fs)
        hashes = crear_hashes(constellation, indice)
        for hash, indice_pares_tiempo in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(indice_pares_tiempo)

    with open("database.pickle", 'wb') as db:
        pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
    with open("dic_canciones.pickle", 'wb') as songs:
        pickle.dump(dic_canciones, songs, pickle.HIGHEST_PROTOCOL)
