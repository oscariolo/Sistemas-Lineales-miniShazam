import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from crear_constelacion import crear_constelacion, datos_espectrograma
import seaborn as sbn

 
def graficar_constelacion(audio_file):
    Fs, audio = read(audio_file)
    constelacion_data = crear_constelacion(audio, Fs)
    pico_tiempos = [x[0] for x in constelacion_data] 
    pico_frecuencias = [x[1] for x in constelacion_data]
    
    plt.scatter(pico_tiempos, pico_frecuencias, color='black', marker='x')
    plt.show()


def graficar_espectrograma(audio_file):
    # Grafico de espectrograma
    Fs, audio = read(audio_file)
    amplitud, frecuencias, tiempos = datos_espectrograma(audio, Fs)
    amplitud = [abs(x)**2 for x in amplitud]  # Energia de la señal que representara el color en el espectrograma
    plt.pcolormesh(tiempos, frecuencias, 10 * np.log10(amplitud), cmap='jet')  # se pasa la amplitud a una escala logaritmica para interpretarla mejor (decibeles)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.colorbar(label="Densidad espectral de la potencia (dB/Hz)")
    plt.ylim([0, Fs/2.])
    plt.show()


def graficador_espectrograma(archivo_audio):
    frecuencia_de_muestreo, datos = read(archivo_audio)
    if datos.ndim == 1:  # pasar a mono el audio
        datos = datos.reshape(-1)
    else:
        datos = datos[:,0].ravel()

    window_size = 1024
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
    # ---------------------#
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(time, frequencies, 10 * np.log10(spectrograma_graficable), cmap='jet')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Power spectral density (dB/Hz)")
    plt.ylim([0, frecuencia_de_muestreo/2.])
    plt.show()


# def grafico_mi_espectrograma(audio_file):
#     # Grafico de espectrograma
#     Fs, audio = read(audio_file)
#     mono_audio = np.mean(audio, axis=1)
#
#     new_audio = np.zeros_like(audio)
#     new_audio[:, 0] = mono_audio
#
#     audio = np.array(audio, dtype=float)
#     audio = audio.T
#
#     ventana = Fs // 10  # 0.1 segundos
#     inicios = np.arange(0, audio.shape[1]-ventana, ventana)
#     idx = np.arange(0, ventana)
#     a = inicios[:, np.newaxis]
#     idxx = a + idx[np.newaxis, :]  # se tiene la cantidad de ventanas
#     Y = audio[0, idxx]
#
#     hann = np.hanning(ventana)[np.newaxis, :]  # ventana de hanning con las dimensiones de nuestras ventanas
#     hann = np.tile(hann, (Y.shape[0], 1))
#     Y_hann = Y*hann
#     Yfft = np.fft.fft(Y_hann, axis=1)
#
#     # Grafico de espectrograma
#     epsilon = 1e-7
#     YfftdB = 20*np.log10(np.abs(Yfft) + epsilon)
#     heatmap = sbn.heatmap(YfftdB[:, 0:22000].T, cmap='jet')
#     cbar = heatmap.collections[0].colorbar
#     cbar.set_label('Densidad espectral de la potencia (dB/Hz)')
#     plt.xlabel("Tiempo (s)")
#     plt.ylabel("Frecuencia (Hz)")
#     plt.gca().invert_yaxis()
#     plt.show()
