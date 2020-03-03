#!/usr/bin/python

"""
Dean's script to check if guitar chords used in a song have voicings given.
"""

import sys
import re

def check_songs(filenames):
    for filename in filenames:
        # Put the checking of each song in a try/except, 
        # so that if one fails the script will still try to check the rest.
        try:
            check_song(filename)
        except Exception as E:
            print "Unable to check song %s" % filename
            print E
        
def check_song(filename):
    print "Checking %s:" % filename
    set_of_chords_used = set()
    #set_of_chords_voiced = set()
    with open(filename, 'r') as f:
        for line in f:
            # If I ever want to use a dictionary? d[key] = d.get(key, 0) + qty ?

            # First filter parenthesis out of the line, i.e. ignore them.
            line = line.replace('(','').replace(')','')

            # Now check the parenthesis-less line for chords.
            set_of_chords_used.update(chords_used_in_line(line))
            #set_of_chords_voiced.update(chords_voiced_in_line(line))

        print "Chords used: %s" % sorted(set_of_chords_used)
        #print "Chords voiced: %s" % sorted(set_of_chords_voiced)

# Chord regular expression.  May need work...
#  - create subgroup for chords inside of parenthesis?
#  - create subgroups for chord itself versus base note?
#  - lookahead assertion to disallow if next thing is not chordish
#        (second letter not start with b, sus, maj, dim, aug ?)
# NOTE: All parenthesis may be removed from the line before it even gets
#       put through the regular expression search.
# chord_rex = re.compile(r'\b[A-G][a-z2-9]?\b')
#chord_rex = re.compile(r'\b[A-G](b|#|m|M|maj|Maj|dim|add|sus|aug|\+)?[2-7]?\b')
chord_rex = re.compile(r'\b[A-G]([0-9]|b|#|m|M|maj|Maj|dim|add|sus|aug|\+)*(/[A-G])?\b')

def chords_used_in_line(line):
    #print line
    result = set()
    for match in chord_rex.finditer(line):
        result.add(match.group(0)) # group(0) being the whole match, not subs
    return result


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Please pass a song file or files on the command line."
    else:
        check_songs(sys.argv[1:])

