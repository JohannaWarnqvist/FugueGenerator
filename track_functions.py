#---------------------------------------------
#In this file we create different functions that modify Tracks that can later be used to 
# modify subject in main 
#---------------------------------------------

from mingus.containers import Track
from mingus.containers import Bar
from mingus.containers import NoteContainer
from mingus.containers import Note
import mingus.core.intervals as intervals
import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.keys as keys
import mingus.midi.midi_file_in as midi
import copy
import random


#--------------------------------------------------------------------
#HELPER FUNCTIONS FOR TRACK OPERATIONS 
#--------------------------------------------------------------------

#adds two tracks to make a sequence 
def add_tracks(track1, track2):
    for i in range(len(track2)):  
        track1.add_bar(track2[i])

# Merges two tracks (One track where both are played simultaneously)
#Tracks do not have to be of the same length
#Ev. problem Notes cannot overlap, notes that do overlap are cut to fit 
def merge_tracks(track1,track2):
    merged_track = Track()
    #Copy inputs to prevent overwriting
    track1_notes = copy.deepcopy(track1).get_notes()
    track2_notes = copy.deepcopy(track2).get_notes()
    
    #Bool that indicates if we should read in the next note in track2
    next_note2 = True

    for note1 in track1_notes:
        #Bool that indicates if we should read in the next note in track1
        next_note1 = False

        #If we want to read in the next note in track 2 attempt to do so
        if next_note2:
            try:
                note2 = next(track2_notes)
            #If generator is empty(we have already added all notes from track 2) just add the next note from track1
            except StopIteration:
                merge_tracks.add_notes(note1[-1],note1[1])
                continue
        
        #While loop to check if we have added the current note1
        while(not next_note1):
            #In this part we compare the current note from track1 (note1) and current node from track2(note2)

            #If notes start at the same time
            if note1[0] == note1[0]:
                #Determine the added notecontainer value, if any of the notes is a oause add the value of the other note
                if note1[-1] is None:
                    nc = note2[-1]
                elif note2[-1] is None:
                    nc = note1[-1]
                else:
                    nc = note1[-1] + note2[-1] 

                # if the notes have different length always use the shortest one
                if note1[1] > note2[1]:
                    merged_track.add_notes(nc,note2[1])
                else:
                    merged_track.add_notes(nc,note1[1])
                
                next_note1 = True #read in next note from track1
                next_note2 = True #read in next note from track2

            #If note1 starts before note2
            elif note1[0] < note2[0]:
                #Determine time until next note in track2
                time_to_next = int(1.0/(note2[0] - note1[0]))

                #If length of note1 is bigger than time until next note in track2 then cut lenght to fit
                if note1[1] > time_to_next:
                    merged_track.add_notes(nc,time_to_next)
                    
                #Otherwise add note as normal
                else: 
                    merged_track.add_notes(nc,note1[1])

                next_note1 = True  #read in next note from track1
                next_note2 = False #do not read in next note from track2

            #If note2 starts before note1
            else:
                #If length of note2 is bigger than time until next note in track1 then cut lenght to fit
                temp = int(1.0/(note1[0] - note2[0]))
                if note2[1] > temp:
                    merged_track.add_notes(nc,temp)
                else: 
                    merged_track.add_notes(nc,note2[1])
                
                next_note2 = True #read in next note from track2
                                  #do not read in next note from track1 (default)

    #Add remaining notes if any from track2
    for note2 in track2_notes:
        merged_track.add_notes(note2[-1],note2[1])

    return merged_track

#--------------------------------------------------------------------
#INPUT 
#Turns a list of tuples (note name, dote duration) into a usable track
# Note, you must fill each bar individually otherwise the note will cut to fit bar
# You can add pauses by setting note name to None
#ex input [("C",2),("D",4),("F",4),("G",1)]
#TODO look into midi input
#--------------------------------------------------------------------
def input_list(list_of_note_tuples):
    #track to return
    track = Track()

    #For every tuple in input
    for (name,duration) in list_of_note_tuples:

        #If we can't add note (duration is too long)
        if not (track.add_notes(name, duration)):
            #Calculate new duration to fit bar and add note
            space_left = track[-1].space_left()
            track.add_notes(name, int(1.0/space_left))

    return track

