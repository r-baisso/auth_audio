import pyaudio
import wave
import time
from datetime import datetime

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 6

print("Iniciando construcao de dataset de treino")
p = pyaudio.PyAudio()
print("Digite qual tipo de dataset sera gerado")
dataset_type = input("Opcoes (train/test): ")

if dataset_type not in {'train', 'test'}:
    raise Exception("Tipo de dataset nao suportado, tente digitar 'train' ou 'test'")

n = int(input("Insira a quantidade de audios desejada: "))

for i in range(1, n+1):
    WAVE_OUTPUT_FILENAME = f"../media/{dataset_type}/voice_{i}.wav"
    print(f"Preparando gravacao do arquivo {i}")
    time.sleep(1)

    print("A gravacao comeca em")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Comece a falar")
    time.sleep(1)

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()

    print("Gravacao finalizada")

    print(f"Salvando arquivo: {WAVE_OUTPUT_FILENAME}")
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    if i <= n:
        _ = input("Pressione enter para ir para proxima gravacao")
print("Script finalizado")