import re, os, sys, glob

def strip_unwanted_chars(file):
    f=open(file, "r")
    s=f.read()

    #removes all characters with value greater than 127
    s = "".join(i for i in s if ord(i)<128)

    #Put spaces around the characters [. , : ; _] so that they are treated as individual words.
    s = re.sub(r"([.,:;_])", r" \1 ", s)

    #replaces brackets {} and [] and any enclosed text with a space.
    #Also, any following integers, 123456789, have been removed, as TLG sometimes uses [#.....]# or {#.....}# to indicate a certain style of bracket.
    s = re.sub(r"\{[^}]*\}[0-9]+", " ", s)
    s = re.sub(r"\[[^}]*\][0-9]+", " ", s)

    #replaces the characters [@ %] and any immediately following integers with a space
    s = re.sub(r"[@|%][0-9]+", " ", s)

    #replace multiple whitespaces with one space
    s = re.sub(r"[\s]+", " ", s)
        
    f.close()
    return s


if (len(sys.argv) == 3):

    indir = sys.argv[1]
    outdir = sys.argv[2]

    if not os.path.exists(indir):
        print "source folder does not exist"
    elif not os.path.exists(outdir):
        print "destination folder does not exist"
    else:
        for infile in glob.glob(os.path.join(indir, '*.TXT') ):

            output = strip_unwanted_chars(infile)

            #print clean text to file
            outfile = re.sub(indir, outdir, infile)
            print outfile
            out = open(outfile, "w")
            out.write(output)
            out.close()
        
else:
    print "Incorrect number of arguments. Please include a source folder and a destination folder."

