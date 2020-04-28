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

