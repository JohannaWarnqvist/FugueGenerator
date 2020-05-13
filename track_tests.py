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
repeating_passages(track, (optional bool with_duration))    returns (average_nm_of_rep,average_len_of_repetition,(percentage_of_repetition- kinda works but not perfect))
count_notes_on_beat(track)                                  Calculates how many notes that are on a beat of its own duration beats, or if it is in the middle of two such beats.
count_notes_in_scale(track)                                 Counts the number of notes in the track that is in the correct scale.
count_tritone_or_seventh_in_two_skips(track)                Returns the number of tritones or sevenths in two skips in a one-voice track.
interval_at_beat(track1,track2,beat)                        Returns the interval between two tracks on a given beat
contrapunctal_motion(track)                                 IN PROGRESS
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
# repeating_passages: (Values may not be exact but are good enough to use in the fitness function)
# Calculates average length of repeating passage, 
# Calculate average numb of repetitions of passages larger than 1 note
# Calculate the precentage of the track that is build up of repetition 
# Note: Repetitions are measured within a bar, witdh_duration determines if repetition has to have same relative note duration or not.
#--------------------------------------------------------------------   
def repeating_passages(track, with_duration = False):
    note_generetor = copy.deepcopy(track).get_notes()
    passage_repetitions = {}    #directory of occurences of different passages (nmb of repetitions)
    passage_lengths = {}        #directory of passage lenths, Cause you can't store two different values to same key in one directory
    current_passage = []        #List of either just (intervals as ints) or (intervals,relative difference between note durations)
    previous_note = None        
    previous_note_length = 0    #Only useful when considering note durations
    nmb_of_notes = 0.0          #Used to calculate percentage
    
    
    for note in note_generetor:
        nmb_of_notes += 1.0
        #If pause go to next note
        if note[-1] is None:
            continue
        
        #If new bar or first Note, change previous note to be the current note
        elif(note[0] == 0.0) or (previous_note is None):
            previous_note = note[-1][0]
            previous_note_length = note[1]
            current_passage = []
            continue

        else:
            #Calculate inteval as an int (works over octaves)
            diff = Note.measure(previous_note,note[-1][0])

            #If we have to take duration into consideration calculate relative duration
            #ev. TODO not precicely what it does but allows repetitions with all same note duration pass
            if with_duration:
                current_passage.append([diff, (previous_note_length - note[1])])
                previous_note_length = note[1]
            
            #If we don't consider duration just add interval
            else:
                current_passage.append(diff)

            #Set previous note to be current one
            previous_note = note[-1][0]
            
            #starting with the longes possible passage calculate the possible passages from current_passage
            for i in range(len(current_passage)):
                tmp = str(current_passage[i:len(current_passage)]) #key

                #if passage is already added increace occurance of passage
                if tmp in passage_repetitions:
                    passage_repetitions[tmp] += 1.0
                    print(tmp)
                    break
                #If passage isn't added to dictionary, add it
                else: 
                    passage_repetitions[tmp] = 0.0
                    passage_lengths[tmp] = len(current_passage)- i + 1.0
            
    average_nm_of_rep = 0.0             #Will get the sum of all occurences
    average_len_of_repetition = 0.0     #Will get the sum of all passage length of repeated passages
    nmb_of_repeating_passages = 0.0     #Keeps track of the number of different repeated passages
    percentage_of_repetition = 0.0      #Will get the sum of all repeated notes

    for keys,occurences in passage_repetitions.items():
        if occurences > 0.0:
            average_nm_of_rep += occurences
            length_of_passage = passage_lengths[keys]
            percentage_of_repetition += (length_of_passage*occurences)
            average_len_of_repetition += length_of_passage
            nmb_of_repeating_passages += 1.0

    #Calculate final return data
    if nmb_of_repeating_passages > 0.0:
        average_nm_of_rep = average_nm_of_rep/nmb_of_repeating_passages
        average_len_of_repetition = average_len_of_repetition/nmb_of_repeating_passages
        print(percentage_of_repetition)
        percentage_of_repetition = percentage_of_repetition/nmb_of_notes #TODO percentage in faulty

    return (average_nm_of_rep,average_len_of_repetition,percentage_of_repetition)
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
# Could be altered to return the indeces of the ugly intervals if that turns out to be useful.
# Limitation: if input has notecontainers with more than one pitch, it counts the first note in the container.
# -------------------------------------------
def count_tritone_or_seventh_in_two_skips(track, return_index = False):
    "Returns the number of tritones or sevenths in two skips in a one-voice track."
    
    unwanted_intervals = [6,10,11]  # tritone, minor and major seventh 
    
    # list of all notes
    notes = [track[i][j][2] for i in range(len(track.bars)) for j in range(len(track[i]))]

    # count nmb of unwanted intervals
    nmb = 0
    for i in range(len(notes)-2):
        note1 = notes[i]
        note2 = notes[i+2]
        if note1 is None or note2 is None:  # make sure notes aren't pauses
            continue
        interval = Note(note1[0]).measure(Note(note2[0]))   #returns the nmb. of halftones between the notes
        if abs(interval)%12 in unwanted_intervals:
                nmb += 1
    return nmb

