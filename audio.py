import numpy as np
import pyaudio


class Input:
    def __init__(self):
        self.BUFFER_SIZE = 8820
        self.SAMPLE_RATE = 44100
        self.REF_FREQ = 440 # A4
        self.REF_OCTAVE = 4
        self.REF_SEMITONE = 57 # Number of semitones of A4 from first
        # b := flat; # := sharp
        self.notes = ["A","A#|Bb","B","C","C#|Db","D","D#|Eb","E","F","F#|Gb","G","G#|Ab"]

    """
    Returns the frequency(float), note(str), and octave(int).
    """
    def get_musical_values(self):
        in_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, 
                                           rate=self.SAMPLE_RATE, input=True, 
                                           frames_per_buffer=self.BUFFER_SIZE)

        freqs = np.linspace(0, self.SAMPLE_RATE / 2, (self.BUFFER_SIZE // 2) + 1)

        window = np.hanning(self.BUFFER_SIZE)
        t_domain_amps = np.frombuffer(in_stream.read(self.BUFFER_SIZE), 
                                                     dtype=np.int16) * window
        f_domain_amps = np.abs(np.fft.rfft(t_domain_amps))

        freq_idx = np.argmax(f_domain_amps)
        frequency = freqs[freq_idx]
        
        semitone_offset = np.nan
        # Cannot calculate log of 0
        if (frequency != 0):
            # Number of semitones from A4
            semitone_offset = round(np.log2(frequency / self.REF_FREQ) * 12)

        octave = 0
        note = ""
        if semitone_offset is not np.nan:
            note_idx = semitone_offset % 12
            note = self.notes[note_idx]

            octave = (self.REF_SEMITONE + semitone_offset) // 12

        if octave < 0: octave = 0

        return frequency, note, octave


if __name__ == "__main__":
    input = Input()
    while True:
        f, n, o = input.get_musical_values()
        print(f"Freq: {f}; Note: {n}; Octave: {o}")