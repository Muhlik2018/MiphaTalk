import pyaudio
import webrtcvad
import numpy
import wave
import struct
import math

# Initialize VAD
vad = webrtcvad.Vad()
vad.set_mode(0)  # 0: Aggressive filtering, 3: Less aggressive

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 320
SHORT_NORMALIZE = (1.0/32768.0)
RECORD_SECONDS = 3



# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )


def is_speech(frame, sample_rate):
    return vad.is_speech(frame, sample_rate)

def record_audio():
    frames = []
    recording = False

    print("Listening for speech...")
    while True:
        frame = stream.read(CHUNK)
        amplitutde=get_rms(frame)
        # print(frame)
        if is_speech(frame, RATE) and amplitutde>0.1:
            print(amplitutde)
            if not recording:
                print("Recording started")
                recording = True
            frames.append(frame)
            for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
                frame = stream.read(CHUNK)
                frames.append(frame)
            break


        # else:
            # if recording:
                # print("Silence detected, stopping recording.")
                # break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames

def save_audio(frames, filename="output.wav"):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Example usage
frames = record_audio()
save_audio(frames)
print("Audio saved as output.wav")