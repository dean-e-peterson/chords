#!/bin/bash

TEMPFILE=temp.tmp
LISTNAME=$1
OUTNAME=${1/.txt/.pdf}

# Print the songs.
echo "---------------------------------"
echo Printing songs...
echo "---------------------------------"
cat $LISTNAME | xargs ./print_songs.py

# Create command to make a composite PDF of them all
echo -n 'pdfunite ' > $TEMPFILE
cat $LISTNAME | sed -e 's/.txt/.pdf/' | tr '\n' ' ' >> $TEMPFILE
echo " $OUTNAME" >> $TEMPFILE
echo "---------------------------------"
echo Creating combined PDF $OUTFILE
echo "---------------------------------"
. temp.tmp
rm temp.tmp
