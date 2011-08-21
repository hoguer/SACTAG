__author__ = "Rachel Hogue"
__email__  = "hoguer711 at gmail dot com"


class tfidf_compare:

    def __init__(self, document1, document2,    #documents to compare
                 corpus_name,                   #background corpus name, as stored in ref_file.txt
                 corpus_filename=None,          #corpus filename if the corpus already has been created and saved to a file
                 stopword_filename = None,      #file with list of stopwords
                 ngram_size = 2,                #length of ngrams
                 variant_word_order = False,    #example: if true, count bigram BA as occurence of bigram AB
                 window = None,                 #give a window in which to find a the words that make up an ngram so they don't
                                                # necessarily have to be consecutive. 
                 DEFAULT_IDF = 1.5):
        
        self.doc1 = document1
        self.doc2 = document2
        self.corpus_filename= corpus_filename
        self.stopword_filename = stopword_filename
        self.ngram_len = ngram_size
        self.vary_word_order = variant_word_order
        self.window = window
        self.compare_list = {} #[ [ngram1, ngram2, ...], [ngram1_doc1_tfidf_score, ngram2_doc1_tfidf_score, ...],
                               #  [ngram1_doc2_tfidf_score, ngram2_doc2_tfidf_score, ...] ]



    def compare(self, comparison_output_filename, document1_tfidf_output_filename, document2_tfidf_output_filename,
                comparison_file=None, document1_tfidf_file=None, document2_tfidf_file=None):
        """Compare document1 to document2 using their tfidf scores. If they have already been compared and
        saved to a file, the user can enter the path to that file using the comparison_file parameter. If the
        tfidf documents have been created already for either of the documents, those can also be passed to this
        function. """

        if os.path.exists(comparison_file):
            self.get_compare_list_from_file(comparison_file)
        else:
            if document1_tfidf_file:
                #get tfidf scores from the file
                try:
                    f = open(document1_tfidf_file, "r")
                except IOError:
                    print 'cannot open ', document1_tfidf_file
                
                doc1_scores = self.read_ngram_dict_from_file(document1_tfidf_file)
            else:
                print "document1 tfidf file does not exist yet. Creating tfidf score file for document1."
                doc1_scores = self.tf_idf(self.doc1)


            if document2_tfidf_file:
                #get tfidf scores from the file
                try:
                    f = open(document2_tfidf_file, "r")
                except IOError:
                    print 'cannot open ', document2_tfidf_file
                
                doc2_scores = self.read_ngram_dict_from_file(document2_tfidf_file)
            else:
                print "document2 tfidf file does not exist yet. Creating tfidf score file for document2."
                doc2_scores = self.tf_idf(self.doc2)

            self.master = self.generate_list_of_shared_ngrams_with_tfidf_scores(doc1list, doc2list)


    def get_tfidf_scores(self, document):
        
        tfidf_object = tfidf.TfIdf(self.corpus_filename, self.stopword_filename, self.ngram_len, self.vary_word_order,
                                   self.window)

        if 


        
            
        

    def get_compare_list_from_file(self, filename):
        """If a comparison list has already been created and saved to a file for the two documents, extract the
        ngrams and tfidf scores from the file."""

        try:
            f = open(filename, "r")
        except IOError:
            print 'cannot open ', filename

        ngrams= []
        document1_scores= []
        document2_scores= []
        
        for line in f:
            splitline = re.split("[\t\n]",line)
            ngrams.append(splitline[0])
            document1_scores.append(float(splitline[1]))
            document2_scores.append(float(splitline[2]))

        self.compare_lists = [ngrams, document1_scores, document2_scores]

    def read_ngram_dict_from_file(self, filename):
        """Extract the {ngram => tfidf score, ...} dictionary from the given filename"""

        try:
            f = open(filename, "r")
        except IOError:
            print 'cannot open ', filename

        output_dict ={}

        for line in f:
            line = line.strip('\n')
            line_array = line.split('\t')
            ngram = tuple(line_array[:-1])
            output_dict[ngram]= line_array[-1]

        f.close()
        return output_dict
