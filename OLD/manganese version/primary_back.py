import tfidf
from helper_functions import file_dict, print_to_csv_file, read_ngram_list_from_file
from ngram_generator import print_to_file_by_ngram
from prelim import setup
import os, glob, time

class tfidf_compare:

    def __init__(self, document1, document2, subcorpora, num_grams, variant_ngrams = False, spread = None, stopwords = True):
        self.doc1 = document1
        self.doc2 = document2
        self.subcorpora = subcorpora
        if stopwords:
            self.stopword_file = "../stopwords/All_0.4.txt"
            self.stopwords = True
        else:
            self.stopwords = False
            self.stopword_file = None
        self.idf_dict = None
        if spread == None:
            self.spread = num_grams
        else:
            self.spread = spread
        self.vary_defn = variant_ngrams
        self.num_grams = num_grams        

        self.doc1_tfidf_file = "../tfidf_scores/" + str(self.num_grams) + "/" + self.doc1 + "_" + self.subcorpora +"_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) + ".txt"
        self.doc2_tfidf_file ="../tfidf_scores/" + str(self.num_grams) + "/" + self.doc1 + "_" + self.subcorpora +"_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) + ".txt"
        

        self.master = [[],[],[]]
        self.dir = "../tfidf_compare/" + self.doc1 + "_" + self.doc2 + "_" + self.subcorpora + "/"

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        if not os.path.exists(self.dir + str(self.num_grams)):
            os.makedirs(self.dir + str(self.num_grams))
                        

    def compare(self):
        compare_file = self.dir + str(self.num_grams) + "/" + "_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) + ".txt"
        if os.path.exists(compare_file):
            self.master = self.get_compare_list_from_file(compare_file)
        else:
            if os.path.exists(self.doc1_tfidf_file):
                print "doc1 file already exists. Reading data from file"
                doc1list = self.read_ngram_list_from_file(self.doc1_tfidf_file)
            else:
                doc1list = self.tf_idf(self.doc1)
            if os.path.exists(self.doc2_tfidf_file):
                print "doc2 file already exists. Reading data from file"
                doc2list = read_ngram_list_from_file(self.doc2_tfidf_file)
            else:         
                doc2list = self.tf_idf(self.doc2)

            self.master = self.generate_list_of_shared_ngrams_with_tfidf_scores(doc1list, doc2list)

    def graph(self,percent = 1):
        self.master = self.sort_scores(self.master)
        docu1 = self.master[1][0,percent*len(self.master)]
        docu2 = self.master[2][0,percent*len(self.master)]
        # author 1 on x axis author 2 on y axis
        plt.scatter(docu1, docu2)
        plt.xlabel(self.doc1)
        plt.ylabel(self.doc2)

        #for i in range(len(author1)):
        #    plt.annotate(i,(author1[i],author2[i]))
        print "showing"
        plt.show()
         
        
    def get_compare_list_from_file(self,filename):
        f = open(filename, "r")
        ngrams= []
        docu1= []
        docu2= []
        ngrams = []
        for line in f:
            splitline = re.split("[\t\n]",line)
            ngrams.append(splitline[0])
            docu1.append(float(splitline[1]))
            docu2.append(float(splitline[2]))
        return [ngrams, docu1, docu2]

    def read_ngram_list_from_file(self,filename):

        output_list =[]

        f=open(filename, 'r')
        for line in f:
            line = line.strip('\n')
            line_array = line.split('\t')
            ngram = tuple(line_array[:-1])
            output_list.append((ngram, line_array[-1]))

        f.close()
        return output_list
                                        

    def generate_list_of_shared_ngrams_with_tfidf_scores(self,doc1_tfidf, doc2_tfidf):
        output_list=[]
        ngrams = []
        document1 = []
        document2 = []
        print "generating list, doc1_tfidf"
        print "doc2_tfidf"

        #make a list of ngrams without their tfidf scores
        doc1_ngrams =[]
        for item in doc1_tfidf:
            doc1_ngrams.append(item[0])
            for doc2_item in doc2_tfidf:
                doc2_item_score = float(doc2_item[1])
                ngram = doc2_item[0]
                if ngram in doc1_ngrams:
                    i = doc1_ngrams.index(ngram)
                    doc1_item = doc1_tfidf[i]
                    doc1_item_score = float(doc1_item[1])
                    if (doc1_item_score > 0) or (doc2_item_score > 0):
                        ngrams.append(ngram)
                        document1.append(doc1_item_score)
                        document2.append(doc2_item_score)
        output_list = [ngrams, document1, document2]
        self.shared_scores_to_file(output_list)
        return output_list

    def shared_scores_to_file(self, combo_list):
        print "in to_file, combo_list: ", combo_list
        combo_list = self.sort_scores(combo_list)
        toFile = ""
        for i in range(len(combo_list[0])):
            toFile += combo_list[0][i][0] + "," + combo_list[0][i][1] + "\t" +  str(combo_list[1][i]) + "\t" + str(combo_list[2][i]) + "\n"
        f = open(self.dir + str(num_grams) + "/" + self.subcorpora + "_" + str(self.spread) + "_" + "v" + str(self.vary_defn) + "_" + "sw" + str(self.stopwords), "w")
        f.write(toFile)
        f.close()

    def sort_scores(self, alist):
        ngrams = []
        docu1 = []
        docu2 = []
        print alist
        refpoint = max (alist[1] + alist[2])

        # combine scores from both authors by calculating distance to
        # reference point
        combined_scores =  map(lambda x,y:compute_score(refpoint,x, y), alist[1], alist[2])

        print sorted([(combined_scores[i], i) for i in range(len(combined_scores))])

        sorted_distances = sorted([(combined_scores[i], i) for i in range(len(combined_scores))])
        c = 0
        for item in sorted_distances:
            i = item[1]
            ngrams[c]= alist[0][i]
            docu1[c]= alist[1][i]
            docu2[c] = alist[2][i]
            c+=1
        return [ngrams, docu1, docu2]
        

        
    def compute_score (self, refpoint, score1, score2):
        d = self.distance ((refpoint, refpoint), (score1, score2))
        return d

    def distance (self, p1, p2):
        """
        Points p1 and p2 are represented as tuples of coordinates.
        """
        d = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        return d
    
    def tf_idf(self, document):
        """Returns the tf-idf score for ngrams for the document. The num_grams specifies the level of grams:
        words, bigrams, trigrams, etc. The function creates an idf corpus for the subcorpora. If the document
        is not in the subcorpora, it is also added to the idf corpus, so that each word appears in at least
        one document.
        Stopwords are optional, but if True, they are created based on the stopword_percentage_threshold
        parameter."""

        path = '../stripped_text/'

        idf_path = "../" + str(self.num_grams) + "grams/" + self.subcorpora + "_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) +  ".txt"
        
        if os.path.exists(idf_path):
            #idf corpus already exists
            print "idf corpus exists."

            #create tfidf object with existing corpus
            _tfidf = tfidf.TfIdf(self.spread, self.vary_defn, "../" + str(self.num_grams) + "grams/" + self.subcorpora + ".txt",self.idf_dict, self.stopword_file)

            #determine document TLG#### filename:
            filedict = file_dict('../ref_file.txt')
            docFilename = filedict[document][0]
        
        else:  #idf corpus not yet in existence
            print "creating idf corpus."
            docFilename = self.add_docs(document)
            _tfidf = tfidf.TfIdf(self.spread, self.vary_defn, None, self.idf_dict, self.stopword_file)
            


        #actually determine tf-idf score for ngrams in document:
        tfidf_list =  _tfidf.get_doc_keywords(path + docFilename, self.num_grams)

        #print tfidf scores to .txt and .csv:
        print_to_file_by_ngram(tfidf_list, "../tfidf_scores/" + str(self.num_grams) + "/" + document + "_" + self.subcorpora +  ".txt")
        print_to_csv_file("../tfidf_scores/" + str(self.num_grams) + "/" + document + "_" + self.subcorpora +  ".txt", self.num_grams)


        #save idf corpus for later use:
        _tfidf.save_corpus_to_file(idf_path)

        return tfidf_list
    
    def add_docs(self, document):
        """adds documents to idf corpus. returns the name of the file for document
        whose ngram tf-idf scores are to be determined."""

        filedict = file_dict('../ref_file.txt')
        path = '../stripped_text/'

        TLG_files = filedict[self.subcorpora]
        
        if filedict[document][0] not in TLG_files:
            TLG_files.append(filedict[document][0])

        f=open("curr_test.txt", 'w')
        f.write("spread\t" + str(self.spread) + "\nvariant\t" + str(self.vary_defn) + "\nstopwords\t" + str(self.stopwords) + "\nstopword_file\t"  + self.stopword_file + "\nnum_grams\t" + str(self.num_grams) + "\n$num_docs$\t" + str(len(TLG_files)))
        f.close()
        setup(TLG_files)
        print "going to master"
        os.system('./master.sh')

