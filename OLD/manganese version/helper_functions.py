from ngram_generator import print_to_file_by_ngram, sort_by_count, print_to_file_by_freq

def ngram_prefix(n):
    """returns a string with a number prefix (bi, tri, etc) followed by gram"""
    options = {1: "word",
               2: "bigram",
               3: "trigram"
               }
    
    try:
        return options[n]
    except ValueError:
        print "That was not a valid number"

def file_dict(ref_file):
    """returns a dictionary of 'subcorpus: TLG file list' pairs from the reference
    file"""
    
    output_dict = {}
    for line in open(ref_file):
        line = line.strip()
        line_list = line.split('\t')
        for item in line_list:
            item = item.strip()
        output_dict[line_list[0]] = line_list[1:]

    return output_dict

def curr_test_dict(ref_file):
    output_dict = {}
    for line in open(ref_file):
        line = line.strip()
        line_list = line.split('\t')
        for item in line_list:
            item = item.strip()
            output_dict[line_list[0]] = line_list[1]

    return output_dict
                                                    

def create_filename(subcorpora_name):
    """Returns a string. Changes spaces and forward slashes to underscores and
    adds a .txt extension"""

    s = ''
    for c in subcorpora_name:
        if ord(c) == 32 or ord(c) == 47:
            s += '_'
        else:
            s += c
    s += '.txt'

    return s

def to_one_file(fileList, name):
    """compiles files in filelist to one file, stored in temp folder"""
    if len(fileList) == 1:
        return fileList[0]
    else:
        s = ''
        for File in fileList:
            x = open(File, 'r')
            s += x.read()

        output_file = '../temp/' + name + '.txt'
        f = open(output_file, 'w')
        f.write(s)
        f.close()

        return output_file

def print_to_csv_file(filename,n):
    filename_list = filename.split('/')
    filen = filename_list[-1]
    output_file_m = '../tfidf_csv_format/' + str(n) + '/' + filen[:-4] + '.csv'
    ngram_dict = {}
    for line in open(filename):
        ngram_list = line.split('\t')
        n_gram = insert_quotations(ngram_list[:-1])
        ngram = tuple(n_gram)
        freq = float(ngram_list[-1])
        ngram_dict[ngram] = freq
    sorted_ngrams = sort_by_count(ngram_dict, True)
    print_to_file_by_freq(sorted_ngrams,output_file_m)

def insert_quotations(ngram_list):
    
    output_list =[]
    
    for item in ngram_list:
        toAdd = "\'" + item + "\'"
        output_list.append(toAdd)
    return output_list

def read_ngram_list_from_file(filename):

    output_list =[]

    f=open(filename, 'r')
    for line in f:
        line = line.strip('\n')
        line_array = line.split('\t')
        ngram = tuple(line_array[:-1])
        output_list.append((ngram, line_array[-1]))

    f.close()
    return output_list
    
