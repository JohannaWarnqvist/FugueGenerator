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