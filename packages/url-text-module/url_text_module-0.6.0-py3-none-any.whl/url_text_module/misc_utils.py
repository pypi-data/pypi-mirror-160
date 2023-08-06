import numpy as np
import pandas as pd

import random
import torch

import os
from os.path import join

import json

import joblib

from typing import Any, List, Dict, Optional, Tuple, Union

from .classes import Featurization, ModelMetadata

from .constants import (
    CLASS_NAME_TO_IDX_FILENAME,
    FEATURIZATION_KEY,
    HYPERPARAMETERS_KEY,
    MODEL_METADATA_FILENAME,
    NORMALIZER_TYPE_KEY,
    PACKAGE_VERSION_KEY,
    PICKLE_EXTENSION,
    RANDOM_STATE_KEY,
    __version__,
    DEFAULT_SEED,
    TRAINING_INDICES_KEY,
    TEST_INDICES_KEY,
    SORTED_FEATURIZATIONS_DICT,
    STD_TEST_SCORE_COL_NAME,
    MEAN_OUTER_FOLDS_SCORE_KEY,
    STD_OUTER_FOLDS_SCORE_KEY,
)

# Get Version of the URL Text Module
def get_version() -> str:
  """Gets version of the url_text_module package.
  
  Returns:
   __version__: version of the url_text_module package.
  """
  return __version__

def seed_everything(seed: int = DEFAULT_SEED) -> None:
  """Seeds everything to enable reproducible results
  
    Args:
      seed: Integer representing the random seed to use for all nondeterministic frameworks. 
              Defaults to 1
  """   
  random.seed(seed)
  os.environ['PYTHONHASHSEED'] = str(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)
  torch.cuda.manual_seed(seed)
  torch.cuda.manual_seed_all(seed)
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  torch.cuda.empty_cache()

def latexify_num(num: float) -> str:
  """Returns string formatted for rendering number in latex math mode

  Args:
    num: float number
  
  Returns: 
    latexified_num: num formatted for rendering in latex math mode as a string. For numbers whose absolute value is
                      between 1 to 9, the string returned is rounded to two decimal places. For numbers whose absolute value is
                      between 10-99, the string returned is rounded to one decimal place. For numbers whose absolute value is 
                      between 100-999, the returned string is rounded to the ones place. For numbers greater than or equal to 1000, 
                      the string is in scientific notation using two decimal places, for example:
                      num: 1010004.4 -> latexified_num: "$1.01\cdot10^{6}$".
  """
  if abs(num) >= 10**3:
    sci_notation = '{:.2e}'.format(num)
    split_str_list = sci_notation.split('e')
    trunc_num = split_str_list[0]
    exp = int(split_str_list[1])
    return f'${trunc_num}\cdot10^' + '{' + f'{exp}' '}$'
  elif abs(num) < 10**3 and abs(num) >= 10**2:
    return str(round(num))
  elif abs(num) < 10**2 and abs(num) >= 10:
    return str(round(num, 1))
  elif abs(num) < 10 and abs(num) >= 1:
    return str(round(num, 2))
  else:
    return str(round(num, 3))

def latexify_wcss_df(wcss_df: pd.DataFrame, col_names_list: List[str]) -> pd.DataFrame:
    """Return a DataFrame which has the Within-Cluster Sum-of-Squares (WCSS) values for various
        hyperparameter combinations (columns) at different values of K (rows) (i.e. different number of clusters) 
        formatted for rendering number in latex math mode

    Args:
      wcss_df: DataFrame containing WCSS scores for various values of K
      col_names_list: List of columns which will be latexified, i.e. WCSS scores which will be 
                        converted to a string which is formatted in Latex math mode. Please 
                        see latexify_num function for details on the float formatting
    
    Returns: 
      latexified_wcss_df: Copy of wcss_df with the WCSS scores converted to strings in latex math mode
    """
    latexified_wcss_df = wcss_df.copy()
    for col_name in col_names_list:
      latexified_wcss_df[col_name] = wcss_df[col_name].apply(latexify_num)
    return latexified_wcss_df

def compute_euclid_dist(list1: List[float], list2: List[float]) -> float:
  """Computes Euclidean Distance between two lists of floats
  
  Returns:
    euclid_dist: Euclidean distance between 
  """
  array1, array2 = np.array(list1), np.array(list2)
  euclid_dist = np.linalg.norm(array1 - array2)
  return euclid_dist

