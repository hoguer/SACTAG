import os, sys


def setup(TLG_files):
    #delete old contents of temp_in folder
    folder = "../temp_in"
    rm_folder_contents(folder)

    #create symbolic links to TLG_files in temp_in
    for i in range(len(TLG_files)):
        print "i: ", i
        print "file: ", TLG_files[i]
        os.symlink("../stripped_text/" + TLG_files[i], folder + "/file" + str(i+1))

def rm_folder_contents(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            os.unlink(file_path)
        except Exception, e:
            print e
                                                