def input_midi(midi_file):
    track = Track()
    midi.MIDI_to_Composition(midi_file)
    print(midi.MIDI_to_Composition(midi_file))
    return track

#with open('final_fugue.mid', 'r') as f:
#    input_midi(f)

#--------------------------------------------------------------------
#INIT PRESETS
#TODO: Write better and more thought out presets for testing 
#--------------------------------------------------------------------
def init_preset_track(num):
    track = Track()
    if num==1: #C-chord
        track.add_notes(None)
        track.add_notes(None)
        nc = NoteContainer(["C","E"])
        track.add_notes(nc)
        track + "E-5"
        track + "A-3"
        track.add_notes(None)
        track + "C-5"
        track + "E-5"
        nc2 = NoteContainer(["F","G"])
        track.add_notes(nc2)
        track + "G-5"
        track + "C-6"
    if num==2:
        track + "C"
        track + "D"
        track + "E"
        track + "A-2"
        track + "C"
        track + "D"
        track + "E"
        track + "F-5"
        track + "D"
        track + "E"
        track + "E-5"
    if num ==3:
        test_scale = scales.Major("C")
        for i in range(7):
            track + test_scale[i]
    return track


# Helper function
def get_interval_from_halfnotes(nmb_of_halfnotes):
    "Function that translates number of halfnotes to an interval known to the transpose function."
    lookup = ["b2"," 2","b3"," 3", " 4", "#4", " 5", "b6", " 6", "b7", " 7"]
    interval = lookup[abs(nmb_of_halfnotes)-1]
    return interval

#--------------------------------------------------------------------
# More info on Mingus web page under intervals - intervals from shorthand
#--------------------------------------------------------------------

#alt method using nmb_of_halfnotes (an int) as input
def transpose_from_halfnote(track,nmb_of_halfnotes,up = True):
    #breakpoint()
    octave_change = 0
    if nmb_of_halfnotes > 11:
        octave_change = nmb_of_halfnotes // 12
        nmb_of_halfnotes = nmb_of_halfnotes - 12*octave_change
        
        

    if nmb_of_halfnotes != 0:
        #determine interval from nmb_of_steps
        interval = get_interval_from_halfnotes(nmb_of_halfnotes)
        
        # Use transpose_track to get a transposed copy of the track
        transposed_track = transpose(track, interval, up)
    else:
        transposed_track = copy.deepcopy(track)
        
    if octave_change != 0:
        notes_input = transposed_track.get_notes()
        for note_description in notes_input:
            note_construction = note_description[-1]
            if note_construction is None:
                continue
            else:
                for note in note_construction:
                    note.change_octave(octave_change)
    
    # Return transposed track
    return transposed_track

# A start to a function to use in bar 5 and 6. Does not yet actually do anything.
# When done, it should be able to transpose a melody from C major to A minor

def transpose_to_relative_minor(track, original_key, harmonic):
    transposed_track = copy.deepcopy(track)
    if original_key in keys.major_keys:
        old_scale = keys.get_notes(original_key)
        new_key = keys.relative_minor(original_key)
        new_scale = keys.get_notes(new_key)
        
        if harmonic:
            new_scale[6] = notes.augment(new_scale[6])
            new_scale[6] = notes.reduce_accidentals(new_scale[6])
        
        
        input_notes = transposed_track.get_notes()
        for bar in input_notes:

            #Check if the nc contained in the bar/"note" is a pause, then do nothing
            nc = bar[-1]
            if nc is None:
                continue
            
            #Otherwise
            else:
                #For every actual note in the note containers (important if there is a chord)
                for note in nc:
                    if note.name in old_scale:
                        index = old_scale.index(note.name)
                        note.name = new_scale[index]
                    else:
                        note.transpose("b3")
                        note.name = notes.reduce_accidentals(note.name)
    else:
        print("input key is not major key")   
    return transposed_track

