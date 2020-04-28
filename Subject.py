from Note import Note
from Scale import Scale
from Melody import Melody

import random
import copy

class Subject(Melody):
    "The subject of the piece"

    def __init__(self, scale, use_random, test_nr = None):
        if use_random:
            self.melody = self.initialize_random_subject(scale)
        else:
            self.melody = self.initialize_test_subject(test_nr)

    def initialize_random_subject(self, scale):
        "Creates a subject randomly, one bar long."

        self.melody = []
        min_pitch = -12
        max_pitch = 12

        beat = 0
        while beat < 4:
            # Decide pitch of a note
            if beat == 0:
                # Set first note in subject to root note
                pitch_tone = scale.scale_tones[0]
            else:
                pitch_tone = random.randrange(min_pitch,max_pitch+3)
                if pitch_tone > max_pitch:
                    pitch_tone = None
                # Make sure all tones are in the correct scale
                while not scale.is_in_scale(pitch_tone):
                    pitch_tone = random.randrange(min_pitch,max_pitch+3)
                    if pitch_tone > max_pitch:
                        pitch_tone = None

            # Decide length of a note, length 1 = quarter note. Max half note or what is left in bar if less than half note.
            length_tone = 0.25*random.randrange(1,min(16-(beat*4),8)+1)

            # Create note object at the current beat
            note = Note(pitch_tone, length_tone, beat)

            # Add note to subject
            self.melody.append(note)

            beat += length_tone

        return self.melody

    def initialize_test_subject(self, test_nr):
        "Creates a subject from the chosen test case."

        if test_nr == 0:
            pitch = [0,0,4,7,None,7]
            length = [1, 0.5, 0.5, 0.5, 0.5, 1]
        elif test_nr == 1:
            pitch = [0, 2, 2, -3, -1, None, -8]
            length = [1.5, 0.25, 0.25, 0.25, 1.25, 0.25, 0.25]
        else:
            pitch = [0,1,2,3]
            length= [1,1,1,1]

        self.melody = []
        beat = 0
        for i in range(len(pitch)):
            note = Note(pitch[i], length[i], beat)
            self.melody.append(note)
            beat += length[i]

        return self.melody


    # Nedan är ett försök till countersubjekt-"skal" med "bra" stämtoner
    # på slagen.

    # def countersubject(self,scale):
    #     countersubject = []
    #     scale = Scale(scale)              # dåligt försök till att få den att fatta vilken tonart som gäller
    #     for i in range(0,4):
    #         a = random.randint(0,1)
    #         if a == 0: # använd ters
    #             pitch = self.pitch_at_given_beat(i) - 3
    #         else: # använd sext
    #             pitch = self.pitch_at_given_beat(i)-8
    #
    #         if not(scale.is_in_scale(pitch)):
    #             pitch = pitch -1          # default är liten ters&sext. ändra till stor om det behövs.
    #                                       # funkar i dur&moll.
    #         print(pitch)
    #         note = Note(pitch,1,i)
    #         countersubject.append(note)
