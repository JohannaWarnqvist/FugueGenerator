class Scale:
    "Defining a scale"
    
    def __init__(self, key):
        "Initializes a scale"

        self.key = key
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
        
    def get_part_of_scale(self, lowest_pitch, highest_pitch):
        pitch_list = [pitch for pitch in range(lowest_pitch, highest_pitch+1)]
        
        i = 0
        while i < len(pitch_list):
            pitch_in_scale = self.is_in_scale(pitch_list[i])
            if not pitch_in_scale:
                pitch_list.pop(i)
            else:
                i += 1
        
        return pitch_list
            
                
    