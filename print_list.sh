#!/bin/bash

TEMPFILE=temp.tmp
LISTNAME=$1
OUTNAME=${1/.list/.pdf}

# Print the songs.
echo "---------------------------------"
echo Printing songs...
echo "---------------------------------"
# Always put chord voicings before the first file added by xargs.
cat $LISTNAME | xargs ./print_songs.py chord_voicings.txt

# Create command to make a composite PDF of them all
echo -n 'pdfunite ' > $TEMPFILE
echo -n 'chord_voicings.pdf ' >> $TEMPFILE
cat $LISTNAME | sed -e 's/.txt/.pdf/' | tr '\n' ' ' >> $TEMPFILE
echo " $OUTNAME" >> $TEMPFILE
echo "---------------------------------"
echo Creating combined PDF $OUTFILE
echo "---------------------------------"
. temp.tmp
rm temp.tmp

# Ugly way to find errors, likely due to curly quotes or other characters
# which the iconv utf8 to iso8859.1 conversion had problems with.
#ls *.latin1
