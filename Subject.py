from Note import Note

import random
import copy

class Subject:
    "The subject of the piece"
    
    def __init__(self, scale, use_random, test_nr = None):
        if use_random:
            self.subject_melody = self.initialize_random_subject(scale)
        else:
            self.subject_melody = self.initialize_test_subject(test_nr)
    
    def initialize_random_subject(self, scale):
        "Creates a subject randomly, one bar long."
        
        self.subject_melody = []
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
            self.subject_melody.append(note)
            
            beat += length_tone
            
        return self.subject_melody

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
        
        self.subject_melody = []
        beat = 0
        for i in range(len(pitch)):
            note = Note(pitch[i], length[i], beat)
            self.subject_melody.append(note)
            beat += length[i]
        
        return self.subject_melody    
    
    def transpose_subject(self, steps, fix_height = False):
        """ Transpose a copy of the subject, fixing so that the highest
        note is not too high if fix_height is set to True.
        """
        
        # Make a deep copy of the subject
        transposed_subject = copy.deepcopy(self.subject_melody)
        
        if fix_height:
            too_high = False
            low = False
            max_height = 12
            min_height = 0
        
        for note in transposed_subject:
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
                for note in transposed_subject:
                    if note.pitch != None:
                        note.pitch -= 12

        return transposed_subject
    
    def inverse_subject(self):
        "Return an inverse of the subject."
        
        # Note: This function should also probably be moved to a melody class
        
        inverse_subject = copy.deepcopy(self.subject_melody)
        starting_pitch = self.subject_melody[0].pitch

        for note in inverse_subject:
            # Check if pause 
            if note.pitch == None:
                continue

            # Invert the melody intervals 
            note.pitch =  2 * starting_pitch - note.pitch
        return inverse_subject

    def subject_at_given_beat(self, beat, melody = None):
        "Return a copy of a melody or the subject, but starting at the wanted beat."
        
        # Note: The melody transposing function should probably be moved to a melody class.
        # The function is used in transposed_subject_at_given_beat though.
        
        if melody == None:
            melody = self.subject_melody
        
        subject_copy = copy.deepcopy(melody)        
        for note in subject_copy:
            note.beat += beat        
        return subject_copy

    def transposed_subject_at_given_beat(self, steps, beat):
        """Return a copy of the subject transposed the given number of steps, 
        with the first note at the wanted beat.
        """
        
        transposed_subject = self.transpose_subject(steps)
        
        transposed_moved_subject = self.subject_at_given_beat(beat, transposed_subject)
        
        return transposed_moved_subject
