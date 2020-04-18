import random
import copy

class Note:
    "Defines a single note."
    
    def __init__(self, pitch, length, beat):
        self.pitch = pitch
        self.length = length
        self.beat = beat
     
    # Name when referenced
    def __repr__(self):
        return f"[{self.pitch}, {self.length}, {self.beat}]"

    # Name when printing
    def __str__(self):
        return f"[{self.pitch}, {self.length}, {self.beat}]"

class Scale:
    "Defining a scale"
    
    def __init__(self, key):
        "Initializes a scale"

        self.scale_tones = [key, key+2, key + 4, key + 5, key + 7, key + 9, key + 11]
        for tone in self.scale_tones:
            tone = tone % 12
        
    def is_in_scale(self, pitch):
        "Check if pitch is in scale."

        if pitch == None:
            return True
        
        for tone in self.scale_tones:
            if pitch % 12 == tone:
                return True
        return False    

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
        beat = 0   
        while beat < 4:
            # Decide pitch of a note
            if beat == 0:
                pitch_tone = scale.scale_tones[0]
            else:
                pitch_tone = random.randrange(-12,15)
                if pitch_tone > 12:
                    pitch_tone = None
                # Make sure all tones are in the correct scale
                while not scale.is_in_scale(pitch_tone):
                    pitch_tone = random.randrange(-12,15)
                    if pitch_tone > 12:
                        pitch_tone = None
                    
            # Decide length of a note        
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
        
        transposed_subject = copy.deepcopy(self.subject_melody)
        
        if fix_height:
            too_high = False
            low = False
        
        for note in transposed_subject:
            # Check if pause
            if note.pitch == None:
                continue
            
            # Transpose to dominant
            note.pitch += steps
            if fix_height:
                if note.pitch > 12:
                    too_high = True
                if note.pitch < 0:
                    low = True
        if fix_height:
            if too_high and not low:
                # Transpose one octave down
                for note in transposed_subject:
                    if note.pitch != None:
                        note.pitch -= 12

        return transposed_subject

    def subject_at_given_beat(self, beat, melody = None):
        "Return a copy of the subject but starting at the wanted beat."
        
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

class Fugue:
    "A fugue consisting of all relevant parts"
    
    def __init__(self, key, random_subject = True, test_nr = None):
        self.key = key
        self.scale = Scale(key)

        self.subject = Subject(self.scale, random_subject, test_nr)
        
        self.first_voice = []
        self.second_voice = []
        self.voices = [self.first_voice, self.second_voice]
        
        # Create first bar with subject in first voice and pause in second voice.        
        bar_pause = Note(None, 4, 0)
        self.first_voice += self.subject.subject_melody
        self.second_voice.append(bar_pause)
        
        
        # Create second bar with answer in second voice. Countersubject comes later.
        self.answer = self.subject.transpose_subject(7,True)
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
        
        stretto_first_voice = self.subject.subject_at_given_beat(beat_first_voice)
        stretto_second_voice = self.subject.subject_at_given_beat(beat_second_voice)
        
        self.first_voice += stretto_first_voice
        self.second_voice += stretto_second_voice

        
    def print_fugue(self):
        "Print both voices of the fugue."
        
        first_voice_sorted = sorted(self.first_voice, key=lambda note: note.beat)
        second_voice_sorted = sorted(self.second_voice, key=lambda note: note.beat)
         
        print(first_voice_sorted)
        print(second_voice_sorted)


key = 0
#fugue = Fugue(key)                  # Use random subject
fugue = Fugue(key, False, 2)        # Use test subject
    
fugue.print_fugue()
