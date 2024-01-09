import numpy as np
from scipy import signal

num_picos = 15  # numero de picos que consdiramos en cada ventana


def datos_espectrograma(audio, Fs):
    # Parametros
    longitud_ventana_segundos = 0.5  # Segundos por ventana
    muestras_por_ventana = int(longitud_ventana_segundos * Fs)  # Muestras de la ventana
    # El modulo es simplemente para que la transformada discreta de fourier sea mas eficiente
    muestras_por_ventana += muestras_por_ventana % 2

    # Ajustamos las ventanas de muestreo para que sean parejas a las muestras de la cancion
    ajuste = muestras_por_ventana - audio.size % muestras_por_ventana
    if audio.ndim > 1:  # si el audio tiene mas de un canal, lo promediamos
        audio = np.mean(audio, axis=1)
    song_input = np.pad(audio, (0, ajuste))

    # Realizamos la transformada discreta de fourier
    frecuencias, tiempos, stft = signal.stft(
        song_input, Fs, nperseg=muestras_por_ventana, nfft=muestras_por_ventana, return_onesided=True
    )
    return stft, frecuencias, tiempos


def crear_constelacion(audio, Fs):
    # stft, frecuencias, tiempos = graficador.grafico_mi_espectrograma(audio, Fs)[:3]  # solo nos interesa el stft y las frecuencias
    stft, frecuencias, tiempos = datos_espectrograma(audio, Fs)[:3]  # solo nos interesa el stft y las frecuencias
    mapa_constelaciones = []

    for indice_tiempo, ventana in enumerate(stft.T):
        # El espectrograma nos da numeros complejos 
        # Tomamos solo los reales
        spectrum = abs(ventana)
        # Encontramos los picos que son mas importantes, la distancia es para no considerar picos muy cerca de otros
        picos, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        # Nos interesa solo los 15 picos mas importantes

        # tomamos los picos deseados o los picos que hay
        n_picos = min(num_picos, len(picos))
        
        picos_altos = np.argpartition(props["prominences"], -n_picos)[-n_picos:]  # los indices de los picos mas grandes
        for pico in picos[picos_altos]: 
            frecuencia = frecuencias[pico]
            mapa_constelaciones.append([indice_tiempo, frecuencia])  # agregamos el tiempo y la frecuencia del pico relevante

    return mapa_constelaciones
