from Note import Note
from Scale import Scale

import random
import copy

class Melody:
    def __init__(self):
        self.melody=melody

    def transpose(self, steps, fix_height = False):
        """ Transpose a copy of the melody, fixing so that the highest
        note is not too high if fix_height is set to True.
        """

        # Make a deep copy of the subject
        transposed_melody = copy.deepcopy(self.melody)

        if fix_height:
            too_high = False
            low = False
            max_height = 12
            min_height = 0

        for note in transposed_melody:
            # Check if pause
            if note.pitch == None:
                continue

            # Transpose the wanted number of steps
            note.pitch += steps
            if fix_height:
                if note.pitch > max_height:
                    too_high = True
                if note.pitch < min_height:
                    low = True
        if fix_height:
            if too_high and not low:
                # Transpose one octave down
                for note in transposed_melody:
                    if note.pitch != None:
                        note.pitch -= 12
        return transposed_melody


    def inverse(self):
        """Return an inverse of the melody. Does not yet take tonality into
        consideration """

        inverse_melody = copy.deepcopy(self.melody)
        starting_pitch = self.melody[0].pitch

        for note in inverse_melody:
            # Check if pause
            if note.pitch == None:
                continue

            # Invert the melody intervals
            note.pitch =  2 * starting_pitch - note.pitch
        return inverse_melody

    def melody_at_given_beat(self, beat, melody = None):
        "Return a copy of a melody, but starting at the wanted beat."

        if melody == None:
            melody = self.melody

        melody_copy = copy.deepcopy(melody)
        for note in melody_copy:
            note.beat += beat
        return melody_copy

    def transposed_melody_at_given_beat(self, steps, beat):
        """Return a copy of the melody transposed the given number of steps,
        with the first note at the wanted beat.
        """

        transposed_melody = self.transpose(steps)

        transposed_moved_melody = self.melody_at_given_beat(beat, transposed_melody)

        return transposed_moved_melody

    def pitch_at_given_beat(self, beat):
        "Returns the melody pitch at a given beat. Useful for writing harmonies"

        # Jag tänkte använda den här funktonen på ett annat ställe, men
        # blev inte klar / lyckades inte. Sparade den här iallafall, om den
        # behövs någon annanstans

        i = 0
        while beat >= self.melody[i].beat:
            i += 1
            if i>=len(self.melody):
                break

        return self.melody[i-1].pitch

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
