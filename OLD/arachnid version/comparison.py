import os
from helper_functions import read_ngram_list_from_file

class comparison:
    def __init__(self, document1, document2, subcorpus, num_grams, variant_ngrams = False, spread = None, stopwords = True):
	self.doc1 = document1
       	self.doc2 = document2
        self.subcorpora = subcorpus
        if stopwords:
            self.stopword_file = "../stopwords/All_0.4.txt"
            self.stopwords = True
        else:
            self.stopwords = False
            self.stopword_file = None
        if spread == None:
            self.spread = num_grams
        else:
            self.spread = spread
        self.vary_defn = variant_ngrams
        self.num_grams = num_grams

        self.doc1_tfidf_file = "../tfidf_scores/" + str(self.num_grams) + "/" + self.doc1 + "_" + self.subcorpora +"_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) + ".txt"
        self.doc2_tfidf_file ="../tfidf_scores/" + str(self.num_grams) + "/" + self.doc2 + "_" + self.subcorpora +"_v_" + str(self.vary_defn) + "_sw_" + str(self.stopwords) + "_s_" + str(self.spread) + ".txt"


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
                doc1list = read_ngram_list_from_file(self.doc1_tfidf_file)
            else:
                print "doc1 file does not exist yet. Please create tfidf score file for doc1."
            if os.path.exists(self.doc2_tfidf_file):
                print "doc2 file already exists. Reading data from file"
                doc2list = read_ngram_list_from_file(self.doc2_tfidf_file)
            else:
                print "doc2 file does not exist yet. Please create tfidf score file for doc2."

            self.master = self.generate_list_of_shared_ngrams_with_tfidf_scores(doc1list, doc2list)


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



#test1 = comparison('Thucydides_Hist.', 'Herodotus_Hist.','Hist.',2, False, 2)
#test1.compare()


#test2 = comparison('Thucydides_Hist.', 'Herodotus_Hist.','Hist.',2, True, 3)
#test2.compare()


test3 = comparison('Thucydides_Hist.', 'Herodotus_Hist.','Hist.',2, True, 2)
test3.compare()