def get_top_k_tfidf_n_grams(
  tfidf_embedding: np.ndarray, idx_to_n_gram: Dict[int, Tuple[str, ...]], k: int = 10
) -> List[Tuple[Tuple[str, ...], float]]:
  """Returns k top n-grams by TF-IDF score in the tfidf_embedding vector
  
  Args:
    tfidf_embedding: Numpy vector where each index correspond to a unique n-gram
    idx_to_n_gram: Dictionary mapping index for tfidf_embedding to the associated n-gram
    k: Integer denoting number of top n-gram to return. Default is 10

  Returns:
    top_tfidf_n_gram_list: List of tuples for the k highest n-grams found in the tfidf_embedding, where
                            top_tfidf_n_gram_list[i][0] is the n-gram and top_tfidf_n_gram_list[i][1] is the TF-IDF score
                            for the i-th highest TF-IDF score in tfidf_embedding
  """
  top_indices = (-tfidf_embedding).argsort(kind = 'stable')[:k]
  top_tfidf_n_gram_list = [(idx_to_n_gram[idx], tfidf_embedding[idx]) for idx in top_indices]
  return top_tfidf_n_gram_list

def compute_splits_dict(cv: object, X: np.ndarray, y: np.ndarray) -> Dict[int, List[int]]:
  """Computes a dictionary mapping each unique splitting used in cross-validation
      to a dictionary mapping the training set and test set each to a list of data indices 

  Args: 
    cv: Cross validation instance which is used to split the data & labels X & y into the training and test sets in each split
    X: Numpy matrix of data points
    y: Integer labels assigned to data points in X
  
  Returns:
    splits_dict: Dictionary mapping integer split ID to a dictionary mapping the training fold (key: TRAINING_INDICES_KEY)
                    and test fold (key: TEST_INDICES_KEY) to a list of data indices corresponding to data & labels in X and y
                    which are in the respective sets
  """
  splits_dict = {}
  for idx, (train_indices, test_indices) in enumerate(cv.split(X, y)):
    splits_dict[idx] = {
        TRAINING_INDICES_KEY: train_indices.tolist(),
        TEST_INDICES_KEY: test_indices.tolist()
    }
  return splits_dict

def sort_featurization_grid(
    featurization_grid: List[Featurization]
  ) -> List[Featurization]:
  """Sorts a list of featurizatios based on the preset SORTED_FEATURIZATIONS_DICT

  Args:
    featurization_grid: List of featuriztions to use as input to the algorithm
  
  Returns:
    sorted_featurization_grid: Has same featurizations as featurization_grid except now sorted according to order specified
                                in SORTED_FEATURIZATIONS_DICT
  """
  featurization_to_idx = {value: key for key, value in SORTED_FEATURIZATIONS_DICT.items()}
  sorted_featurization_grid = sorted(featurization_grid, key = lambda feat: featurization_to_idx[feat.type])
  return sorted_featurization_grid

def extract_best_score_std_params(grid_search_obj: object) -> Tuple[float, Dict[str, List[Union[str, float, int, None]]]]:
  """Returns the best score, standard deviation, and parameters found from grid search

  Args: 
    grid_search_obj: Fitted grid search object
  
  Returns:
    best_score: Best avg. score found across the test folds of the fitted grid_search_obj
    best_std: Standard deviation of the score of the best hyperparameter + featurization comabination
                across test folds
    best_params: Hyperparameters which achieved the best avg. score found across the test folds
  """
  best_std = grid_search_obj.cv_results_[STD_TEST_SCORE_COL_NAME][grid_search_obj.best_index_]
  best_score, best_params = grid_search_obj.best_score_, grid_search_obj.best_params_
  return best_score, best_std, best_params

def pretty_print_cv_results(
  grid_obj: object, best_featurization: Featurization, optimize_metric: str
) -> None:
  """Prints the results a grid search cross validation procedure

  Args:
    grid_obj: Fitted grid search object
    best_featurization: Featurization to use as input to the algorithm
    optimize_metric: Metric optimized in the cross-validation procedure
  """
  best_score, best_std, best_params = extract_best_score_std_params(grid_obj)
  print(f'Best CV mean {optimize_metric} score: %.2f%%' % (best_score * 100))
  print(f'Best CV {optimize_metric} std: %.2f%%' % (best_std * 100))
  print('Best parameters:', best_params)
  best_featurization_type, best_featurization_named_params = best_featurization.type, best_featurization.named_parameters
  print('Best featurization type: ', best_featurization_type)
  print('Featurization Name Parameters: ', best_featurization_named_params)

