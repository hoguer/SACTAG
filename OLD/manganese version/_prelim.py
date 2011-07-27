import os, sys
from helper_functions import file_dict

if len(sys.argv) != 7:  # the program name and the two arguments
    # stop the program and print an error message
    sys.exit("Must provide two authors, a subcorpora, an integer spread, num_grams, and variant word order as True or False")

f = open("curr_test.txt", "w")
f.write(sys.argv[1] + "\n" + sys.argv[2] + "\n" + sys.argv[3] + "\n" + str(sys.argv[4]) + "\n" + str(sys.argv[5]) + "\n" + sys.argv[6])

filedict = file_dict('../ref_file.txt')
TLG_files = filedict[sys.argv[3]]

#delete old contents of temp_in folder
folder = "../temp_in"
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    try:
        os.unlink(file_path)
    except Exception, e:
        print e

#create symbolic links to TLG_files in temp_in
for i in range(len(TLG_files)):
    os.symlink("../stripped_text" + TLG_files[i], folder + "/file" + str(i+1))
