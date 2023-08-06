# Code inspired from https://stackabuse.com/python-for-nlp-creating-bag-of-words-model-from-scratch/
import numpy as np

from collections import Counter

from nltk.util import ngrams
from copy import copy

# sklearn Customs
from sklearn.base import BaseEstimator, TransformerMixin

from typing import Dict, List, Optional, Tuple, Union

# Helpers
def create_n_grams_counter(tokenized_docs: List[List[str]], n: int) -> Counter:
  """Creates counter for each unique n-gram found across the tokenized documents in
      tokenized_docs

  Args:
      tokenized_docs: List of tokenized documents, which are themselves a list of document tokens
  
  Returns:
      n_grams_counter: Counter which has the count of each unique n-gram across the tokenized documents
                        in tokenized_docs. Counter can be indexed for the count with an n-gram tuple
  """
  n_grams_counter = Counter()
  for doc in tokenized_docs:
    n_gram_rep_list = list(ngrams(doc, n))
    n_grams_counter.update(n_gram_rep_list)
  return n_grams_counter
  
def find_most_freq_n_grams(n_grams_counter: Counter, k: Optional[int] = None) -> List[Tuple[Tuple[str, ...], int]]:
  """Returns the top k most frequent n-gram in n_grams_counter

  Args:
      n_grams_counter: n-grams counter found for a corpus of tokenized documents
      k: Integer denoting the number of top-k n-grams in n_grams_counter to return. Defaults is None,
          in which all n-grams are returned
  
  Returns:
      most_freq: List of tuples denoting top-k most frequent n-grams in n_grams_counter, 
                  ordered from most frequent to least frequent. Structure of most_freq is such that
                  most_freq[0] is the most frequent n-gram in n_grams_counter, where
                  most_freq[0][0] is the n-gram tuple representation and most_freq[0][1] is the
                  associated count of the n-gram found from the n_grams_counter
  """
  if k is None:
    k = len(n_grams_counter)
  assert k <= len(n_grams_counter)
  most_freq = n_grams_counter.most_common(k)
  return most_freq

def compute_term_freq(tokenized_doc: List[str], query_n_gram_tup: Tuple[str, ...], n: int, normalize: bool = False) -> Union[int, float]:
  """Returns the frequency/count of an n-gram query_n_gram_tup in the tokenized document tokenized_doc

  Args:
      tokenized_doc:    List of tokens for a document
      query_n_gram_tup: Tuple of token strings representing the query n-gram for the n-grams found for the tokenized_doc
      n:                n denotes how to create n-grams from tokenized_doc, i.e. creating n-grams from the tokens in tokenized_doc 
                          for which the query_n_gram_tup will be queried against
      normalize:        Boolean determining if raw frequency count should be returned, or the count divided by the total number of n-grams
                         in the document, i.e. between 0-1. Default is False.
  
  Returns:
      term_freq:        Term frequency of the query_n_gram_tup (an n-gram) within the tokenized_doc broken into n-grams (specified by n)
  """
  ngram_rep_list = list(ngrams(tokenized_doc, n))
  total_num_n_grams = len(ngram_rep_list)
  doc_n_grams_counter = Counter(ngram_rep_list)
  n_gram_tup_occurences = doc_n_grams_counter[query_n_gram_tup]
  term_freq = n_gram_tup_occurences/total_num_n_grams if normalize else n_gram_tup_occurences
  return term_freq

