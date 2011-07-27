import os
from helper_functions import file_dict

class idf:

    def __init__(self, file_path, subcorpus, num_grams, variant_word_order, spread, stopword_file=None):
        self.subcorpus = subcorpus
        self.num_grams = num_grams
        self.variant = variant_word_order
        self.spread = spread
        self.stopword_file = stopword_file
        self.stopwords = False
        
        if stopword_file:
            self.stopwords = True
        
        self.ref_dict = file_dict('../ref_file.txt')
        self.num_docs = len(self.ref_dict[self.subcorpus])
        self.file_path = file_path

        self.idf_files_path = "../idf_files/" + str(self.num_grams) + 'grams/' + \
            str(self.spread) + "_v" + str(self.variant) + "_sw" + str(self.stopwords) + "/"
        
        if not os.path.exists(self.idf_files_path):
            os.makedirs(self.idf_files_path)

        self.idf_dict_file = "../" + str(self.num_grams) + "grams/" \
            + self.subcorpus + "_v" + str(self.variant) + "_sw"\
            + str(self.stopwords) + "_s" + str(self.spread) + ".txt"
        
        if not os.path.exists(idf_dict_file):
            self.create_idf_dictionary()

    def create_idf_dictionary(self):
        
        idf_dictionary = {}
        for file in self.ref_dict[self.subcorpus]:
            idf_dictionary = self.add_document(file, idf_dictionary)

        save_to_file(idf_dictionary)
            
    def add_document(self, file, dictionary):
        
        if not os.path.exists(self.idf_files_path + file):
            f = open(input, 'r')
            doc_text = f.read()
            ngrams = set(self.get_tokens(doc_text))
            #SAVE TO FILE
        else:
            #read from file
            file = open(self.idf_files_path + file, 'r')
            ngrams = []
            for line in file:
                tokens = line.rpartition('\t')
                term = tuple(tokens[0].split('\t'))
                ngrams.append(tuple)

        for ngram in ngrams:
            if ngram in dictionary:
                dictionary[ngram] += 1
            else:
                dictionary[ngram] = 1

            
    def get_tokens(self, str):
        """Break a string into ngrams"""
        word_list = re.findall(r"\S+", str.lower())

        if self.num_grams == 1:
            for item in word_list:
                item = (item, )
            return word_list

        else:
            n_grams = self.get_ngrams(word_list)
        
        return n_grams

    def get_ngrams(self, word_list):
        
        output = []
        for i in range(0, len(word_list)):
            first_word = word_list[i]
            if not self.in_punctuation(first_word):
                output += self.ngrams_helper(word_list[i+1:], [[first_word]])
        return output

    def in_punctuation(self, word):
        return word in ".;"

        
    def ngrams_helper(self, word_list, ngrams):
        
        for c in range(0, self.spread-1):
            if len(word_list) > c and self.in_punctuation(word_list[c]):
                word_list = word_list[0:c]

        for i in range(0, self.spread-1):
            if len(word_list) > i:
                for ngram in ngrams:
                    new_ngrams = []
                    if len(ngram) < self.num_grams:
                        if self.variant:
                            new_ngram = sorted(ngram + [word_list[i]])
                        else:
                            new_ngram = (ngram + [word_list[i]])
                        new_ngrams += [new_ngram]
                    ngrams += new_ngrams
        ngrams = [tuple(ngram) for ngram in ngrams if len(ngram)==num_grams]
        return ngrams
            

test = idf('Attic_Prose', 2, True, 2)
print test.subcorpus
        
