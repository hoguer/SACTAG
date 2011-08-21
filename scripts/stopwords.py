import os, re
from helper_functions import file_dict

def create_stopword_file(subcorpus, stopword_percentage_threshold, path_to_files, stopword_filename="stopwords.txt"):
    """Creates a stopword file. Returns stopword list"""

    #ref_file.txt contains the names and corresponding TLG files for authors and subcorpora
    filedict = file_dict('../test_ref.txt')

    # stores {word --> occurence} 
    stopwords = {}
        
    for filename in filedict[subcorpus]:
        stopwords = add_file_to_stopwords(path_to_files + filename, stopwords)

    num_docs = len(filedict[subcorpus])

    save_file(stopword_filename, stopwords, num_docs, stopword_percentage_threshold)

    print "created stopword file: ", stopword_filename 

    return stopwords


def add_file_to_stopwords(filename, stopwords):
    
    f = open(filename, 'r') 
    doc_text= f.read()
    word_list = re.findall(r"\S+", doc_text.lower())
    word_list = set(word_list)

    for word in word_list:
        if word in stopwords:
            stopwords[word] += 1
        else:
            stopwords[word] = 1

    return stopwords

    
def save_file(stopword_filename, stopwords, num_docs, percentage_threshold):

    stopword_file = open(stopword_filename, "w")

    for word, num in stopwords.iteritems():
        if not (num < (percentage_threshold * num_docs)):
            stopword_file.write(word + "\n")

    stopword_file.close()


#example for creating a stopword file with a subcorpus of all. In this example, words must appear in 10% of documents
#to be considered a stopword. 
#create_stopword_file('All',0.1, "files/")
