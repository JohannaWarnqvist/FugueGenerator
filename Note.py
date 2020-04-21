class Note:
    "Defines a single note."
    
    def __init__(self, pitch, length, beat):
        self.pitch = pitch
        self.length = length    # 1 = quarter note
        self.beat = beat
     
    # Name when referenced
    def __repr__(self):
        return f"[{self.pitch}, {self.length}, {self.beat}]"

    # Name when printing
    def __str__(self):
        return f"[{self.pitch}, {self.length}, {self.beat}]"