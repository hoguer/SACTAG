#!/Usr/bin/env python
# 
# Copyright 2010  Niniane Wang (niniane@gmail.com)
# Reviewed by Alex Mendes da Costa.
# 
# This is a simple Tf-idf library.  The algorithm is described in
#   http://en.wikipedia.org/wiki/Tf-idf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = "Niniane Wang, edited by Rachel Hogue"
__email__ = "niniane at gmail dot com"

import math
import re
from operator import itemgetter
from helper_functions import rpartition
#from nltk import ngrams

class TfIdf:

  """Tf-idf class implementing http://en.wikipedia.org/wiki/Tf-idf.
  
     The library constructs an IDF corpus and stopword list either from
     documents specified by the client, or by reading from input files.  It
     computes IDF for a specified term based on the corpus, or generates
     keywords ordered by tf-idf for a specified document.
  """

  def __init__(self,spread,variant_word_order, corpus_filename = None,corpus = None, stopword_filename = None, DEFAULT_IDF = 1.5):
    """Initialize the idf dictionary.  
    
       If a corpus file is supplied, reads the idf dictionary from it, in the
       format of:
         # of total documents
         term: # of documents containing the term

       If a stopword file is specified, reads the stopword list from it, in
       the format of one stopword per line.

       The DEFAULT_IDF value is returned when a query term is not found in the
       idf corpus.
    """
    self.spread = spread
    self.vwo = variant_word_order
    self.num_docs = 0
    self.term_num_docs = {}     # term : num_docs_containing_term
    self.idf_default = DEFAULT_IDF

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

#we should have it so that you can call create_idf_corpus(subcorpus, spread, etc), and it could make an idf object with
#attributes such as idf_dict, spread, etc. We should also have a create_stopword_file(). Finally, we should have a compare()
#method and a graph() method and a generate_tfidf_scores() method for one author. 

    if corpus:
      self.term_num_docs = corpus
    elif corpus_filename:
      corpus_file = open(corpus_filename, "r")

      # Load number of documents.
      line = corpus_file.readline()
      self.num_docs = int(line.strip())

      # Reads "term:frequency" from each subsequent line in the file.
      for line in corpus_file:
        tokens = rpartition(line, "\t")
        term = tokens[0].strip()
        frequency = int(tokens[2].strip())
        self.term_num_docs[term] = frequency


  def set_num_docs(self,num_docs):
    self.num_docs = num_docs

  def get_tokens(self, str, num):
    """Break a string into tokens, preserving URL tags as an entire token.

       This implementation does not preserve case.  
       Clients may wish to override this behavior with their own tokenization.
    """
    word_list = re.findall(r"\S+", str.lower())
    
    if num == 1:
      for item in word_list:
        item = (item, )
      return word_list
      
    else:
      print "getting ngrams from file. Spread: ", self.spread, ", numgrams: ", num, "variant word order: ", self.vwo
      n_grams = self.get_ngrams(word_list, num, self.spread, self.vwo)
      return n_grams

  def add_input_document(self, input, num = 1):
    """Add terms in the specified document to the idf dictionary."""
    self.num_docs += 1
    f = open(input, 'r') #added
    doc_text= f.read() #added
    ngrams = set(self.get_tokens(doc_text, num))
    for ngram in ngrams:
      if ngram in self.term_num_docs:
        self.term_num_docs[ngram] += 1
      else:
        self.term_num_docs[ngram] = 1

  def save_corpus_to_file(self, idf_filename, stopword_filename=None,     #normally stopword_filename is required
                          STOPWORD_PERCENTAGE_THRESHOLD = 1.10):
    """Save the idf dictionary and stopword list to the specified file."""
    output_file = open(idf_filename, "w")

    output_file.write(str(self.num_docs) + "\n")
    for term, num_docs in self.term_num_docs.items():
      ngram = ''
      if type(term).__name__ != 'tuple':
        term = (term, )
      for gram in term:
            ngram += gram + '\t'
      output_file.write(ngram + "\t" + str(num_docs) + "\n")

    sorted_terms = sorted(self.term_num_docs.items(), key=itemgetter(1),
                          reverse=True)
    if stopword_filename:
      print "stopword filename: ", stopword_filename
      stopword_file = open(stopword_filename, "w")
      for term, num_docs in sorted_terms:
        if num_docs < STOPWORD_PERCENTAGE_THRESHOLD * self.num_docs:
          break

        stopword_file.write(term + "\n")

  def get_num_docs(self):
    """Return the total number of documents in the IDF corpus."""
    return self.num_docs

  def get_idf(self, term):
    """Retrieve the IDF for the specified term. 
    
       This is computed by taking the logarithm of ( 
       (number of documents in corpus) divided by (number of documents
        containing this term) ).
     """

    #throw out the whole bigram if a stopword is in it:
    
    for word in self.stopwords:   #we need the condition "if any word in stopwords
      if word in term:            #is in term." This works for tuples; nice because
        return 0                  #partial strings return false: ex. "re" is not in
                                  #("redundant", "hippo"), but "redundant" is. 

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) / 
      (1 + self.term_num_docs[term]))

  def get_doc_keywords(self, curr_doc, num = 1):
    """Retrieve terms and corresponding tf-idf for the specified document.

       The returned terms are ordered by decreasing tf-idf.
    """
    tfidf = {}
    f = open(curr_doc, 'r') #added
    doc_text= f.read() #added
    tokens = self.get_tokens(doc_text, num)
    tokens_set = set(tokens)
    for ngram in tokens_set:
      # The definition of TF specifies the denominator as the count of terms
      # within the document, but for short documents, I've found heuristically
      # that sometimes len(tokens_set) yields more intuitive results.
      mytf = float(tokens.count(ngram)) / len(tokens)
      myidf = self.get_idf(ngram)
      tfidf[ngram] = mytf * myidf
    
    return sorted(tfidf.items(), key=itemgetter(1), reverse=True)


  def in_punctuation(self,c):
    return c in ".;"

  def get_ngrams(self,word_list, num_grams, spread, variant_order = True):
    output = []
    for i in range(0,len(word_list)):
      first_word = word_list[i]
      if not self.in_punctuation(first_word):
        output += self.ngrams_helper(word_list[i+1:], [[first_word]], num_grams, spread, variant_order)
    return output

  def ngrams_helper(self, word_list, ngrams, num_grams, spread, variant_order):

    for c in range(0,spread-1):
      if len(word_list) > c and self.in_punctuation(word_list[c]):
        word_list = word_list[0:c]
        
    new_ngrams = []
    for i in range(0,spread-1):
      if len(word_list) > i:
        for ngram in ngrams:
          if len(ngram) < num_grams:
            if self.vwo:
              new_ngram = sorted(ngram + [word_list[i]])
            else:
              new_ngram = (ngram + [word_list[i]])
            new_ngrams += [new_ngram]
        ngrams += new_ngrams
        new_ngrams = []

    ngrams = [tuple(ngram) for ngram in ngrams if len(ngram)==num_grams]
    return ngrams                                                                                                                                                                        