#TEST for Transpose to relative minor 

def transpose(track, interval, up):
    "Return a copy of the track, transposed the given interval up if up = True, otherwise down."
    
    # Copy value of reference to aviod problems with overwriting    
    transposed_track = copy.deepcopy(track)
    
    # Calculate transposed track
    input_notes = transposed_track.get_notes()
    for note in input_notes:
        # Try to check if the note container is None. If not, transpose it.
        # note is technically a note container, might be good to know sometime.
        if note[-1] is None:
                continue                    
        else:
            note[-1].transpose(interval, up)
    
    # Return transposed track
    return transposed_track


      
#--------------------------------------------------------------------
#REVERSE DONE
#Returns an copied and reversed track of input track
#--------------------------------------------------------------------
def reverse(track):
    # Copy value of reference to aviod problems with overwriting    
    input_track = copy.deepcopy(track)
    #empty track to write to later
    reversed_track = Track()

    #create a reversed list of notes from input track
    input_notes = input_track.get_notes()
    reversed_notes = reversed(list(input_notes))
    
    #Add notes to reversed_track
    for note in reversed_notes:
        reversed_track.add_notes(note[-1])

    # Return reversed track
    return reversed_track

#--------------------------------------------------------------------
#INVERSE - IN PROGRESS
#TODO Add the right accidentals to the notes depending on the scale
#returns a copied and inverted track of input track. Inverts around the starting note of the input track
#--------------------------------------------------------------------
def inverse(track):
    # Copy value of reference to aviod problems with overwriting 
    inversed_track = copy.deepcopy(track)

    #"note" generator
    input_notes = inversed_track.get_notes()
    #note[-1] is a note container
    #note[-1][0] is a note

    #take out the first actual note from the "note" generator
    start_note = next(input_notes)[-1][0]

    #save the note name value without axidentals for camparison with the scale string
    base_note_value = start_note.name[0]

    #create a string with the ordered notes from the cmaj scale starting from the note after 
    #the base_note_value until the base_note_value is read again. This is used to calculate the
    #inversed notes later on
    Cmaj_scale = "CDEFGABCDEFGAB"
    scale = Cmaj_scale.split(base_note_value)[1]

    #Its not pretty nut it seems to work
    #For every bar/"note" we get out of the note generator
    for bar in input_notes:

        #Check if the nc contained in the bar/"note" is a pause, then do nothing
        nc = bar[-1]
        if nc is None:
             continue
        
        #Otherwise
        else:
            #For every actual note in the note containers (important if there is a chord)
            for note in nc:

                #initial value for an offset variable 
                diff = 0

                #If the note doesn't have the same note name (eg. "C" or "D") as the base note 
                #We calculate how many steps in the major scale we have to take to find 
                # A note that corresponds the one we have without accidentals. 
                # (eg. base_note_val ="C", note = "Eb" we have to take 2 steps to find "E" in Cmaj)
                if not (note.name[0] == base_note_value):
                    diff = scale.index(note.name[0]) + 1

                #Calculation of octave, a little messy but works    
                if base_note_value == "C":
                    if note.name[0] == "C":
                        note.octave = start_note.octave + (start_note.octave - note.octave)
                    else:
                        note.octave = start_note.octave + (start_note.octave - note.octave - 1)

                else:
                    if note.name[0] == "C" or scale.index("C") == (6-diff):
                        note.octave = start_note.octave + (start_note.octave - note.octave + 1)
                    else:
                        note.octave = start_note.octave + (start_note.octave - note.octave)
                
                #Use offset to assign the note the correct note value in C-maj
                if not (note.name[0] == base_note_value):
                    note.name = scale[-diff]
                else:
                    note.name = base_note_value
                
                #TODO Add the right accidentals to the notes depending on the scale
                
                
    #return inversed track
    return inversed_track       

