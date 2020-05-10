#---------------------------------------------
# In this file we create different functions that verifies or measure different aspects of tracks 
# Basically a huge helper file for creating fitness functions later on
#---------------------------------------------

from mingus.containers import Track
from mingus.containers import Bar
from mingus.containers import NoteContainer
from mingus.containers import Note
import mingus.core.intervals as intervals
import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.keys as keys
import midi_test as midi
import copy
import random
import track_functions as Track_Functions

"""FUNCTION INDEX                                           (to be able to find functions easier)
repeating_note_length(track)                                Calculates a fraction between the nmb of notes and the most occuring note length and returns it
average_numb_of_chords(track1,track2)                       Returns an average numb of chords/bar created by two tracks playing simultaneously
average_note_length_cluster(track)                          returns the average size of same length note clusters
repeating_note_pitch(track, (optional bool exact))          Calculates a fraction between the nmb of notes and the most occuring note pitch and returns it
repeating_passages(track)                                   IN PROGRESS
count_notes_on_beat(track)                                  Calculates how many notes that are on a beat of its own duration beats, or if it is in the middle of two such beats.
count_notes_in_scale(track)                                 Counts the number of notes in the track that is in the correct scale.
count_tritone_or_seventh_in_two_skips(track)                Returns the number of tritones or sevenths in two skips in a one-voice track.
interval_at_beat(track1,track2,beat)                        Returns the interval between two tracks on a given beat
"""

#--------------------------------------------------------------------
# repeating_note_length:
# Calculates a fraction between the nmb of notes and the most occuring note length and returns it
# Ex. If 60% of the notes are quarter notes the function will reeturn 0.6
#--------------------------------------------------------------------
def repeating_note_length(track):
    note_generetor = copy.deepcopy(track).get_notes()
    #Dictionary that matches note length to nmb of occurences of that note
    note_lengths = {}
    #nmb of notes in track
    nmb_of_notes = 0.0

    for note in note_generetor:
        #If note length is not in dictionary add it
        if not(note[1] in note_lengths):
            note_lengths[note[1]] = 0.0
        #increment nmb of occurences and total number of notes
        note_lengths[note[1]] += 1.0
        nmb_of_notes += 1.0
    
    #Calculate the biggest fraction between occurences and nmb of notes in track
    biggest_fraction = 0.0
    for lengths,occurences in note_lengths.items():
        temp = occurences/nmb_of_notes
        if temp > biggest_fraction:
            biggest_fraction = copy.deepcopy(temp)

    return biggest_fraction

#--------------------------------------------------------------------
# average_numb_of_chords:
# Returns an average numb of chords/bar created by two tracks playing simultaneously
#TODO fix merge so that it doesn't cut length but doubles note instead
#--------------------------------------------------------------------
def average_numb_of_chords(track1, track2):
    #Use help function merge tracks to create a track were notes from both tracks are merged into note containers
    merged_track = Track_Functions.merge_tracks(track1,track2)
    note_generetor = merged_track.get_notes()
    numb_of_chords = 0.0

    for note in note_generetor:
        #If note is a pause skip
        if note[-1] is None:
            continue
        #If note container contains more than one note (a chord) increment chord counter
        if len(note[-1]) > 1:
            numb_of_chords += 1.0
    
    #Return average amount of chords/ bar
    return (numb_of_chords/ len(merged_track))

#--------------------------------------------------------------------
# average_note_length_cluster:
# returns the average size of same length note clusters (average number of notes in sequence to have the same note duration)
#--------------------------------------------------------------------
def average_note_length_clusters(track):
    note_generetor = copy.deepcopy(track).get_notes()
    nmb_of_notes = 1.0
    #List with length of all note-length clusters saved sequentially
    cluster_length = [1.0]
    curent_note_length = next(note_generetor)[1]

    for note in note_generetor:
        #If note is part of current cluster increment value
        if note[1] == curent_note_length:
            cluster_length[-1] += 1.0
        #Otherwise start new cluster
        else:
            curent_note_length = note[1]
            cluster_length.append(1.0)
    
    #Add all cluster lengths together
    added_cluster_legths = 0.0
    for length in cluster_length:
        added_cluster_legths += length
        
    #return average cluster length
    return (added_cluster_legths/len(cluster_length))

