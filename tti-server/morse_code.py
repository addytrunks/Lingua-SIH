import numpy as np
import scipy.io.wavfile as wav
import io

SAMPLE_RATE = 44100
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '@': '.--.-.', ' ': '/'
}


def text_to_morse_code(text):
    text = text.upper()
    morse_code = ' '.join(MORSE_CODE_DICT.get(char, '') for char in text)
    return morse_code


def morse_code_to_audio(morse_code, dot_length=0.1, frequency=1000):
    def create_signal(frequency, duration):
        t = np.linspace(0, duration, int(
            SAMPLE_RATE * duration), endpoint=False)
        return 0.5 * np.sin(2 * np.pi * frequency * t)

    audio_signal = np.array([])

    for char in morse_code:
        if char == '.':
            audio_signal = np.concatenate(
                [audio_signal, create_signal(frequency, dot_length)])
        elif char == '-':
            audio_signal = np.concatenate(
                [audio_signal, create_signal(frequency, 3 * dot_length)])
        elif char == ' ':
            audio_signal = np.concatenate(
                [audio_signal, np.zeros(int(SAMPLE_RATE * dot_length))])
        elif char == '/':
            audio_signal = np.concatenate(
                [audio_signal, np.zeros(int(SAMPLE_RATE * dot_length * 3))])
        audio_signal = np.concatenate(
            [audio_signal, np.zeros(int(SAMPLE_RATE * dot_length / 2))])
    return audio_signal


def translate_morse_code(text):
    morse_code = text_to_morse_code(text)
    stream = io.BytesIO()
    wav.write(stream, SAMPLE_RATE, (morse_code_to_audio(
        morse_code) * 32767).astype(np.int16))
    return morse_code, stream.read()