# ---------------------------------------------
# interval_at_beat: 
# Returns the interval between two tracks on the given beat
# Returns a string by default, returns number of halftones if return_int=True, returns None if there is a pause in any voice
# Limitaion: Does not take octaves into account, example: [C4, G4] = [C4, G5] = fifth.
# ---------------------------------------------
def interval_at_beat(track1,track2,beat,return_int=False):
    pitch1 = Track_Functions.pitch_at_given_beat(track1,beat)
    pitch2 = Track_Functions.pitch_at_given_beat(track2,beat)
    
    # Check for pauses
    if pitch1 is None or pitch2 is None:
        return None

    # Return halftone interval if requested
    interval_halftones = Note(pitch1[0]).measure(Note(pitch2[0]))
    if return_int == True:    
        return interval_halftones
    
    # Else return a str
    # Workaround for the fact that the .determine function doesn't return unisons or octaves
    if interval_halftones == 0:
        return 'perfect unison'
    elif interval_halftones%12 == 0:
        return 'octave'
    else:
        note_pair = NoteContainer([pitch1[0],pitch2[0]])
        return note_pair.determine()[0]

# ---------------------------------------------
# contrapunctal_motion: 
# IN PROGRESS
# Will measure what contrapunctal motion is used in the track, or how much of which if several.
# ---------------------------------------------
def contrapunctal_motion(first_voice, second_voice):
    print("Start of contrapunctal_motion")
    beat_first = 0
    beat_second = 0
    
    motion_first = motion_of_track(first_voice)
    motion_second = motion_of_track(second_voice)
    
    # Check combo of motions
    contrapunctal_motion = []
    parallel_motion = 0
    similar_motion = 0
    rest_motion = 0
    one_motion = 0
    oblique_motion = 0
    contrary_motion = 0

    
    previous_beat = 0
    current_beat = min(motion_first[0][1], motion_second[0][1])
    total_nr_beats = len(first_voice)
    ind_first = 0
    ind_second = 0
    while current_beat < total_nr_beats:
            print(f"ind_first: {ind_first}")
            print(f"ind_second: {ind_second}")
            #breakpoint()
            # Chech if same motion in both tracks
            if motion_first[ind_first][-1] == motion_second[ind_second][-1]:
                # Check if both are resting
                if motion_first[ind_first][-1] == 'Rest':
                    current_motion = 'Rest'
                    rest_motion += current_beat - previous_beat
                else:
                    # Check if parallel or similar
                    parallel = check_if_parallell(first_voice, second_voice, previous_beat, current_beat)
                    
                    if parallel:
                        current_motion = 'Parallel'
                        parallel_motion += current_beat - previous_beat

                    else:
                        current_motion = 'Similar'
                        similar_motion += current_beat - previous_beat
            
            # Check if one track is 'Same', then oblique
            elif motion_first[ind_first][-1] == 'Same' or motion_second[ind_second][-1] == 'Same':
                current_motion = 'Oblique'
                oblique_motion += current_beat - previous_beat
            # Check if one track is resting, then 'One'
            elif motion_first[ind_first][-1] == 'Rest' or motion_second[ind_second][-1] == 'Rest':
                current_motion = 'One'
                one_motion += current_beat - previous_beat
            # Otherwise motion is in opposite directions and contrary
            else:
                current_motion = 'Contrary'
                contrary_motion += current_beat - previous_beat
            
            # Add motion to list
            contrapunctal_motion.append([previous_beat, current_beat-previous_beat, current_motion])
            
            # Update beats and indices
            previous_beat = current_beat
            old_ind_first = ind_first
            if motion_first[ind_first][0] + motion_first[ind_first][1] <= motion_second[ind_second][0] + motion_second[ind_second][1]:
                current_motion = motion_first[ind_first][0] + motion_first[ind_first][1]
                ind_first += 1
                
            if motion_first[old_ind_first][0] + motion_first[old_ind_first][1] >= motion_second[ind_second][0] + motion_second[ind_second][1]:
                current_motion = motion_second[ind_second][0] + motion_second[ind_second][1]
                ind_second += 1
    
    contrapunctal_motion_values = {'Contrary': contrary_motion/total_nr_beats, 'Parallel': parallel_motion/total_nr_beats, 
                    'Oblique': oblique_motion/total_nr_beats, 'Similar': similar_motion/total_nr_beats, 
                    'Rest': rest_motion/total_nr_beats, 'One': one_motion/total_nr_beats}
    print("End of contrapunctal_motion")
    return contrapunctal_motion_values

# TODO: fix so that similiar and parallel can be checked within same motion part


