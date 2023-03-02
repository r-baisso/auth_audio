import pyaudio
import wave
import os
import time
import pickle as pkl

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 6
WAVE_OUTPUT_FILENAME = "voice.wav"
WAVE_OUTPUT_FILEPATH = f"../media/production/{WAVE_OUTPUT_FILENAME}"

print('Starting auth audio app')

p = pyaudio.PyAudio()

while True:
    print("Setting up the audio stream")
    stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Recoding audio")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print()
    stream.stop_stream()
    stream.close()
    # p.terminate()
    print("Audio recorded")

    print(f"Saving audio to file: {WAVE_OUTPUT_FILEPATH}")
    wf = wave.open(WAVE_OUTPUT_FILEPATH, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Audio Saved")

    with open('../model/rbaisso_model_20230302.pkl', 'rb') as file:
        aa = pkl.load(file)

    print("F0 reference =", aa.user_m0)
    print("User Authentication =", aa.predict(WAVE_OUTPUT_FILEPATH, RATE))
    time.sleep(1.5)
    print()