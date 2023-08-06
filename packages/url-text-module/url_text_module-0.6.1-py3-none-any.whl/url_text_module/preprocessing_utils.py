import pandas as pd
import numpy as np

import json
from urllib.request import urlopen

# Preprocessing
from sklearn.preprocessing import StandardScaler

from transformers import AutoTokenizer, BertPreTrainedModel
from transformers.modeling_outputs import BaseModelOutput

from datasets import Dataset, DatasetDict

import torch

from typing import List, Set, Type, Optional

from .classes import Featurization

from .misc_utils import determine_device

from .constants import (
  BERT_NAME, 
  BIGRAM_NAME, 
  FUGASHI_STR, 
  FUGASHI_TAGGER, 
  HF_BERT_MODELS, 
  INPUT_COL_NAME, 
  EMBEDDINGS_COL_NAME, 
  LEMMATIZE_KEY, 
  MODEL_BASE_TYPE_KEY, 
  MODEL_HF_HUB_NAME_KEY, 
  REVISION_HASH_KEY, 
  STOPWORDS_KEY, 
  STOPWORDS_URL_KEY, 
  TFIDF_NAME, 
  TOKENIZED_WITH_KEY, 
  UNIGRAM_NAME
)

def load_stopwords_json(stopwords_url: str) -> Set[str]:
    """Fetches a JSON at URL stopwords_url and returns the set of stopwords located at that URL

    Args:
        stopwords_url: String of the URL where the JSON of stopwords is located
    
    Returns:
        stopwords: Set of stopwords located stopwords_url
    """
    f = urlopen(stopwords_url)
    stopwords = set(json.load(f))
    return stopwords

def tokenize_with_fugashi(
    text: str, 
    tagger = FUGASHI_TAGGER, 
    lemmatize: bool = False, 
    stopwords: Optional[Set[str]] = None
) -> List[str]:
    """Returns tokens found using the fugashi Japanese text Python package. Enables options
          for additional preprocessing of the text including removing stopwords and subsequently
          reducing tokens to their lemma representations

    Args:
        text:       String input to be split into tokens
        tagger:     Tagger instance developed on Japanese text, capable of 
                        taking an input string and providing a list of word tokens
                        and other associated metadata for each token, i.e. its lemma
                        representation
        lemmatize:  Boolean indicating if tokens should be processed to their lemma form
        stopwords:  Set of stopwords used to remove tokens from the final list which are
                        are considered noise to the input 
    
    Returns:
        tokenized_words: List of processed tokens
    """
    def remove_stopwords_func(word_objs, stopwords_set):
      return [word for word in word_objs if word.surface not in stopwords_set]
    word_objs = tagger(text)
    if stopwords: 
      word_objs = remove_stopwords_func(word_objs, stopwords)
    tokenized_words = [word.feature.lemma if lemmatize else word.surface for word in word_objs]
    return tokenized_words

