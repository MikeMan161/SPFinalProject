import numpy as np
import pyaudio
from scipy import windows


class Input:
    def __init__(self):
        self.BUFFER_SIZE = 2048
        self.SAMPLE_RATE = 44100

    """
    Returns the frequency(float), note(str), and octave(int).
    """
    def get_input_values(self):
        in_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, 
                                           rate=self.SAMPLE_RATE, input=True, 
                                           frames_per_buffer=self.BUFFER_SIZE)

        window = windows.blackmanharris(self.buffer_size)
        freqs = np.linspace(0, self.sample_rate / 2, (self.buffer_size // 2) + 1)

        t_domain_amps = np.frombuffer(in_stream.read(self.buffer_size), 
                                      dtype=np.int16) * window
        f_domain_amps = np.abs((np.fft.rfft(t_domain_amps)))
        f_domain_dB_amps = self.to_dB_and_filter(f_domain_amps)


        frequency = 0
        note = 0
        octave = 0
        return frequency, note, octave