#--------------------------------------------------------------------
#INIT RANDOM (1-BAR) TRACK
# Can be used to initalize a random subject, if is_subject is set to True. This gives a random bar that
# starts on the root note of the key. 
#--------------------------------------------------------------------
# Limitations (intended and uninteded) so far:
#   - duration is either half, quarter or eigth note. This is set to create a 'meaningful' melody.
#   there could be more options but it should probably be weighed towards these values
#   - the pitch range is only root to 7th. maybe it would be better to center the range around the root note
#   - the randomization is uniform
#   - it can't generate any pauses
#   - it only returns a single bar (useful for subjects but we might want to create longer random tracks ?)
# ----------------------------------
def init_random_track(key, is_subject):
    notes = keys.get_notes(key)
    bar = Bar()
    while bar.current_beat < 1 :
        # Randomize pitch and duration of each note. 
        duration = 2**random.randint(1,3)
        pitch = notes[random.randint(0,6)] 
        
        # If it is intened to be a subject, set the first note to the root.
        if bar.current_beat == 0 and is_subject == True:
            pitch = notes[0]
        
        # If the randomized duration doesn't fit in the bar, make it fit
        if 1/duration > 1 - bar.current_beat:
            duration = 1 / (1- bar.current_beat)
        
        # Place the new note in the bar
        bar.place_notes(pitch, duration)
    
    # Create a track to contain the randomized bar
    track = Track()
    track + bar
    
    # Return the track
    return track


#--------------------------------------------------------------------
#CHANGE-SPEED DONE
# Changes the speed of a track 
# up = true if you want to speed up, up = False if you want to slow down
# factor determines how much to speed up / slow down if factor = 2 we will either dubbel of half the speed 
#--------------------------------------------------------------------
def change_speed(track, factor, up=True):
    changed_track = Track()
    #if factor is 0 we return an empty track
    if (factor != 0.0) : 

        input_track = copy.deepcopy(track)
        input_notes = input_track.get_notes()

        #if we want to speed up (notespeed *= factor)
        if up:
            for note in input_notes:
                changed_track.add_notes(note[-1],int(note[1]*factor))

        #if we want to slow down (notespeed *= (1/factor))
        else:
            for note in input_notes:
                changed_track.add_notes(note[-1], int(note[1]/factor))
                

    return changed_track    

#--------------------------------------------------------------------
# SHIF DONE
# Shifts a track for the pause duration and returns a copied and shifted track
# Used for canon
#--------------------------------------------------------------------
def shift(track, pause_duration):
    shifted_track = Track()
    
    bar = Bar()
    bar.place_rest(pause_duration)
    input_note_containers = track.get_notes()
    
    for note in input_note_containers:
        placed = bar.place_notes(note[-1], note[1])
        if not placed:
            beat_left = 1.0 - bar.current_beat
            beats_part_1 = beat_left
            beats_part_2 = 1/note[1] - beats_part_1
            
            if beats_part_1 != 0:
                duration_part_1 = 1/beats_part_1
                bar.place_notes(note[-1], duration_part_1)

            shifted_track.add_bar(copy.deepcopy(bar))
            
            bar = Bar()
            
            duration_part_2 = 1/beats_part_2
            
            bar.place_notes(note[-1], duration_part_2)

    shifted_track.add_bar(copy.deepcopy(bar))

    return shifted_track


# ---------------------------------------------
# CREATE ANSWER
# This function handles leaps from the root to the fifth, if there are any, in the subject before transposing
# to the dominant. Such leaps are ok in the subject but should apparantly be avoided in the answer. (This is called tonal answer). 
# ---------------------------------------------
def create_answer(track, key):
    # First look for any perfect fifth leaps from the root note in the melody
    # If found, diminsh the fifth to a fourth before transposing
    
    track_copy = copy.deepcopy(track)
    for i in range(len(track_copy[0])-1):
        note1 = track_copy[0][i][2][0].name      # This monstrosity is the note name
        if note1 == key:                    
            note2 = track_copy[0][i+1][2][0].name
            interval = intervals.determine(note1,note2)
            if interval == 'perfect fifth':
                track_copy[0][i+1][2][0].transpose('2',False)

    answer = transpose_from_halfnote(track_copy,7,up=True)    
    return answer