class PretrainedBERTTokenizerAndModel:
    """Class for fetching tokenizer & torch model for a pretrained BERT model
        for performing tokenization of text inputs & performing CLS Pooling
        to extract numerical embeddings

    Args:
      auto_BERT_model_base: Reference to specific BERT model class in HuggingFace, 
                              e.g. AutoModelForMaskedLM
      model_hf_hub_name:    String which identifies specific pretrained BERT model 
                              on HuggingFace Hub
      revision_hash:        String hash which indicates which version of a pretrained tokenizer
                              and model to use when constructing this class. Useful for reproducibility.
                              Defaults to None
    """
    def __init__(
      self, 
      auto_BERT_model_base: Type[BertPreTrainedModel], 
      model_hf_hub_name: str, 
      revision_hash: Optional[str] = None
    ) -> None:
        self.device, _ = determine_device()
        if revision_hash:
          # Use specific version of tokenizer & model -- recommended for reproducibility
          self.tokenizer = AutoTokenizer.from_pretrained(model_hf_hub_name, revision = revision_hash)
          self.model = auto_BERT_model_base.from_pretrained(model_hf_hub_name, revision = revision_hash, output_hidden_states = True)
        else:
          # Use latest version of tokenizer& model
          self.tokenizer = AutoTokenizer.from_pretrained(model_hf_hub_name)
          self.model = auto_BERT_model_base.from_pretrained(model_hf_hub_name, output_hidden_states = True)
        self.model.to(self.device)
    
    def tokenize(self, input: str):
      """Returns tokens from input text string which are used as input 
            to a HuggingFace BERT-based model

      Args:
          input:  String input to be split into tokens
      
      Returns:
          tokens: List of tokens found for raw input input
      """
      return self.tokenizer.tokenize(input)

    def create_tokenized_hf_dataset_dict(
      self, 
      data_df: pd.Series, 
      columns_to_keep: Optional[Set[str]] = None
    ) -> DatasetDict:
      """Returns a HuggingFace DatasetDict which has the necessary
          data columns to create CLS Pooling embeddings using a pretrained
          BERT model

      Args:
          data_df:           DataFrame which has original text data which will be tokenized by this method. 
                              data_df is required to have input text strings under the column named
                              INPUT_COL_NAME
          columns_to_keep:   Set of columns from data_df to keep in final dataset within the returned
                              tokenized_dataset. Default is None
      
      Returns:
          tokenized_dataset: DatasetDict which has data columns useful for CLS Pooling using a
                              pretrained BERT model
      """
      hf_dataset = Dataset.from_pandas(data_df)
      all_columns = hf_dataset.column_names
      if columns_to_keep:
          columns_to_remove = columns_to_keep.symmetric_difference(all_columns)
          hf_dataset = hf_dataset.remove_columns(columns_to_remove)
      dataset_dict = DatasetDict({
        "train": hf_dataset
      })
      tokenized_dataset = dataset_dict.map(lambda x: self.tokenizer(x[INPUT_COL_NAME]), batched = True)
      return tokenized_dataset
    
    ## Code inspired from this tutorial on HuggingFace (https://huggingface.co/course/chapter5/6?fw=pt)
    def cls_pooling(self, model_output: BaseModelOutput) -> torch.Tensor:
        """Returns the last hidden-state tensor associated with the prepended [CLS] token of the input,
            yields a contextualized embedding of the model output for an tokenized input string

        Args:
            model_output:     Output from feeding a tokenized input to a pretrained BERT model. 
                                Has fields useful for performing CLS pooling including tensors for
                                each hidden state from processing the input using the model
        
        Returns:
            cls_hidden_state: Last hidden state tensor of a pretrained BERT model associated with the [CLS] token
                                which is prepended to the input. Tensor is of shape 1 x 768
        """
        hidden_states = model_output.hidden_states
        last_hidden_state = hidden_states[-1]
        cls_hidden_state = last_hidden_state[:, 0]
        return cls_hidden_state

    def get_embedding(self, text_input: str) -> torch.Tensor:
        """Returns CLS Pooling embedding for text string input text_input using the pretrained BERT model self.model 

        Args:
            text_input:           Input text to be embedded using self.model
        
        Returns:
            cls_pooled_embedding: Tensor of the last hidden state of self.model for the [CLS] token prepended to the text_input
                                    providing a contextualized embedding of the entire input string
        """
        encoded_input = self.tokenizer(
            text_input, padding = True, truncation = True, return_tensors = "pt"
        )
        self.model.eval() # Important to turn off dropout!!
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        model_output = self.model(**encoded_input)
        cls_pooled_embedding = self.cls_pooling(model_output)
        return cls_pooled_embedding
    
    def embed_data_df(
      self, 
      data_df: pd.DataFrame, 
      columns_to_keep: Optional[Set[str]] = None
    ) -> pd.DataFrame:
        """Returns a pandas DataFrame which retains columns_to_keep & is given the EMBEDDINGS_COL_NAME column,
            embedding the input text data in the column INPUT_COL_NAME using the pretrained BERT model, 
            self.model, by applying CLS Pooling. data_df must have INPUT_COL_NAME column

        Args:
            data_df:           DataFrame which has original text data which will be embedded by this method. 
                                data_df is required to have input text strings under the column named
                                INPUT_COL_NAME
            columns_to_keep:   Set of columns from data_df to keep in final returned embeddings_df. Default is None
        
        Returns:
            embeddings_df:     DataFrame which has both EMBEDDINGS_COL_NAME containing the CLS Pooling embeddings found
                                for the input text strings in INPUT_COL_NAME in data_df and columns maintained from
                                columns_to_keep parameter
        """
        tokenized_data_dict = self.create_tokenized_hf_dataset_dict(
          data_df, 
          columns_to_keep = columns_to_keep
        )
        embeddings_data_dict = tokenized_data_dict.map(
          lambda x: {EMBEDDINGS_COL_NAME: self.get_embedding(x[INPUT_COL_NAME]).detach().cpu().numpy()[0]}
        )
        # Create dataframe with CLS Pooling Embeddings
        embeddings_data_dict.set_format('pandas')
        embeddings_df = embeddings_data_dict['train'][:]
        return embeddings_df