#--------------------------------------------------------------------
# repeating_note_pitch:
# Calculates a fraction between the nmb of notes and the most occuring note pitch and returns it
# Excat is a bool that determines if you differ C-5, C, and Cb or consider them to be the same
#--------------------------------------------------------------------    
def repeating_note_pitch(track, exact = False):
    note_generetor = copy.deepcopy(track).get_notes()
    #Dictionary that matches note pitch to nmb of occurences of that note
    note_pitches = {}
    #nmb of notes in track
    nmb_of_notes = 0.0

    for note in note_generetor:
        if note[-1] is None:
            continue
        #If note pitch is not in dictionary add it
        nc = note[-1]
        for note_pitch in nc:
            if exact:
                if not(note_pitch.name in note_pitches):
                    note_pitches[note_pitch.name] = 0.0
                note_pitches[note_pitch.name] += 1.0
            else:
                if not(note_pitch.name[0] in note_pitches):
                    note_pitches[note_pitch.name[0]] = 0.0
                note_pitches[note_pitch.name[0]] += 1.0
        
        nmb_of_notes += 1.0
    
    #Calculate the biggest fraction between occurences and nmb of notes in track
    biggest_fraction = 0.0
    for pitches,occurences in note_pitches.items():
        temp = occurences/nmb_of_notes
        if temp > biggest_fraction:
            biggest_fraction = copy.deepcopy(temp)

    return biggest_fraction

#--------------------------------------------------------------------
# repeating_passages:
# Calculates average length of repeating passage, 
# Calculate average numb of repetitions of passages larger than 3 notes
#--------------------------------------------------------------------   
def repeating_passages(track, with_duration = False):
    note_generetor = copy.deepcopy(track).get_notes()
   


#--------------------------------------------------------------------
# count_notes_on_beat:
# Calculates how many notes that are on a beat of its own duration beats, or 
# if it is in the middle of two such beats.
# Returns a list of the number of notes placed on correct beats, and the number 
# of notes in the middle of beats, normalized over total number of notes.
#--------------------------------------------------------------------   
def count_notes_on_beat(track):
    placed_on_beat = 0
    placed_on_half_beat = 0
    total_nr_of_notes = 0

    note_containers = track.get_notes()
    for note in note_containers:
        total_nr_of_notes += 1
        # Get the note from the container
        print(note)
        note_duration = note[1]
        note_beat = note[0]
        if (note_beat % (1/note_duration)) == 0:
            placed_on_beat += 1
        elif (note_beat % (1/(2*note_duration))) == 0:
            placed_on_half_beat += 1
    
    return [placed_on_beat/total_nr_of_notes, placed_on_half_beat/total_nr_of_notes]

#--------------------------------------------------------------------
# count_notes_in_scale:
# Counts the number of notes in the track that is in the correct scale.
# Returns the number of notes in scale normalized over total number of notes.
#--------------------------------------------------------------------   
def count_notes_in_scale(track, key):
    total_nr_of_notes = 0
    notes_in_scale = 0
    scale_notes = keys.get_notes(key)
    notes = track.get_notes()
    for note_container in notes:
        note = note_container[-1][0]
        total_nr_of_notes += 1
        if note.name in scale_notes:
            notes_in_scale += 1
    
    return notes_in_scale/total_nr_of_notes

# ------------------------------------------
# count_tritone_or_seventh_in_two_skips(track): 
# Please feel free to rename !!
# Returns the number of tritones or sevenths in two skips in a one-voice track.
# Limitation: if input has notecontainers with more than one pitch, it counts the first note in the container.
# -------------------------------------------
def count_tritone_or_seventh_in_two_skips(track):
    "Returns the number of tritones or sevenths in two skips in a one-voice track."

    # All possible names of the 6, 10 and 11 halftone intervals
    unwanted_intervals = ['augmented fourth','minor fifth','major seventh','minor seventh']
    
    # List of all notes in the track
    notes = [track[i][j][2][0] for i in range(len(track.bars)) for j in range(len(track[i]))]
    
    # Count number of 'ugly' intervals 
    nmb = 0
    for i in range(len(notes)-2):
        note_pair = NoteContainer([notes[i],notes[i+2]])
        interval = note_pair.determine()    
        if interval[0] in unwanted_intervals: # interval[0] because interval is a list, apparantly
            nmb += 1
    return nmb

# ---------------------------------------------
# interval_at_beat: 
# returns the interval between two tracks on the given beat.
# If there's a pause in any of the tracks, it returns None
# (It might be an idea to move pitch_at_given_beat inside this function.)
# ---------------------------------------------
def interval_at_beat(track1,track2,beat):
    "Returns the interval between two tracks on a given beat."
    pitch1 = Track_Functions.pitch_at_given_beat(track1,beat)
    pitch2 = Track_Functions.pitch_at_given_beat(track2,beat)
    if isinstance(pitch1,NoteContainer) and isinstance(pitch2,NoteContainer):
        note_pair = NoteContainer([pitch1[0],pitch2[0]])
        return note_pair.determine()[0]

""" Can be used to test functions
test_track = Track_Functions.init_random_track("C",True)
print(test_track)
print("function"(test_track))
"""
