#!/usr/bin/env python
# 
# Copyright 2009  Niniane Wang (niniane@gmail.com)
# Reviewed by Alex Mendes da Costa.
#
# This is a simple Tf-idf library.  The algorithm is described in
#   http://en.wikipedia.org/wiki/Tf-idf
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# Tfidf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details:
#
#   http://www.gnu.org/licenses/lgpl.txt

__author__ = "Niniane Wang, edited by Rachel Hogue"
__email__ = "niniane at gmail dot com, hoguer711 at gmail dot com"

import math
import re
from operator import itemgetter

class TfIdf:

  """Tf-idf class implementing http://en.wikipedia.org/wiki/Tf-idf.
  
     The library constructs an IDF corpus and stopword list either from
     documents specified by the client, or by reading from input files.  It
     computes IDF for a specified term based on the corpus, or generates
     keywords ordered by tf-idf for a specified document.
  """

  def __init__(self, corpus_filename = None, stopword_filename = None,
               ngram_size = 2, variant_word_order = False,
               window = None, DEFAULT_IDF = 1.5):
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
    self.num_docs = 0
    self.term_num_docs = {}     # term : num_docs_containing_term
    self.len_gram = ngram_size
    if window:
      self.window = window
    else:
      self.window = ngram_size
    self.vary_word_order = variant_word_order
    self.stopwords = []
    self.idf_default = DEFAULT_IDF

    if corpus_filename:
      self.get_corpus_from_file(corpus_filename)

    if stopword_filename:
      stopword_file = open(stopword_filename, "r")
      self.stopwords = [line.strip() for line in stopword_file]

  def get_corpus_from_file(self, filename):

    try:
      corpus_file = open(filename, "r")
    except IOError:
      print 'cannot open ', corpus_file

    # Load number of documents.
    line = corpus_file.readline()
    self.num_docs = int(line.strip())

    # Reads "ngram:frequency" from each subsequent line in the file.
    for line in corpus_file:
       tokens = line.rpartition("\t")
       term = tokens[0].strip()
       frequency = int(tokens[2].strip())
       self.term_num_docs[term] = frequency

  def get_tokens(self, str):
    """Break a string into tokens (ngrams)
    """
    word_list = re.findall(r"\S+", str.lower())
    
    if self.len_gram == 1:
      return [tuple([word]) for word in word_list]
    else:
      return self.get_ngrams(word_list)

  def get_ngrams(self, word_list):
    """Break a list of words into a list of ngram tuples based
    on variant word order and window parameters. 
    """
    output = []
    for i in range(0,len(word_list)):
      first_word = word_list[i]
      if not self.in_punctuation(first_word):
        output += self.ngrams_helper(word_list[i+1:], [[first_word]])
    return output

  def ngrams_helper(self, word_list, ngrams):

    #shorten word_list to go only up to punctuation
    #We are not interested in ngrams with punctuation
    #in the middle of them.
    for c in range(0,self.window-1):
      if len(word_list) > c and self.in_punctuation(word_list[c]):
        word_list = word_list[0:c]
        
    new_ngrams = []
    for i in range(0,self.window-1):
      if len(word_list) > i:
        for ngram in ngrams:
          if len(ngram) < self.len_gram:
            if self.vary_word_order:
              new_ngram = sorted(ngram + [word_list[i]])
            else:
              new_ngram = (ngram + [word_list[i]])
            new_ngrams += [new_ngram]
        ngrams += new_ngrams
        new_ngrams = []

    return [tuple(ngram) for ngram in ngrams if len(ngram)==self.len_gram]
    

  def in_punctuation(self,c):
    return c in ".;"
    
  def add_input_document(self, input):
    """Add terms in the specified document to the idf dictionary."""
    self.num_docs += 1
    try:
      f = open(input, 'r')
    except IOError:
      print 'cannot open ', input
    doc_text= f.read()
    ngrams = set(self.get_tokens(doc_text))
    for ngram in ngrams:
      if ngram in self.term_num_docs:
        self.term_num_docs[ngram] += 1
      else:
        self.term_num_docs[ngram] = 1

  def save_corpus_to_file(self, idf_filename="idf_dictionary.txt"):
    """Save the idf dictionary and stopword list to the specified file."""
    try:
      output_file = open(idf_filename, "w")
    except IOError:
      print 'cannot open ', idf_filename

    output_file.write(str(self.num_docs) + "\n")
    for ngram, num_docs in self.term_num_docs.items():
      ngram_string = '\t'.join(ngram)
      output_file.write(ngram_string + "\t" + str(num_docs) + "\n")

    output_file.close()
    print "Saved idf dictionary to ", idf_filename

  def get_num_docs(self):
    """Return the total number of documents in the IDF corpus."""
    return self.num_docs

  def get_idf(self, term):
    """Retrieve the IDF for the specified term. 
    
       This is computed by taking the logarithm of ( 
       (number of documents in corpus) divided by (number of documents
        containing this term) ).
     """

    #return idf=0 if stopwords are in ngram
    if set(term).intersection(self.stopwords):
      return 0

    if not term in self.term_num_docs:
      return self.idf_default

    return math.log(float(1 + self.get_num_docs()) / 
      (1 + self.term_num_docs[term]))

  def get_doc_keywords(self, curr_doc):
    """Retrieve terms and corresponding tf-idf for the specified document.

       The returned terms are ordered by decreasing tf-idf.
    """
    tfidf = {}
    try:
        f = open(curr_doc, 'r')
    except IOError:
        print 'cannot open ', curr_doc
    doc_text= f.read()
    tokens = self.get_tokens(doc_text)
    tokens_set = set(tokens)
    for ngram in tokens_set:
      mytf = float(tokens.count(ngram)) / len(tokens_set)
      myidf = self.get_idf(ngram)
      tfidf[ngram] = mytf * myidf

    return sorted(tfidf.items(), key=itemgetter(1), reverse=True)