def create_input_string_preprocessor(featurization: Featurization) -> np.ndarray:
  """Uses featurization metadata to load the proper input string preprocessor in order to provide
      the proper, possibly cleaned input to the featurizer
  
  Args:
    featurization: Featurization containing various pieces of metadata pertaining to the transformation of the input string to a feature vector

  Return:
    input_str_preprocessor: function which takes an input string as input and returns a numpy array corresponding
                              to the feature embedding
  """
  featurization_metadata_dict = featurization.metadata
  if featurization.type == UNIGRAM_NAME or featurization.type == BIGRAM_NAME or featurization.type == TFIDF_NAME:
    stopwords_metadata = featurization_metadata_dict[STOPWORDS_KEY]
    lemmatize = featurization_metadata_dict[LEMMATIZE_KEY]
    if stopwords_metadata is None:
      stopwords = None
    else:
      stopwords = load_stopwords_json(stopwords_metadata[STOPWORDS_URL_KEY]) if STOPWORDS_URL_KEY in stopwords_metadata else set(stopwords_metadata)
    if featurization_metadata_dict[TOKENIZED_WITH_KEY] == FUGASHI_STR:
      return lambda input_str: tokenize_with_fugashi(input_str, lemmatize = lemmatize, stopwords = stopwords).to_numpy()
  elif featurization.type == BERT_NAME:
    auto_model_base, model_hf_hub_name = featurization_metadata_dict[MODEL_BASE_TYPE_KEY], featurization_metadata_dict[MODEL_HF_HUB_NAME_KEY]
    auto_bert_model = HF_BERT_MODELS[auto_model_base]
    revision_hash = featurization_metadata_dict[REVISION_HASH_KEY] if REVISION_HASH_KEY in featurization_metadata_dict else None
    bert_tokenizer_and_model = PretrainedBERTTokenizerAndModel(auto_bert_model, model_hf_hub_name, revision_hash = revision_hash)
    return lambda input_str: bert_tokenizer_and_model.get_embedding(input_str).detach().cpu().numpy()
  else:
    print('Not a valid featurization type')
    

def standardize_X(raw_X: np.ndarray) -> np.ndarray:
  """Standardizes data in raw_X returns scaled_X (zero-mean, unit variance for each feature) which has
        the same shape as raw_X
  Args:
    raw_X: unstandardized Numpy matrix of data of shape num. of data points by num. of features 
  
  Returns:
    scaled_X: standardized Numpy matrix of raw_X, i.e. each feature now has zero-mean & unit variance.
  """
  scaler = StandardScaler()
  scaled_X = scaler.fit_transform(raw_X)
  return scaled_X

