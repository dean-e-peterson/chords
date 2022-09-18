#!/usr/bin/python3
import re
import sys

sharps = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')
flats = ('A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab')
# m for minor, M for major, a for add, d for dim, and s for sus
patternNotes = r'(?:^|(?<=[ /\(]))[A-G][#b]?(?:$|(?=(?:[ mM/\d\)]|add|dim|sus)))'
patternNotInChords = 'h'

def transpose_file(file, halfsteps):
    for line in file:
        # Avoid transposing many lyrics lines by looking for non-chord pattern.
        if re.search(patternNotInChords, line):
            print(line, end = '')
        else:
            print(transpose_line(line, halfsteps), end = '')


def transpose_line(line, halfsteps):
    def replace_note(match_note):
        note = match_note.group(0)
        return transpose_note(note, halfsteps)

    return re.sub(patternNotes, replace_note, line)


def transpose_note(note, halfsteps):
    if note in sharps:
        i = sharps.index(note)
        #print(f'Sharp[{i}] {note} => ', end = '')
        i = (i + halfsteps) % 12
        note = sharps[i]
        #print(f'Sharp[{i}] {note}')
    elif note in flats:
        i = flats.index(note)
        #print(f'Flat[{i}] {note} => ', end = '')
        i = (i + halfsteps) % 12
        note = flats[i]
        #print(f'Flat[{i}] {note}')

    return note


if __name__ == '__main__':

    if len(sys.argv) < 2:
        exit(1)

    halfsteps = int(sys.argv[1])

    filename = None
    if len(sys.argv) > 2:
        filename = sys.argv[2]

    if filename == None:
        file = sys.stdin
    else:
        file = open(filename, 'rt')

    transpose_file(file, halfsteps)
