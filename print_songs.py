#!/usr/bin/python3
"""
Create PDF files for text files with song text with guitar chords, using a2ps.
"""
# dprun.py routine for running an external command.
#
# Fine.  FINE!  Since I cannot locate a SIMPLE existing standard python
# library function to do what I want, I'll write my own little wrapper.
#
# I want to run an OS command, return its output as string,
# and raise an exception if the return status is not zero.

import os
import sys
import subprocess
import optparse

def dprun (commandline, checkstatus=True):
    # Make sure a string was passed, not a sequence.
    if not isinstance(commandline, str):
        raise TypeError('commandline must be a string')

    # Run child process.
    process = subprocess.Popen(commandline
                              ,shell=True
                              ,stdout=subprocess.PIPE
                              ,stderr=subprocess.STDOUT
                              )

    # Get output, if any.
    output = process.stdout.read()

    # Wait for process to finish.  This seems essential despite waiting for
    # end of stdout, and at any rate, it prevents zombie infestations.
    process.wait()

    # Unless caller told use not to, raise an exception if return code non-zero
    if checkstatus and process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, commandline)

    # Return output.
    return output


def print_songs(filenames):
    for filename in filenames:
        # Process each song in a try/except,
        # so that if one fails the script will still try to process the rest.
        try:
            generate_pdf_for_song(filename)
            print_song(filename)
        except Exception as E:
            print("Unable to print song %s" % filename)
            print(E)

def generate_pdfs_for_songs(filenames):
    for filename in filenames:
        # Process each song in a try/except,
        # so that if one fails the script will still try to process the rest.
        try:
            generate_pdf_for_song(filename)
        except Exception as E:
            print("Unable to generate_pdf_for song %s" % filename)
            print(E)

def generate_pdf_for_song(filename):
    # Grab first line of file as Title to print as headings, and the number
    # of lines so we can shrink fonts to try to fit each file on one page.
    (title, lines, columns) = song_stats(filename)
    print("\nCreating PDF:\n%s\n%s\n(%d lines x %d columns)" % (
            filename, title, lines, columns))

    # Generate Postscript file.
    #
    # a2ps command options:
    #   -1      1-up printing (one virtual page per physical side of paper)
    #   -B      No page headers or footers (unless overridden later in cmd line)
    #   -C      Print line numbers every 5 lines.
    #   -L n    Lines to fit on one virtual page (could enlarge as well?)
    #   -l n    Columns to fit on one virtual page (could re-enlarge after -L!?)
    #   --header=       Would remove header but not title (don't need if use -B)
    #   --borders=no    No line drawn around whole virtual page.
    #   --margin=12     Margin pts on inner side of physical page, for binding.
    #   --center-title=title        Bold, central top title.
    #   --left-title='$D{%%...}%%p' File mod timestamp, in man strftime format,
    #       plus page #s, with %s doubled so python does not string format them.
    #   --right-title='#?2|$t2|$Q|' Would put page number on upper right,
    #       (I don't honestly know how right-title works, but I liked the
    #        default and had to explicitly specify it to get it back after
    #        wiping out all headers with -B.  a2ps --list=settings showed it.)
    postscript_filename = filename.replace('.txt', '.ps')
    #a2ps_command = """a2ps -1 -B --margin=16 --center-title="%s" --left-title='$D{%%m/%%d/%%Y %%l:%%M %%P }' --right-title='#?2|$t2|$Q|' --borders=no %s -o %s""" % (title, filename, postscript_filename)
    a2ps_command = """a2ps -1 -B --margin=16 --center-title="%s" --left-title='$D{%%m/%%d/%%Y %%l:%%M %%P}, %%p. of %%p#' --borders=no %s -o %s""" % (title, filename, postscript_filename)
    if lines > 63:
        a2ps_command += """ -L %d""" % (lines)
    print(a2ps_command)
    print(dprun(a2ps_command))

    # If the .ps output file already exists, a2ps seems to create a backup
    # file ending in tilde (~).  Delete them.
    backup_filename = postscript_filename[0:13] + '~'
    if os.path.isfile(backup_filename):
        print(dprun("rm %s" % backup_filename))
        #print "deleted %s" % backup_filename

    # Convert the Postscript file to a PDF file.
    print(dprun("ps2pdf %s" % postscript_filename))
    print("%s created" % (postscript_filename.replace('.ps', '.pdf')))

    # Now that we have a PDF file, delete the Postscript file.
    print(dprun("rm %s" % postscript_filename))
    print("%s deleted" % (postscript_filename))

def print_song(filename):
    pdf_filename = filename.replace('.txt', '.pdf')
    print(dprun("lpr %s" % pdf_filename))
    print("%s printed to default printer" % pdf_filename)

def show_counts_of_lines_in_song_files(filenames):
    for filename in filenames:
        try:
            show_count_of_lines_in_song_file(filename)
        except Exception as E:
            print("Unable to determine lines in song %s" % filename)
            print(E)

def show_count_of_lines_in_song_file(filename):
    (title, lines, columns) = song_stats(filename)
    print("%s lines: %s" % (lines, filename))

def song_stats(filename):
    """
    Get songfile information, like the # of lines and columns in the text file,
    and the first of the file to use as a song title.
    """
    lines = 0
    columns = 0
    firstline = True
    with open(filename, 'r') as f:
        for line in f:
            if firstline:
                # Title is first line, stripped of trailing newline, etc.
                title = line.strip()
                firstline = False
            lines += 1
            columns = max(columns, len(line))
    # Return a tuple of the title, lines, and columns.
    return (title, lines, columns)


if __name__ == '__main__':
    # Parse command line arguments.
    desc = """%prog [-l | -p] textfile [ textfile...]

    Create PDF files from song text files using a2ps.
    Note: Expects input filenames to end in a lower case .txt."""
              
    parser = optparse.OptionParser(usage=desc)
    parser.add_option('-l', '--lines', action='store_true', dest='lines_only',
                      help='show number of lines; do not create pdfs or print')
    parser.add_option('-p', '--print', action='store_true', dest='print_also',
                      help='try to print generated PDF files with lpr')
    parser.set_defaults(lines_only=False)
    parser.set_defaults(print_also=False)
    (options, args) = parser.parse_args()

    # Do what command line arguments requested.
    if len(args) == 0:
        print("Please pass a song file or files on the command line.")
        exit
    if options.lines_only:
        show_counts_of_lines_in_song_files(args)
    elif options.print_also:
        print_songs(args)
    else:
        generate_pdfs_for_songs(args)