def save_dict_as_json(parent_dir_path: str, json_filename: str, dict_to_save: Dict) -> None:
  """Saves a Python dictionary dict in the parent_dir_path directory on the host's filesystem as json_filename

  Args:
    parent_dir_path: Path to directory on host's filesystem where the json file will be saved
    json_filename: Name of the json file with the .json file extension
    dict_to_save: Python dictionary to be saved
  """
  json_file_path = join(parent_dir_path, json_filename)
  with open(json_file_path, 'w') as f:
    dict_as_json = json.dumps(dict_to_save)
    f.write(dict_as_json)

def read_json_as_dict(path_to_json_file: str) -> Dict:
  """Returns the Python dictionary version of a json located at path_to_json_file on
      the host's filesystem

  Args:
    path_to_json_file: Path to the json which will be converted to a dictionary on the host's filesystem
  
  Returns:
    data_dict: Dictionary version of the json located at path_to_json_file
  """
  with open(path_to_json_file, 'r') as f:
    data_dict = json.load(f)
  return data_dict

def prettify_algo_performance_dict(nested_cv_algo_performance_dict: Dict[str, Dict[str, float]]) -> Dict[str, Tuple[float, float]]:
  """Prettifies and returns a dictionary only containing the mean score and standard deviation of each algorithm in nested_cv_algo_performance_dict

  Args:
    nested_cv_algo_performance_dict: Nested dictionary containing a dictionary of scores on the outer cv splits of Nested CV for each algorithm used in Nested CV
      {
        <algo-1>: {
          split_0: <score-on-outer-split-0-test-fold>,
          ...,
          split_n: <score-on-outer-split-n-test-fold>,
          MEAN_OUTER_FOLDS_SCORE_KEY: <mean-score-on-outer-folds>,
          STD_OUTER_FOLDS_SCORE_KEY: <standard-deviation-on-outer-folds>
        }
        ... from algo-1 to algo-n
      }

  Returns:
    prettified_algo_performance_dict: Prettified dictionary of the structure:
      {
        <algo-1>: (<mean-score-on-outer-folds>, <standard-deviation-on-outer-folds>),
        ... from algo-1 to algo-n
      }
  """
  prettified_algo_performance_dict = {}
  for algo_name, outer_fold_score_dict in nested_cv_algo_performance_dict.items():
    mean_outer_fold_score, std_outer_fold_score = outer_fold_score_dict[MEAN_OUTER_FOLDS_SCORE_KEY], outer_fold_score_dict[STD_OUTER_FOLDS_SCORE_KEY]
    prettified_algo_performance_dict[algo_name] = (mean_outer_fold_score, std_outer_fold_score)
  return prettified_algo_performance_dict

def print_prettier_algo_performance_dict(
  prettified_algo_performance_dict: Dict[str, Tuple[float, float]], 
  optimize_metric: Optional[str] = None
) -> None:
  """Prints a prettified version of the results of Nested Cross Validation
      showing, for each algorithm, the mean score and standard deviation on the outer cv test folds
  
  Args:
    prettified_algo_performance_dict: Prettified dictionary of the structure:
      {
        <algo-1>: (<mean-score-on-outer-folds>, <standard-deviation-on-outer-folds>),
        ... from algo-1 to algo-n
      }
    optimize_metric: Name of the metric used to determine the best hyperparameter, featurization combination during nested CV. Is printed if provided
  """
  optimize_metric_str = f' ({optimize_metric})' if optimize_metric else ''
  print(f'Nested CV Outer Fold Scores{optimize_metric_str}:\n')
  for algo_name, (mean_outer_fold_score, std_outer_fold_score) in prettified_algo_performance_dict.items():
    print( f'   {algo_name}: {round(mean_outer_fold_score, 2)} +/- {round(std_outer_fold_score, 2)}\n')

def save_sklearn_model(fitted_sk_model: object, save_dir: str, model_name: str) -> str:
  """Saves a fitted scikit-learn model, fitted_sk_model, to host's filesystem as a pickle file
      at the location save_dir/{model_name}.pkl
  
  Args:
    fitted_sk_model: Fitted sklearn model
    save_dir: Path to directory on host's filesystem where the model will be saved
    model_name: name of the model, i.e. the name of the model's file before the pickle extension
  
  Returns:
    save_path: Path (including the filename) on the host where the model was saved
  """
  model_filename = f'{model_name}{PICKLE_EXTENSION}'
  save_path = join(save_dir, model_filename)
  joblib.dump(fitted_sk_model, save_path)
  return save_path

