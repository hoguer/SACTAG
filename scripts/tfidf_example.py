import tfidf
from stopwords import *

#test1, all parameters set to default
mytfidf = tfidf.TfIdf()

mytfidf.add_input_document("../test_files/kowari.txt")
mytfidf.add_input_document("../test_files/platypus.txt")
mytfidf.save_corpus_to_file(idf_filename="test1.txt")

#test2, turn on variant word order
mytfidf = tfidf.TfIdf(variant_word_order=True)

mytfidf.add_input_document("../test_files/kowari.txt")
mytfidf.add_input_document("../test_files/platypus.txt")
mytfidf.save_corpus_to_file(idf_filename="test2.txt")

#test3, try with trigrams
mytfidf = tfidf.TfIdf(ngram_size=3)

mytfidf.add_input_document("../test_files/kowari.txt")
mytfidf.add_input_document("../test_files/platypus.txt")
mytfidf.save_corpus_to_file(idf_filename="test3.txt")

#test4, try giving it a window of 4
mytfidf = tfidf.TfIdf(window=4)

mytfidf.add_input_document("../test_files/kowari.txt")
mytfidf.add_input_document("../test_files/platypus.txt")
mytfidf.save_corpus_to_file(idf_filename="test4.txt")

#test5 Let's give it a stopword percentage threshold of 1,
#since we're only dealing with two files. If a word is in
#both, it's a stopword.
create_stopword_file("test", 1.0, "../test_files/")

mytfidf = tfidf.TfIdf(stopword_filename="stopwords.txt")

mytfidf.add_input_document("../test_files/kowari.txt")
mytfidf.add_input_document("../test_files/platypus.txt")
mytfidf.save_corpus_to_file(idf_filename="test5.txt")

print mytfidf.get_doc_keywords("../test_files/platypus.txt")
