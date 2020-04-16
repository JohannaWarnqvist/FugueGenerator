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
        return f"[{self.pitch}, {self.length}]"

    # Name when printing
    def __str__(self):
        return f"[{self.pitch}, {self.length}]"

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


def create_answer(subject):
    "Create a dominant answer to the subject"
    
    answer = copy.deepcopy(subject)
    
    too_high = False
    low = False
    for note in answer:
        # Check if pause
        if note.pitch == None:
            continue
        
        # Transpose to dominant
        note.pitch += 7        
        if note.pitch > 12:
            too_high = True
        if note.pitch < 0:
            low = True
    
    if too_high and not low:
        # Transpose one octave down
        for note in answer:
            if note.pitch != None:
                note.pitch -= 12

    return answer

def initialize_random_subject(scale):
    "Creates a subject randomly, one bar long."
    
    subject = []
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
        subject.append(note)
        
        beat += length_tone
        print(beat)
        
    return subject

def initialize_test_subject(test_nr):
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
    
    subject = []
    beat = 0
    for i in range(len(pitch)):
        note = Note(pitch[i], length[i], beat)
        subject.append(note)
        beat += length[i]
    
    return subject

key = 0
scale = Scale(key)

# When using a test subject:
#subject = initialize_test_subject(1)

# When randomizing the subject:
subject = initialize_random_subject(scale)

answer = create_answer(subject)

print(subject)
print(answer)