import mingus.core.notes as notes
from mingus.containers import Bar
from mingus.containers import NoteContainer
import mingus.core.intervals as intervals

import mingus.extra.lilypond as LilyPond
from Mingus_LilyPond_helper import to_LilyPond_file
from mingus.midi import midi_file_out



print(notes.is_valid_note("C"))
print(notes.is_valid_note("D#"))
print(notes.is_valid_note("Eb"))

print(notes.note_to_int("C"))   #0
print(notes.note_to_int("Db"))  #1
print(notes.note_to_int("C#"))  #1

print(notes.int_to_note(1))     #C#

print(notes.augment("C"))
print(notes.augment(notes.int_to_note(0)))

print("This " + intervals.determine("D","C"))

b = Bar()
b + "C"
b + "E"
b + "G"
b + "B"

print(LilyPond.from_Bar(b))
bar = LilyPond.from_Bar(b)
to_LilyPond_file(bar,"lilytest")

nc = NoteContainer(["A", "C", "E"])
midi_file_out.write_NoteContainer("real_juice.mid", nc)
midi_file_out.write_Bar("real_juice.mid", b)

#inverse function that inverses based on half note values - wasn't what you were supposed to do apparently 
def inverse(track):
    # Copy value of reference to aviod problems with overwriting 
    inversed_track = copy.deepcopy(track)

    #generator
    input_notes = inversed_track.get_notes()
    #note[-1] is a note container
    #note[-1][0] is a note

    #take out the first note from the "note container" generator
    start_note = next(input_notes)[-1][0]

    for bar in input_notes:
        nc = bar[-1]
        if nc is None:
             continue
        else:
            for note in nc:
                temp = Note.measure(start_note,note)
                Note.from_int(note,int(start_note) + (-1)*temp)
    
    #return inversed track
    return inversed_track