# Vectorizers
class TextVectorizer(BaseEstimator, TransformerMixin):
  """Base class for text vectorizers, useful in the featurization of text strings

  Args:
      n: Used to create n-grams from a training corpus of tokenized documents. Default is 1, i.e. unigram-based features
      k_highest: Number of top most frequent n-grams to keep as features in final feature vector. 
                  Defaults to None, i.e. keeps all unique n-grams as features.
  
  Attributes:
      n: Used to create n-grams from a training corpus of tokenized documents. Default is 1, i.e. unigram-based features
      k_highest: Determines number of top most frequent n-grams to keep as features in final feature vector. 
                  Defaults to None, i.e. keeps all unique n-grams as features.
      n_grams_counter: Counter which has the cumlative count of each unique n-gram across the tokenized documents
                        in the training document corpus. Counter can be indexed for the count with an n-gram tuple. 
                        Defaults to None until fit or fit_transform methods are called
      idx_to_n_gram: Dictionary mapping the integer index in the feature vector to the n-gram in the vocabulary associated with that feature value
      n_gram_to_idx: Dictionary mapping an n-gram in the vocabulary to the integer index in the feature vector associated with that feature value
      vec_length: Number of unique n-grams forming the vocabulary, which is also the length of the feature vectors
  """
  def __init__(self, n: int = 1, k_highest: Optional[int] = None):
    self.n: int = n
    self.k_highest: int = k_highest
    self.n_grams_counter: Union[Counter, None] = None
    self.idx_to_n_gram: Dict[int, Tuple[str, ...]] = {}
    self.n_gram_to_idx: Dict[Tuple[str, ...], int] = {}
    self.vec_length: int = len(self.n_gram_to_idx)

  def get_most_freq(self) -> List[Tuple[Tuple[str, ...], int]]:
    """Returns self.k_highest most frequent (self.n)-grams & associated counts across training document corpus

    Returns:
      most_freq: List of tuples denoting top-(self.k_highest) most frequent (self.n)-grams across document
                  corpus, where most_freq[i][0] is the n-gram tuple representation and most_freq[i][1] is the
                  associated count of the cumlative occurences of the ith most-frequent n-gram in each document across all documents
                  in the corpus
    """
    try:
      most_freq = copy(self.most_freq)
      return most_freq
    except BaseException as error:
      print(f"An exception occured when getting most frequent grams list: {error}")
  
  def get_vocab(self) -> Dict[Tuple[str, ...], int]:
    """Returns vocabulary dictionary mapping a unique n-gram to unique integer index. This mapping is useful in building 
        the final feature vector for a document

    Returns:
      vocab_dict: Dictionary mapping all the self.k_highest unique (self.n)-grams observed across the training document corpus to
                    a unique integer index.
    """
    try:
      vocab_dict = copy(self.n_gram_to_idx)
      return vocab_dict
    except BaseException as error:
      print(f"An exception occured when getting the vocab dictionary: {error}")

  def _set_vec_length(self) -> int:
    # Sets the length of final feature vector during the fitting of vectorizer on a corpus of 
    # tokenized training documents, i.e. the corpus
    self.vec_length = len(self.n_gram_to_idx)

  def fit(self, training_docs: List[List[str]], y: Optional[any] = None) -> None:
    """Uses training document corpus of tokenized documents to fit the vectorizer, creating the 
        n-gram vocabulary, which is used in creating the feature vector representation of each document.
        For each unique n-gram, i, in the vocabulary, the feature value associated with the n-gram can be found at
        index i in the feature vector
    
    Args:
      training_docs: List of tokenized documents, which are themselves a list of document tokens, used to fit the vectorizer,
                      The fitted vectorizer can then be used for creating feature vectors for the training documents and 
                      future unseen documents, i.e. a test set of documents
      y:             Not used!
    """
    self.n_grams_counter = create_n_grams_counter(training_docs, self.n)
    self.most_freq = find_most_freq_n_grams(self.n_grams_counter, self.k_highest)
    self.n_gram_to_idx.update({self.most_freq[idx][0]: idx for idx in range(len(self.most_freq))})
    self.idx_to_n_gram.update({idx: self.most_freq[idx][0] for idx in range(len(self.most_freq))})
    self._set_vec_length()
  
  def get_n_gram_idx(self, n_gram: Tuple[str, ...]) -> int:
    """Returns index within the constructed feature vector for a unique n-gram, n_gram, in the vocabulary

    Returns:
        index: Integer index in the feature vector associated with the n-gram, n_gram.
    """
    index = self.n_gram_to_idx[n_gram]
    return index
  
  def construct_doc_vect_using_ngram(self, tokenized_doc: List[str]) -> np.ndarray:
    """Returns a feature vector for the tokenized_doc, which has a length equal to
        the number of unique n-grams in the corpus. Out-of-Vocabulary (OOV) n-grams
        present in the tokenized_doc are ignored
    """
    print("Implemented in subclasses")
    raise NotImplementedError

  def transform(self, tokenized_docs: List[List[str]], y: Optional[any] = None) -> np.ndarray:
    """Returns feature vectors created for the tokenized documents in tokenized_docs using the fitted vectorizer

    Args:
        tokenized_docs: List of tokenized documents, which are themselves a list of document tokens to transform into
                          feature vectors
        y:              Not used!

    Returns:
        doc_vecs: Numpy matrix of shape len(tokenized_docs) by the size of the vocabulary, corresponding to the
                    feature vectors of the documents in tokenized_docs
    """
    doc_vecs = np.zeros((len(tokenized_docs), len(self.n_gram_to_idx)))
    for i in range(len(tokenized_docs)):
      doc = tokenized_docs[i]
      doc_vecs[i, :] = self.construct_doc_vect_using_ngram(doc)
    return doc_vecs
  
  def fit_transform(self, training_docs: List[List[str]], y: Optional[any] = None) -> np.ndarray:
    """Convenience method which both fits the vectorizer using training_docs, creating the n-gram vocabulary, 
        and constructs & returns the feature vector representation of each document in training_docs
    
    Args:
      training_docs: List of tokenized documents, which are themselves a list of document tokens, used to fit the vectorizer.
                      The fitted vectorizer can then be used for creating feature vectors for the training documents and 
                      future unseen documents i.e. a test set of documents. These documents are transformed into feature vectors, 
                      i.e. transformed_input
      y:             Not used!

    Returns:
      transformed_input: Numpy matrix of shape len(training_docs) by the size of the fitted vocabulary, corresponding to the
                            feature vectors of the documents in training_docs
    """
    self.fit(training_docs)
    transformed_input = self.transform(training_docs)
    return transformed_input

