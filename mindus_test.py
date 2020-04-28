import mingus.core.notes as notes
from mingus.containers import Bar
from mingus.containers import NoteContainer

import mingus.extra.lilypond as LilyPond
from Mindus_LilyPond_helper import to_LilyPond_file
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