def load_sklearn_model(save_dir: str, model_name: str) -> object:
  """Loads a scikit-learn model from the host's filesystem to use for inferencing on new data

  Args:
    save_dir: Path to directory on host's filesystem where the model is stored
    model_name: Name of the model that prepends the filename of the model, i.e. {model_name}.pkl
  
  Returns:
    fitted_model: Fitted scikit-learn model, ready for inferencing
  """
  model_filename = f'{model_name}{PICKLE_EXTENSION}'
  path_to_file = join(save_dir, model_filename)
  fitted_model = joblib.load(path_to_file)
  return fitted_model

def create_directory_and_save_model_metadata(
  parent_dir: str, 
  model_metadata: ModelMetadata
) -> str:
    """Creates a directory on the host's filesystem for fitted model metadata including the model itself ({parent_dir}/{model_metadata.name}/{model_metadata.name}.pkl), its hyperparameters,
        the featurization used for the inputs, and the normalization applied to the inputs ({parent_dir}/{model_metadata.name}/{MODEL_METADATA_FILENAME})
    
    Args:
      parent_dir: Path to the directory the model_metadata.name directory will be created inside
      model_metadata: Stores various metadata about a model including the fitted model, the name to save the model as, the hyperparameters
                        used to develop the model, the featurization applied to the input to the model, the type of normalization applied to the input,
                        and the random state, or seed used to fit the model, and the mapping from class name string to
                        integer label
    
    Returns:
      model_dir_path: Path to the model directory that contains the fitted scikit-learn model ({model_dir_path}/{model_metadata.name}.pkl) and the 
                        hyperparameters and settings for the model and its inputs ({model_dir_path}/{MODEL_METADATA_FILENAME})
    """
    model_name, fitted_sk_model = model_metadata.name, model_metadata.fitted_model
    model_dir_path = join(parent_dir, model_name)
    os.mkdir(model_dir_path)
    saved_model_path = save_sklearn_model(fitted_sk_model, model_dir_path, model_name)
    model_metadata_dict = {
        HYPERPARAMETERS_KEY: model_metadata.hyperparameters,
        FEATURIZATION_KEY: named_tuple_as_dict(model_metadata.featurization),
        NORMALIZER_TYPE_KEY: model_metadata.normalizer_type,
        RANDOM_STATE_KEY: model_metadata.seed,
        PACKAGE_VERSION_KEY: get_version(),
    }
    save_dict_as_json(model_dir_path, MODEL_METADATA_FILENAME, model_metadata_dict)
    class_to_idx_dict = model_metadata.class_to_idx
    save_dict_as_json(model_dir_path, CLASS_NAME_TO_IDX_FILENAME, class_to_idx_dict)
    return model_dir_path


# Taken from: https://stackoverflow.com/questions/43265832/mapping-over-namedtuple-as-dictionary

def named_tuple_as_dict(obj):
    """Returns a dictionary version of a named tuple, 
        noteably nested named tuples are recursively converted into dictionaries
    """
    if isinstance(obj, dict):
        return {key: named_tuple_as_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [named_tuple_as_dict(value) for value in obj]
    elif is_named_tuple_instance(obj):  # see note
        return {key: named_tuple_as_dict(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, tuple):
        return tuple(named_tuple_as_dict(value) for value in obj)
    else:
        return obj

def is_named_tuple_instance(x: Any) -> bool:
    """Determines if x is a named tuple instance"""
    _type = type(x)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, '_fields', None)
    if not isinstance(fields, tuple):
        return False
    return all(type(i)==str for i in fields)
  
# Taken from URL Image Module
def determine_device(no_cuda: bool = False) -> torch.device:
  """Determines device based on CUDA availability on host and no_cuda parameter

  Args:
    no_cuda: boolean indicates if CUDA should not be used. Default is False.

  Returns:
    device: PyTorch device, i.e. cuda or cpu
    use_cuda: boolean indicating if CUDA should be used for task
  """
  use_cuda = not no_cuda and torch.cuda.is_available()
  device = torch.device('cuda' if use_cuda else 'cpu')
  return device, use_cuda