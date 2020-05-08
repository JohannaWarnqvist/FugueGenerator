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
repeating_note_lenght(track)                                Calculates a fraction between the nmb of notes and the most occuring note length and returns it
average_numb_of_chords(track1,track2)                       Returns an average numb of chords/bar created by two tracks playing simultaneously
average_note_length_cluster(track)                          returns the average size of same length note clusters
repeating_note_pitch(track, (optional bool exact))          Calculates a fraction between the nmb of notes and the most occuring note pitch and returns it
repeating_passages(track)                                   IN PROGRESS
"""

#--------------------------------------------------------------------
# repeating_note_lenght:
# Calculates a fraction between the nmb of notes and the most occuring note length and returns it
# Ex. If 60% of the notes are quarter notes the function will reeturn 0.6
#--------------------------------------------------------------------
def repeating_note_lenght(track):
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
# Calculate numb of repetitions of passages larger than 3
#--------------------------------------------------------------------   
def repeating_passages(track):
    note_generetor = copy.deepcopy(track).get_notes()

""" Can be used to test functions
test_track = Track_Functions.init_random_track("C",True)
print(test_track)
print("function"(test_track))
"""