# -------------------------------------------------------
# PITCH_AT_GIVEN_BEAT
# Returns a note container with the pitch of the note at the beat, or if there is no note exactly on the beat, the one before.
# Useful for testing harmonies later on
# -------------------------------------------------------
def pitch_at_given_beat(track, beat):
    """Returns the melody pitch at a given beat. Accepts beat as an int. Assumes beats start on 0. Assumes 4/4 time.
    Example: Beat 3 = bar 0, beat 3. Beat 5 = bar 1, beat 1."""

    # A study in python divison operators, to locate the given beat in the track.
    bar_no = beat // 4
    beat_in_bar = (beat % 4) / 4

    # The bar that holds the given beat
    bar = track[bar_no]

    # Create a list of the timestamps in the bar
    timestamps = [note[0] for note in bar]

    # Find the index of the timestamp equal to or smaller than the given beat
    index = timestamps.index(max(i for i in timestamps if i <= beat_in_bar))
    
    # Return the pitch/pitches
    return bar[index][2]


#-------------------------
#ENDING WIP
#Creates an ending to the piece
#Modifies the given tracks
#-----------------------

def ending(first_track, second_track, subject, key=r""):

    if not bool(key):
        key = 'C'

    cadence = [chord.I(key), chord.IV(key), chord.V(key), chord.I(key)]

    #tracks = [first_track, second_track]

    bar = Bar()
    bar.place_rest(2)
    first_track.add_bar(bar)     #Sätt något som passar med andra hälften av subjektet

    while second_track[-1].current_beat < 1:       #Placing fitting notes in second to last bar

        print('test1')
        duration = 2 ** random.randint(1, 3)
        pitch = cadence[0][random.randint(0, len(cadence[0])-1)]

        # If the randomized duration doesn't fit in the bar, make it fit
        if 1 / duration > 1 - second_track[-1].current_beat:
            duration = 1 / (1 - second_track[-1].current_beat)

        # Place the new note in the bar
        second_track[-1].place_notes(pitch, duration)

    first_track[-1].place_notes(cadence[0][0],2)

    bar = Bar()
    bar.place_notes(cadence[1][0], 2)
    bar.place_notes(cadence[2][0], 2)
    first_track.add_bar(bar)

    bar = Bar()
    bar.place_notes(cadence[3][0],1)
    first_track.add_bar(bar)

    bar = Bar()
    print(bar.current_beat)
    while bar.current_beat < 0.5:
        print('test2')
        # Randomize pitch and duration of each note.
        duration = 2 ** random.randint(1, 3)
        pitch = cadence[1][random.randint(0, len(cadence[0])-1)]

        # If the randomized duration doesn't fit in the bar, make it fit
        if 1 / duration > 1 - bar.current_beat:
            duration = 1 / (1 - bar.current_beat)

        # Place the new note in the bar
        bar.place_notes(pitch, duration)
    while bar.current_beat < 1:

        print('test3')
        duration = 2 ** random.randint(1, 3)
        pitch = cadence[2][random.randint(0, len(cadence[1])-1)]

        # If the randomized duration doesn't fit in the bar, make it fit
        if 1 / duration > 1 - bar.current_beat:
            duration = 1 / (1 - bar.current_beat)

        # Place the new note in the bar
        bar.place_notes(pitch, duration)
    second_track.add_bar(bar)

    bar = Bar()
    bar.place_notes(cadence[3][2],1)
    second_track.add_bar(bar)



#----------------------------------
# TODO
#-----------------------------------


#augumentation/diminition


#ev. normalize notes to scale?
