import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks
import os
import hashlib
import pickle
import time
from tkinter import filedialog

def graficar_espectrograma(spectrograma_graficable,frequencies,time,frecuencia_de_muestreo):
    
    plt.pcolormesh(time, frequencies, 10 * np.log10(spectrograma_graficable), cmap='jet')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Power spectral density (dB/Hz)")
    plt.ylim([0, frecuencia_de_muestreo/2.])
    plt.show()


def datos_espectrograma(archivo_audio):
    frecuencia_de_muestreo, datos = wavfile.read(archivo_audio)
    if(len(datos.shape) > 1):#pasar a mono el audio
        datos = np.mean(datos, axis=1)
        
    
    window_size = 2024
    overlap = int(window_size*0.5)
    # Ventanas para analisis de la señal
    window = np.hamming(window_size)
    windows = [datos[i:i+window_size] * window for i in range(0, len(datos)-window_size, window_size-overlap)]
    # Calcuo del FFT para cada ventana (o intervalo) de la señal
    spectrograma = [np.abs(np.fft.rfft(win))**2 for win in windows]
    # La transpuesta es solo para poder graficar el espectrograma
    spectrograma_graficable = np.array(spectrograma).T
    
    # frecuencias y tiempo
    frequencies = np.fft.rfftfreq(window_size, d=1.0/frecuencia_de_muestreo)
    time = np.arange(len(spectrograma_graficable[0])) * (window_size - overlap) / frecuencia_de_muestreo
    return spectrograma_graficable,frequencies,time,frecuencia_de_muestreo
    

def graficar_picos_frecuencias(peak_times, peak_frequencies):
    # Grafico de picos de frecuencias mas relevantes
    plt.scatter(peak_times, peak_frequencies, color='black', marker='x')
    plt.show()  

def picos_frecuencias(spectrograma_graficable,frequencies,time):
    #picos de frecuencias
    # Encuentra los indices de los picos de frecuencia mas relevantes
    peak_indices = find_peaks(np.max(spectrograma_graficable, axis=0))[0]
    #Picos de frecuencia ordenados por tiempo
    peak_frequencies = frequencies[np.argmax(spectrograma_graficable, axis=0)[peak_indices]]#frecuencias relevantes
    peak_times = time[peak_indices]
    return peak_times, peak_frequencies



def generar_huellas(peak_frequencies, peak_times, fan_out=50): #fan out es el numero de puntos vecinos que se consideran para generar la huella
    fingerprints = []
    #se itera para cada pico de frecuencia y se crea un hash con los picos de frecuencia vecinos
    for i in range(len(peak_times)): 
        for j in range(1, fan_out):
            if i + j < len(peak_times): #se verifica que no se salga del rango
                freq1 = peak_frequencies[i] 
                freq2 = peak_frequencies[i + j]
                t1 = peak_times[i]
                t2 = peak_times[i + j]

                # diferencia de tiempo entre los picos de frecuencia
                delta_t = t2 - t1

                # Crea el hash
                hash = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(delta_t)}".encode('utf-8')).hexdigest()
                # Agrega el hash a la lista de huellas
                fingerprints.append((hash, t1))

    return fingerprints

def identificar_song(fingerprints, database):
    song_counts = {} #diccionario que cuenta los aciertos de cada cancion
    for fp, delta_t in fingerprints: #se itera para cada huella
        if fp in database: #se verifica que la huella este en la base de datos (si ninguna cancion tiene esa huella no le corresponde)
            for id_cancion, stored_delta_t in database[fp]:
                if abs(stored_delta_t - delta_t) <= 1:  #permite un margen de error de 1 segundo en los tiempos
                    if id_cancion not in song_counts: #se agrega la cancion al diccionario si no esta
                        song_counts[id_cancion] = 1
                    song_counts[id_cancion] += 1

    # Regresa el id de la cancion con mas aciertos
    return max(song_counts, key=song_counts.get) if song_counts else None


def wrapper_graficador_espectrograma(archivo_audio):
    graficar_espectrograma(*datos_espectrograma(archivo_audio))

def wrapper_graficador_frecuencias(archivo_audio):
    graficar_picos_frecuencias(*picos_frecuencias(*datos_espectrograma(archivo_audio)[:3]))

def guardar_huella_base_de_datos(archivo_audio,base_de_datos):
    huellas = wrapper_generar_huellas(archivo_audio)
    for fp, delta_t in huellas:
        if fp not in base_de_datos:
            base_de_datos[fp] = []
        base_de_datos[fp].append((archivo_audio, delta_t))

def wrapper_generar_huellas(archivo_audio):
    picos_tiempo,picos_f = picos_frecuencias(*datos_espectrograma(archivo_audio)[:3])
    return generar_huellas(picos_f,picos_tiempo)

    




if __name__ == "__main__":

    folder_path = filedialog.askdirectory()
    # Cambiar al directorio seleccionado
    os.chdir(folder_path)

    
    database = pickle.load(open('database.pkl', 'rb'))

    if(False):
        guardar_huella_base_de_datos('ReachSummit.wav', database)
        guardar_huella_base_de_datos('San Lucas.wav', database)
        guardar_huella_base_de_datos('Memory.wav', database)
        guardar_huella_base_de_datos('Fairy_Fountain.wav', database)
        guardar_huella_base_de_datos('PetitAlegro.wav', database)
        guardar_huella_base_de_datos('SweetPiano.wav', database)
        guardar_huella_base_de_datos('Thats so raven.wav', database)
        guardar_huella_base_de_datos('Until I Found You.wav', database)
        guardar_huella_base_de_datos('Lost.wav', database)
        guardar_huella_base_de_datos('Aqui Abajo.wav', database)
    

    comienzo = time.time()
    id_cancion = identificar_song(wrapper_generar_huellas('ReachSummitT2.wav'), database)
    print(id_cancion)
    id_cancion = identificar_song(wrapper_generar_huellas('SanlucasUkelele.wav'), database)
    print(id_cancion)
    id_cancion = identificar_song(wrapper_generar_huellas('ReachSummitTest.wav'), database)
    print(id_cancion)
    end_time = time.time()
        
    print("Se demoro : ", end_time - comienzo, " segundos en procesar las canciones")
    
    
    