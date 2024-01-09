from crear_constelacion import crear_constelacion
from crear_hashes import crear_hashes
from scipy.io import wavfile
from encontrar_cancion import puntuar_canciones
import pickle
import graficador
import crear_database
import pyaudio
import wave


if __name__ == "__main__":
    # variables para grabar audio
    chunk = 1024
    formato = pyaudio.paInt16
    canales = 2
    ratio = 44100
    segundos = 15

    p = pyaudio.PyAudio()

    stream = p.open(format=formato,
                    channels=canales,
                    rate=ratio,
                    input=True,
                    frames_per_buffer=chunk)

    print('grabando...')

    frames = []

    for i in range(0, int(ratio / chunk * segundos)):
        data = stream.read(chunk)
        frames.append(data)

    print('grabación terminada')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open('grabacion.wav', 'wb')
    wf.setnchannels(canales)
    wf.setsampwidth(p.get_sample_size(formato))
    wf.setframerate(ratio)
    wf.writeframes(b''.join(frames))
    wf.close()

    # crear_database.crear_base_de_datos()
    Fs, audio_input = wavfile.read('grabacion.wav')
    constelacion = crear_constelacion(audio_input, Fs)
    hashes = crear_hashes(constelacion)
    database = pickle.load(open('database.pickle', 'rb'))
    canciones_indexadas = pickle.load(open("dic_canciones.pickle", "rb"))
    puntajes = puntuar_canciones(hashes, database)

    if puntajes is None:
        print("No se encontro ninguna cancion")
        graficador.graficador_espectrograma("canciones/Thats so raven.wav")
        exit()

    cancion_mas_probable = puntajes[0][0]  # el primer item es el que tiene mas aciertos

    print("Cancion con mas aciertos: " + canciones_indexadas[cancion_mas_probable].split('\\')[-1].split('.')[0])

    # graficador.graficar_espectrograma('prueba.wav')
    # graficador.graficar_constelacioin('prueba.wav')

    # graficador.graficar_constelaciones(canciones_indexadas[cancion_mas_probable]
    # graficaor.graficar_espectrograma(canciones_indexadas[cancion_mas_probable])
    # graficador.graficar_constelaciones(canciones_indexadas[cancion_mas_probable])
