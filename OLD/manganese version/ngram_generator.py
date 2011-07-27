import string
import re
#from nltk import ngrams

#def build_ngram_dictionary (filename, ngram_count_dict, n):

#    f=open (filename, "r")
	
#    text = f.read()
	
#    f.close()

#    word_list = re.split(" +", text)

#    ngram_list = ngrams(word_list, n)

#    for w in ngram_list:

#        if ngram_count_dict.has_key (w):

#            ngram_count_dict[w] = ngram_count_dict[w] + 1

#        else:

#            ngram_count_dict[w] = 1

    
#    return ngram_count_dict



def sort_by_ngram (ngram_count_dict):

    sorted =  ngram_count_dict.items()

    sorted.sort()

    return sorted


def sort_by_count (ngram_count_dict, reverse=False):

    sorted = []

    for (k, v) in ngram_count_dict.items():

        sorted = sorted + [(v, k)]

    if not reverse:
        sorted.sort()
    else:
        sorted.sort(reverse=True)

    return sorted

    
def print_to_file_by_freq (ngram_list, filename):

    f = open(filename, 'w')
    print "printing by freq to: ", filename
    for ngram_count in ngram_list:

        ngram = ''
        for gram in ngram_count[1]:
            ngram += gram + '\t'

        f.write(ngram + str(ngram_count[0]) + "\n")

    f.close()

def print_to_file_by_ngram (ngram_list, filename):

    f = open(filename, 'w')

    for ngram_count in ngram_list:
        ngram = ''
        for gram in ngram_count[0]:
            ngram += gram + '\t'

        f.write(ngram + str(ngram_count[1]) + '\n')

    f.close()

def build_ngram_freq_list(file_list, n):
    """returns a list of words with calculated ngram frequences sorted by count,
    and one sorted by ngram"""

    ngram_count_dict = {}

    for filename in file_list:

        try:

            thisFile = "../stripped_text/" + filename
	
            ngram_count_dict =  build_ngram_dictionary (thisFile, ngram_count_dict, n)

        except IOError:

            pass
    
    sorted_by_count = sort_by_count (ngram_count_dict)
    sorted_by_ngram = sort_by_ngram (ngram_count_dict)

    return sorted_by_count, sorted_by_ngram

def build_ngram_dict_for_filelist(file_list, n):
    """similar to build_ngram_freq_list, but returns a dictionary, not lists"""

    ngram_count_dict = {}
    
    for filename in file_list:
        
        ngram_count_dict = build_ngram_dictionary (filename, ngram_count_dict, n)

    return ngram_count_dict
    
