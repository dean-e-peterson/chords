#!/bin/bash

# Original, 6 or more of just x and digits:
# egrep '\([x0-9]{6,}\)' *

# Now allow small o which I saw somewhere, and uppercase X and questions marks)
# egrep '\([xXo0-9?]{6,}\)' *

# Now don't prefix filename (-h), sort by chord, and remove duplicate lines)
# egrep -h '\([xXo0-9?]{6,}\)' * | sort | uniq

# Alternately, leave the filename prefix, but put a tab after it,
# then sort on the 2nd tab separated field (the chord),
# then use a tab stop longer than the longest filename (I hope)
# to display the output in a columnar fashion...and yes, I should probably
# just implement this in Python or something.
# (The $'\t' is BASH-SPECIFIC syntax to convert escape sequences in that word.)
# egrep -T '\([xXo0-9?]{6,}\)' * | sort -t $'\t'  -k 2 | expand -t 50

# Now lets try leaving the grep output alone (filename, colon, and chord line),
# but use sed to swap it so the chord line stuff is first, then tab & filename.
egrep '\([xXo0-9?]{6,}\)' * | sed -e 's/\([^:]*\):\(.*\)/\2\t\1/g' | expand -t 45,55,65,75,85 | sort 