# ---------------------------------------------
# track_motion: 
# Help function that gets a track as input and calculates how the motion is for different parts.
# Returns a list of list elements in the form [start, length, type], with start being the start of the 
# motion, length being the length of the motion in beats, and type is either 'Up', 'Down', 'Same' or 'Rest'.
# ---------------------------------------------
def motion_of_track(track):
    print("Start of motion_of_track")

    # Initialize lists to contain tuples of which beats contain which motion
    motion = []


    # Loop over all notes in first voice to decide motion
    notes = track.get_notes()

    previous_note = None
    current_passage = 0
    current_start = 0
    current_motion = None
    for note in notes:  

        # If first note in track
        if previous_note is None:
            # If not a rest, add to first part but set which motion later
            if not note[-1] is None:
                previous_note = note
                current_passage = 1/note[1]
                continue
            # If a rest, start a rest motion
            else:
                previous_note = note
                current_passage = 1/note[1]
                current_motion = 'Rest'
                continue
          
        # If the note is a rest, end last motion and start a rest motion
        if note[-1] is None:
            if current_motion != 'Rest':
                # Add the previous motion to the list
                motion.append([current_start, current_passage, current_motion])                
                
                # Start new upward motion
                current_start += current_passage
                current_passage = 1/note[1]
                current_motion = 'Rest'
            else:
                current_passage += 1/note[1]
        
        # Upward motion between this and previous note
        elif note[-1][0] > previous_note[-1][0]:
            if current_motion == 'Up':
                current_passage += 1/note[1]                
            elif current_motion is None:
                current_motion = 'Up'
                current_passage += 1/note[1]                
            else:
                # Add the previous motion to the list
                motion.append([current_start, current_passage, current_motion])                
                
                # Start new upward motion
                current_start += current_passage
                current_passage = 1/note[1]
                current_motion = 'Up'
        
        # Downward motion between this and previous note
        elif note[-1][0] < previous_note[-1][0]:
            if current_motion == 'Down':
                current_passage += 1/note[1]                
            elif current_motion is None:
                current_motion = 'Down'
                current_passage += 1/note[1]                
            else:
                # Add the previous motion to the list
                motion.append([current_start, current_passage, current_motion])                
                
                # Start new upward motion
                current_start += current_passage
                current_passage = 1/note[1]
                current_motion = 'Down'
        
        # No motion between this and previous note
        elif note[-1][0] == previous_note[-1][0]:
            if current_motion == 'Same':
                current_passage += 1/note[1]                
            elif current_motion is None:
                current_motion = 'Same'
                current_passage += 1/note[1]                
            else:
                # Add the previous motion to the list
                motion.append([current_start, current_passage, current_motion])                
                
                # Start new upward motion
                current_start += current_passage
                current_passage = 1/note[1]
                current_motion = 'Same'
        
        previous_note = note
    
    # Add the previous motion to the list
    motion.append([current_start, current_passage, current_motion])                
    
    print(motion)
    print("End of motion_of_track")
    return motion
   
def check_if_parallell(first_voice, second_voice, start_beat, end_beat):
    print("Start of check_if_parallel")

    intervals = get_all_intervals(first_voice, second_voice, start_beat, end_beat)
    
    first_interval = intervals[0]
    for interval in intervals:
        if interval != first_interval:
            return False
    print("End of check_if_parallel")

    return True
   
   
def get_all_intervals(first_voice, second_voice, start_beat = 0, end_beat = None):
    print("Start of get_all_intervals")

    if end_beat is None:
        end_beat = min(first_voice.current_beat, second_voice.current_beat)
    
    notes_first = first_voice.get_notes()
    notes_second = second_voice.get_notes()
    
    for note_first in notes_first:
        print(f"note_first: {note_first}")
        # If end of note is before beat, take the next note
        if note_first[0] + note_first[1] <= start_beat:
            continue
        else:
            break

    print(f"first note_first: {note_first}")
    
    for note_second in notes_second:
        print(f"note_second: {note_second}")
        # If end of note is before beat, take the next note
        if note_second[0] + note_second[1] <= start_beat:
            continue
        else:
            break
    
    print(f"first note_second: {note_second}")

    intervals = []
    beat = start_beat
    ind_first = 0
    ind_second = 0
    print(f"end_beat: {end_beat}")
    print(f"beat: {beat}")
    while beat < end_beat:
        print(f"beat start of loop: {beat}")
        current_interval = interval_at_beat(first_voice, second_voice,4*beat,return_int=True)
        intervals.append(current_interval)
        print(f"note_first used: {note_first}")
        print(f"note_second used: {note_second}")
        # Update beat and current notes
        if note_first[0]+1/note_first[1] <= note_second[0] + 1/note_second[1]:
            beat = note_first[0] + 1/note_first[1]
            for note_first in notes_first:
                if note_first[0] + 1/note_first[1] <= beat:
                    continue
                else:
                    break
        
        if note_first[0] + 1/note_first[1] >= note_second[0] + 1/note_second[1]:
            beat = note_second[0] + 1/note_second[1]
            for note_second in notes_second:
                # If end of note is before beat, take the next note
                if note_second[0] + 1/note_second[1] <= beat:
                    continue
                else:
                    break
        print(f"beat in end of loop: {beat}")
            
    print(f"intervals: {intervals}")
    print("End of get_all_intervals")
    return intervals


print(test_track)
contrapunctal_motion(test_track, test_track_2)