class BOWVectorizer(TextVectorizer):
  """Bag-of-Words Vectorizer in which the features in the feature vector are simply the word counts 
      of the unique (self.n)-grams in the corpus vocabulary within the tokenized document
  """
  def construct_doc_vect_using_ngram(self, tokenized_doc):
    doc_vec = np.zeros((len(self.n_gram_to_idx),))
    doc_ngram_rep_set = set(ngrams(tokenized_doc, self.n))
    for n_gram_tup in doc_ngram_rep_set:
      # Skip OOV n-grams
      if n_gram_tup not in self.n_gram_to_idx:
        continue
      tf = compute_term_freq(tokenized_doc, n_gram_tup, self.n)
      n_gram_tup_idx = self.get_n_gram_idx(n_gram_tup)
      doc_vec[n_gram_tup_idx] = tf
    return doc_vec

# Code inspired from: https://www.askpython.com/python/examples/tf-idf-model-from-scratch

class TFIDFVectorizer(TextVectorizer):
  """Term-Frequency Inverse Document (TFIDF) Frequency Vectorizer in which the features in the feature vector 
      are the product of the frequency or normalized frequency (tf) of an n-gram, i, in a document  
      multipled by the inverse-document frequency (idf) which is the log(N/df_i) where N is the total number of 
      documents in the training corpus & df_i is the number of documents in the training corpus where
      n-gram i is present. Results in feature vectors where the features have value tf*idf.

  Args:
      n:            Used to create n-grams from a training corpus of tokenized documents. Default is 1, i.e. unigram-based features
      k_highest:    Determines number of top most frequent n-grams to keep as features in final feature vector. 
                      Default is None, i.e. keeps all unique n-grams as features.
      tf_normalize: Boolean indicating whether to use the normalized (between 0 to 1) or unnormalized term-frequency of an n-gram 
                      in a document when computing tf*idf. Default is False
  
  Attributes:
      n: Used to create n-grams from a training corpus of tokenized documents. Default is 1, i.e. unigram-based features
      k_highest: Determines number of top most frequent n-grams to keep as features in final feature vector. 
                  Defaults to None, i.e. keeps all unique n-grams as features.
      tf_normalize: Boolean indicating whether to use the normalized (between 0 to 1) or unnormalized term-frequency of an n-gram 
                      in a document when computing tf*idf. Default is False
      most_freq: List of tuples denoting top-(self.k_highest) most frequent n-grams in self.n_grams_counter, 
                  ordered from most frequent to least frequent. Structure of most_freq is such that
                  most_freq[0] is the most frequent n-gram in self.n_grams_counter, where
                  most_freq[0][0] is the n-gram tuple representation and most_freq[0][1] is the
                  associated count of the n-gram found from the self.n_grams_counter. 
                  Defaults to None until fit or fit_tranform methods are called
      n_grams_counter: Counter which has the cumlative count of each unique n-gram across the tokenized documents
                        in the training document corpus. Counter can be indexed for the count with an n-gram tuple. 
                        Defaults to None until fit or fit_transform methods are called
      idx_to_n_gram: Dictionary mapping the integer index in the feature vector to the n-gram in the vocabulary associated with that tf-idf feature value
      n_gram_to_idx: Dictionary mapping an n-gram in the vocabulary to the integer index in the tf-idf feature vector associated with that feature value
      n_gram_doc_count_dict: Dictionary mapping each unique n-gram tuple in the corpus vocabulary to the number of documents for which that is present, or the 
                              document frequency. Useful in determining df_i in computing inverse document frequency log(N/df_i), 
                              where df_i = self.n_gram_doc_count_dict[i] for n-gram tuple i. Defaults to None until fit or 
                              fit_tranform methods are called
      total_documents: Total number of documents in training document corpus, used for computing inverse document frequency, i.e. this is N in log(N/df_i) 
                        Defaults to None until fit or fit_tranform methods are called
  """
  def __init__(self, n = 1, k_highest = None, tf_normalize = False):
    self.n: int = n
    self.k_highest: int = k_highest
    self.tf_normalize: bool = tf_normalize
    self.most_freq: Union[List[Tuple[Tuple[str, ...], int]], None] = None
    self.n_grams_counter: Union[Counter, None] = None
    self.idx_to_n_gram: Dict[int, Tuple[str, ...]] = {}
    self.n_gram_to_idx: Dict[Tuple[str, ...], int] = {}
    self.n_gram_doc_count_dict: Union[Dict[Tuple[str, ...], int], None] = None
    self.total_documents: Union[int, None] = None
  
  def _compute_n_gram_doc_count_dict(self, training_docs: List[str]) -> Dict[Tuple[str, ...], int]:
    # Computes the dictionary mapping a unique n-gram tuple in the vocabulary to number of documents 
    # the n-gram appears in across the training corpus
    n_gram_doc_count_dict = {n_gram_tup: 0 for n_gram_tup in list(self.n_gram_to_idx.keys())}
    for doc in training_docs:
      doc_ngram_rep_set = set(ngrams(doc, self.n))
      for n_gram_tup in doc_ngram_rep_set:
        n_gram_doc_count_dict[n_gram_tup] += 1
    return n_gram_doc_count_dict
  
  def inverse_doc_freq(self, n_gram_tup: Tuple[str, ...]) -> float:
    """Returns the inverse document frequency of the n-gram n_gram_tup across the training document corpus

    Args:
      n_gram_tup: n-gram for which the inverse document frequency is being computed

    Returns:
      idf: Inverse document frequency found by taking the log(N/df_i), where N is the total number of documents
            in the training corpus and df_i is the number of documents in the training corpus where
            n-gram n_gram_tup is present.
    """
    n_gram_tup_occurence = self.n_gram_doc_count_dict[n_gram_tup]
    idf = np.log(self.total_documents/n_gram_tup_occurence)
    return idf
      
  def fit(self, training_docs, y = None):
    self.total_documents = len(training_docs)
    self.n_grams_counter = create_n_grams_counter(training_docs, self.n)
    self.most_freq = find_most_freq_n_grams(self.n_grams_counter, self.k_highest)
    self.n_gram_to_idx.update({self.most_freq[idx][0]: idx for idx in range(len(self.most_freq))})
    self.idx_to_n_gram.update({idx: self.most_freq[idx][0] for idx in range(len(self.most_freq))})
    self.n_gram_doc_count_dict = self._compute_n_gram_doc_count_dict(training_docs)
    self._set_vec_length()

  def construct_doc_vect_using_ngram(self, tokenized_doc):
    doc_tfidf_vec = np.zeros((len(self.n_gram_to_idx),))
    doc_ngram_rep_set = set(ngrams(tokenized_doc, self.n))
    for n_gram_tup in doc_ngram_rep_set:
      # Skip OOV n-grams
      if n_gram_tup not in self.n_gram_to_idx:
        continue
      tf = compute_term_freq(tokenized_doc, n_gram_tup, self.n, normalize = self.tf_normalize)
      idf = self.inverse_doc_freq(n_gram_tup)
      tfidf_score = tf*idf
      n_gram_tup_idx = self.get_n_gram_idx(n_gram_tup)
      doc_tfidf_vec[n_gram_tup_idx] = tfidf_score
    return doc_tfidf_vec