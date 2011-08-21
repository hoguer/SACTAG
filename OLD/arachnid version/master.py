import tfidf
import os
import sys
from helper_functions import curr_test_dict

paramDict = curr_test_dict("curr_test.txt")

path = '../TLG_idf_files/' + paramDict['num_grams'] + 'grams' + '/' + paramDict['spread'] + "_" + "v" + paramDict['variant'] + "_" + "sw" + paramDict['stopwords'] + "/"

if not os.path.exists(path):
    os.makedirs(path)

TLG_file = os.readlink(sys.argv[1])
TLG_file = TLG_file.split('/')
TLG_file = TLG_file[-1]

if not os.path.exists(path + TLG_file):
    print TLG_file
    if paramDict['variant'] == 'True':
        variant = True
    else:
        variant = False

    _tfidf = tfidf.TfIdf(int(paramDict['spread']), variant, None, None, paramDict['stopword_file'])
    _tfidf.add_input_document('../stripped_text/' + TLG_file, int(paramDict['num_grams']))
    _tfidf.save_corpus_to_file(path + TLG_file)
else:
    print 'path already exists for ', TLG_file
