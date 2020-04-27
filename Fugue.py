from Scale import Scale
from Melody import Melody
from Melody import Subject
from Note import Note

import random
import copy

class Fugue:
    "A fugue consisting of all relevant parts"

    def __init__(self, key, random_subject = True, test_nr = None):

        # Set scale
        self.key = key
        self.scale = Scale(key)

        # Create the subject
        self.subject = Subject(self.scale, random_subject, test_nr)

        # Initialize voices
        self.first_voice = []
        self.second_voice = []
        self.voices = [self.first_voice, self.second_voice]

        # Create first bar with subject in first voice and pause in second voice.
        bar_pause = Note(None, 4, 0)
        self.first_voice += self.subject.melody
        self.second_voice.append(bar_pause)


        # Create second bar with answer in second voice. Countersubject comes later.
        self.answer = self.subject.transpose(7,True)
        first_note = self.answer[0]
        change_in_beat = 4 - first_note.beat
        for note in self.answer:
            note.beat += change_in_beat
        self.second_voice += self.answer


        # Create development in minor in bar 5 and 6.
        voices_development = copy.deepcopy(self.voices)
        for voice in voices_development:
            for note in voice:
                note.beat += 12
                if note.pitch != None:
                    note.pitch -= 3

        self.first_voice += voices_development[0]
        self.second_voice += voices_development[1]


        # Create stretto in bar 9 and 10.
        beat_first_voice = 4*8
        beat_second_voice = beat_first_voice + 2

        stretto_first_voice = self.subject.melody_at_given_beat(beat_first_voice)
        stretto_second_voice = self.subject.melody_at_given_beat(beat_second_voice)

        self.first_voice += stretto_first_voice
        self.second_voice += stretto_second_voice


    def print_fugue(self):
        "Print both voices of the fugue."

        first_voice_sorted = sorted(self.first_voice, key=lambda note: note.beat)
        second_voice_sorted = sorted(self.second_voice, key=lambda note: note.beat)

        print(first_voice_sorted)
        print(second_voice_sorted)
