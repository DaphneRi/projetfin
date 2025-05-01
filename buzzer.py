from machine import Pin, PWM
from time import sleep

# Fréquences des notes (en Hz)
NOTES = {
    "A": 440, "A#": 466, "B": 494,
    "C": 523, "C#": 554, "D": 587, "D#": 622, "E": 659,
    "F": 698, "F#": 740, "G": 784, "G#": 830
}

# Mélodie de l'Imperial March (notes et durées)
IMPERIAL_MARCH = [
    ("A", 0.5), ("A", 0.5), ("F", 0.35), ("C", 0.15), ("A", 0.5),
    ("F", 0.35), ("C", 0.15), ("A", 1),
    ("E", 0.5), ("E", 0.5), ("F", 0.35), ("C", 0.15), ("G#", 0.5),
    ("F", 0.35), ("C", 0.15), ("A", 1),
    ("A#", 0.5), ("A", 0.35), ("A", 0.15), ("A#", 0.5), ("G#", 0.25), ("G", 0.25),
    ("F", 0.15), ("C", 0.15), ("A", 0.5),
    ("F", 0.35), ("C", 0.15), ("A", 1)
]

class Buzzer:
    def __init__(self, pin):
        """Initialise le buzzer sur la broche spécifiée."""
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty_u16(1000)  # Volume réglé à haute intensité

    def play_tone(self, freq, duration):
        """Joue une note à une fréquence donnée pendant une durée en secondes."""
        if freq == 0:  # Pause (silence)
            self.buzzer.duty_u16(0)
        else:
            self.buzzer.freq(freq)
            self.buzzer.duty_u16(1000)  # Ajuste le volume
        sleep(duration)
        self.buzzer.duty_u16(0)  # Arrête le son entre les notes
        sleep(0.05)  # Pause courte entre les notes

    def play_song(self, song):
        """Joue une liste de notes avec leurs durées."""
        for note, duration in song:
            freq = NOTES.get(note, 0)  # Cherche la fréquence ou met 0 (silence)
            self.play_tone(freq, duration)

    def stop(self):
        """Arrête le buzzer."""
        self.buzzer.duty_u16(0)

# Initialisation du buzzer sur la broche 22
buzzer = Buzzer(22)

# Joue le thème de Dark Vador !
buzzer.play_song(IMPERIAL_MARCH)

# Arrêt du buzzer
buzzer.stop()