#        file_path = '../TLG_idf_files/' + str(self.spread) + "_" + "v" + str(self.vary_defn) + "_" + "sw" + str(self.stopwords) + "/"
#        num_files = len(os.listdir(file_path))
        
#        while len(TLG_files) != num_files:
#            time.sleep(60)
#            num_files = len(os.listdir(file_path))
            
        self.idf_dict = self.compile_idf_dict()
        #compile_TLG_idfs()
        #Change the tfidf() function that calls this one, so that it then uses the created dict for its idf dict. 
            
#        print "docs: ", tfidf_instance.get_num_docs()
#        for filename in filedict[self.subcorpora]:
#            print "adding ", filename
#            tfidf_instance.add_input_document(path + filename, self.num_grams)
#            print "docs: ", tfidf_instance.get_num_docs()
        
        #Check that document is also in the idf corpus
#        if filedict[document][0] not in filedict[self.subcorpora]:
#            print "document not in subcorpora."
#            print "adding it"
#            tfidf_instance.add_input_document(path + filedict[document][0], self.num_grams)
#            print "docs: ", tfidf_instance.get_num_docs()

        return filedict[document][0]

    def compile_idf_dict(self):

        idf_dict = {}
        
        path = '../TLG_idf_files/' + str(self.num_grams) + 'grams/' + str(self.spread) + "_" + "v" + str(self.vary_defn) + "_" + "sw" + str(self.stopwords) + "/"
        files = os.listdir(path)
        for infile in files:
            file = open(path + infile, 'r')
            num_docs = file.readline() #first line is number of docs in corpus
            for line in file:
                tokens = line.rpartition("\t")
                term = tokens[0].strip()
                frequency = int(tokens[2].strip())
                if term in idf_dict:
                    idf_dict[term] += frequency
                else:
                    idf_dict[term] = frequency
        idf_dict['$num_docs$'] = len(files)
        print 'num_docs', idf_dict['$num_docs$']
        return idf_dict
                                                                

    def create_stopword_file(self,subcorpora, stopword_percentage_threshold):
        """Creates a stopword file. Returns stopword filename."""

        _tfidf = tfidf.TfIdf()
        filedict = file_dict('../ref_file.txt')
        path = '../stripped_text/'
        for filename in filedict[self.subcorpora]:
            print filename
            _tfidf.add_input_document(path + filename)
        print str(stopword_percentage_threshold)
        _tfidf.save_corpus_to_file("../1grams/" + self.subcorpora + ".txt",
                               "../stopwords/" + self.subcorpora + "_" + str(stopword_percentage_threshold) +  ".txt",
                               stopword_percentage_threshold)

        return "../stopwords/" + self.subcorpora + "_" + str(stopword_percentage_threshold) +  ".txt" #returns stopword filename




# params: (self, document1, document2, subcorpora, num_grams, variant_ngrams = False, spread = None, stopwords = True)


history_3vfalseswtrue =  tfidf_compare('Thucydides_Hist.', 'Herodotus_Hist.', 'Hist.', 2, False, 3)
history_3vfalseswtrue.compare()



#atticprose4 =  tfidf_compare('Aeschines_Orat.','Demosthenes_Orat.', 'Attic_Prose', 3, True)
#atticprose4.compare()



#create_stopword_file('Attic_Prose',1.0)

