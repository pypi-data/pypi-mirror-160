import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier

from os.path import join
import os

from url_text_module.classes import AlgorithmMetadata, Featurization

from .constants import (
    ALGO_DICT,
    ALGORITHM_METADATA_FILENAME,
    BEST_FEATURIZATION_KEY,
    BEST_PARAMS_KEY,
    BEST_SCORE_KEY,
    BEST_STD_KEY,
    CROSS_VAL_DICT,
    CV_METADATA_FILENAME,
    CV_TYPE_KEY,
    DEFAULT_N_JOBS,
    DUMMY_CLASSIFIER_STRATEGIES,
    FEATURIZATION_COL_NAME,
    FINAL_RESULTS_FILENAME,
    HYPERPARAMETERS_AND_SETTINGS_DIR_NAME,
    INNER_CV_RESULTS_DIR_NAME,
    INNER_SPLITS_NUM_KEY,
    INTERMEDIATE_RESULTS_CSV_FILENAME,
    MEAN_OUTER_FOLDS_SCORE_KEY,
    MEAN_TEST_SCORE_COL_NAME,
    N_JOBS_KEY,
    NESTED_CV_METADATA_FILENAME,
    NESTED_CV_RESULTS_FILENAME,
    DOESNT_USE_RANDOM_STATE_SET,
    NUM_SPLITS_KEY,
    OPTIMIZE_METRIC_KEY,
    OUTER_CV_RESULTS_FILENAME,
    OUTER_SPLITS_NUM_KEY,
    PARAMETERS_COL_NAME,
    RANDOM_STATE_KEY,
    RANDOM_STATE_STR,
    RESULTS_DIR_NAME,
    SAVE_ALGO_METADATA_KEY,
    SAVE_CV_METADATA_KEY,
    SAVE_DIR_KEY,
    SCORE_STR,
    SHUFFLE_KEY,
    SPLIT_STR,
    SPLITS_FILENAME,
    STD_OUTER_FOLDS_SCORE_KEY,
    STD_TEST_SCORE_COL_NAME,
    STRATEGY_KEY,
    TEST_INDICES_KEY,
    TEST_SCORE_STR,
    TRAINING_INDICES_KEY,
    VECTORIZER_MAP,
    NORMALIZER_DICT,
    DEFAULT_SEED,
    get_metric_func_and_scorer,
)

from .misc_utils import (
    compute_splits_dict,
    extract_best_score_std_params,
    named_tuple_as_dict,
    save_dict_as_json,
    sort_featurization_grid
)

from typing import List, Dict, Union, Optional, Tuple

def get_dummy_classifier_preds_and_probs(
    dummy_classifier_options: Dict[str, Union[str, int]], 
    X_train: Union[List[str], np.ndarray], 
    y_train: np.ndarray, 
    X_test: Union[List[str], np.ndarray]
) -> Tuple[np.ndarray, np.ndarray]:
  """Returns the predictions and associated probabilites given by a dummy classifier baseline
        parameterized by the options in dummy_classifier_options

  Args:
    dummy_classifier_options:  Dictionary containing options which parameteriz the dummy classifier including
                                strategy for predicting (key: STRATEGY_KEY, must be one of the strategies in DUMMY_CLASSIFIER_STRATEGIES), 
                                random state (key: RANDOM_STATE_STR), and the constant class to predict in the case dummy_classifier_options[STRATEGY_KEY] == CONSTANT_STR
    X_train: List or array of training data to fit the dummy classifier with
    y_train: Integer labels corresponding to the data in X_train to fit the dummy classifier with
    X_test: Test data which will be predicted on by the dummy classifier

  Returns:
    preds: Array of predicted integer labels corresponding to the data in X_test
    pred_probas: Matrix of predicted probabilities where the rows correspond to the data points in
                    X_test and the columns correspond to the classes, e.g. where pred_probas[:, 0] corresponds
                    to the probability of the class 0
  """
  assert dummy_classifier_options[STRATEGY_KEY] in DUMMY_CLASSIFIER_STRATEGIES
  if RANDOM_STATE_STR not in dummy_classifier_options:
    dummy_model = DummyClassifier(**dummy_classifier_options, random_state = DEFAULT_SEED)
  else:
    dummy_model = DummyClassifier(**dummy_classifier_options)
  dummy_model.fit(X_train, y_train)
  preds, pred_probas = dummy_model.predict(X_test), dummy_model.predict_proba(X_test)
  return preds, pred_probas

def create_algo_metadata(
    algo_name: str,
    hyperparameter_grid: List[Dict[str, List[Union[str, float, int, bool, None]]]], 
    featurization_grid: List[Featurization], 
    normalizer_type: Optional[str] = None,
) -> AlgorithmMetadata:
    """Creates dictionary storing various pieces of metadata about an algorithm to be used for cross-validation
        namely the algorithm-specific hyperparameter grid, featurization_grid, and the type of normalizer to use, normalizer_type

    Args:
        algo_name: string name for the algorithm
        hyperparameter_grid: List representing the algorithm-specific hyperparameter grid
        featurization_grid: List of featurizations to use as inputs to the algorithm
        normalizer_type: Type of normalizer to apply to use on the algorithm's inputs. Must be a key in
                            NORMALIZER_DICT if it is not None
    
    Returns:
        algo_metadata: Metadata storing algorithm-specific hyperparameters & featurizations to use as inputs and the normalizer to use on the algorithm's
                        inputs
    """
    algo_metadata = AlgorithmMetadata(algo_name, hyperparameter_grid, featurization_grid, normalizer_type)
    return algo_metadata

def unpack_algorithm_metadata(
    algo_metadata: AlgorithmMetadata
) -> Tuple[str, List[Dict[str, List[Union[str, float, int, bool, None]]]], List[Featurization], str]:
    """Unpacks algorithm's metadata namely the algorithm-specific, the name of the algorithm, hyperparameter grid, 
        featurization grid, and the type of normalizer to use on the inputs to the algorithm

    Args:
        algo_metadata: Metadata storing algorithm-specific hyperparameters & featurizations to use as inputs and the normalizer to use on the algorithm's
                        inputs
    Returns:
        algo_name: string name for the algorithm
        hyperparameter_grid: List representing the algorithm-specific hyperparameter grid
        featurization_grid: List of featurizations to use as input to the algorithm
        normalizer_type: Type of normalizer to apply to use on the algorithm's inputs. Must be a key in
                            NORMALIZER_DICT if it is not None
    """
    algo_name, normalizer_type = algo_metadata.name, algo_metadata.normalizer_type
    hyperparameters_grid, featurizations_grid = algo_metadata.hyperparameters_grid, algo_metadata.featurization_grid
    return algo_name, hyperparameters_grid, featurizations_grid, normalizer_type

def create_multiple_algorithm_metadata_dict(
    algorithm_specific_hyperparameter_dict: Dict[str, List[Dict[str, List[Union[str, float, int, bool, None]]]]], 
    featurization_type_dict: Dict[str, List[Featurization]], 
    normalizer_type_dict: Dict[str, str]
) -> Dict[str, AlgorithmMetadata]:
    """Creates dictionary of algorithm metadata storing various pieces of metadata about each algorithm specified in
            algorithm_specific_hyperparameter_dict to be used for cross-validation namely the algorithm-specific hyperparameter grid, 
            featurization grid, and the type of normalizer to use on the featurized inputs to the algorithm

    Args:
        algorithm_specific_hyperparameter_dict: Dictionary mapping each algorithm name to a list representing the algorithm-specific hyperparameter grid
        featurization_type_dict: Dictionary mapping each algorithm name to a list of featurizations to use as input to the algorithm
        normalizer_type_dict: Dictionary mapping each algorithm name to the type of normalizer to apply to use on the algorithm's inputs. Must be a key in
                                NORMALIZER_DICT if it is not None
    
    Returns:
        all_algos_metadata: Dictionary mapping algorithm name to metadata which holds the algorithm-specific hyperparameters & featurizations to use as inputs 
                                and the normalizer to use on the algorithm's featurized inputs
    """
    assert set(algorithm_specific_hyperparameter_dict.keys()) == set(featurization_type_dict.keys())
    assert set(featurization_type_dict.keys()) == set(normalizer_type_dict.keys())
    algo_names = list(algorithm_specific_hyperparameter_dict.keys())
    all_algos_metadata = {}
    for algo in algo_names:
        algo_hyperparameter_grid, algo_featurization_grid = algorithm_specific_hyperparameter_dict[algo].copy(), featurization_type_dict[algo].copy()
        algo_normalizer_type = normalizer_type_dict[algo]
        algo_metadata = create_algo_metadata(
           algo, algo_hyperparameter_grid, algo_featurization_grid, algo_normalizer_type
        )
        all_algos_metadata[algo] = algo_metadata
    return all_algos_metadata

def build_pipe(
    algo_name: str, 
    featurization: Featurization, 
    normalizer_type: str = None, 
    seed: int = DEFAULT_SEED
) -> object:
    """Creates Pipeline for classification model using algorithm name, type of featurization to perform on the input to the algorithm,
            and the type of normalization to perform on the featurization 

    Args:
        algo_name: Name of the classification algorithm the pipeline is being built for
        featurization: Featurization to apply to input strings to the model
        normalizer_type: Type of normalizer to use on the data prior to being inputted to the model. If not None, must be key in NORMALIZER_DICT.
                            Default is None, i.e. no normalization is applied
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Default is DEFAULT_SEED

    Returns:
        pipe: scikit-learn Pipeline of the structure:
            (featurization_type, parameterized_vectorizer)* -> (normalizer_type, normalizer)* -> ('classifier', algorithm)
            
            * Not present in final pipeline if corresponding vectorizer or normalization_type is None
    """
    algo_obj = ALGO_DICT[algo_name]
    featurization_type, featurization_named_params_dict = featurization.type, featurization.named_parameters
    uses_random_state = algo_name not in DOESNT_USE_RANDOM_STATE_SET
    pipe_input = []
    if VECTORIZER_MAP[featurization_type] is not None:
        vectorizer = VECTORIZER_MAP[featurization_type]
        parameterized_vectorizer = vectorizer(**featurization_named_params_dict)
        pipe_input.append((featurization_type, parameterized_vectorizer))
    if normalizer_type is not None:
        normalizer = NORMALIZER_DICT[normalizer_type]()
        pipe_input.append((normalizer_type, normalizer))
    classifier = algo_obj(random_state = seed) if uses_random_state else algo_obj()
    pipe_input.append(('classifier', classifier))
    pipe = Pipeline(pipe_input)
    return pipe

class CrossValidationWithGridSearch:
    """Class enabling the cross validation procedure using grid search for
            different featurizations of the input data

    Args:
        cv_type: Type of cross validation procedure to perform. Must be a key   
                    in CROSS_VAL_DICT
        num_splits: Number of splits of the data into train/test, where 
                        each data point is a part of the test set exactly once
        optimize_metric: Metric used to determine best set of hyperparmeters + featurization set for the 
                            cross-validation procedure
        shuffle: Determines if data should be shuffled when creating the data splitting
        n_jobs: Number indicating the number of cores to utilize in parallel when performing the grid-search procedure
        seed: Default is DEFAULT_SEED. Seed used by stochatic algorithms for enabling reproducibility of the experiment. Default is DEFAULT_SEED
        
    Attributes:
        cv_type: Type of cross validation procedure to perform. Must be a key   
                    in CROSS_VAL_DICT
        num_splits: Number of splits of the data into train/test, where 
                        each data point is a part of the test set exactly once
        optimize_metric: Metric used to determine best set of hyperparmeters + featurization set for the 
                            cross-validation procedure
        shuffle: Determines if data should be shuffled when creating the data splitting
        n_jobs: Number indicating the number of cores to utilize in parallel when performing the grid-search procedure. Default is DEFAULT_N_JOBS
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Default is DEFAULT_SEED
    """
    def __init__(
        self,
        cv_type: str,
        num_splits: int,
        optimize_metric: str,
        shuffle: bool = True,
        n_jobs: int = DEFAULT_N_JOBS,
        seed: int = DEFAULT_SEED
    ):
        self.cv_type = cv_type
        self.num_splits = num_splits
        self.optimize_metric = optimize_metric
        self._metric_func, self._scorer = get_metric_func_and_scorer(self.optimize_metric)
        self.shuffle = shuffle
        self.n_jobs = n_jobs
        self.seed = seed
        self._cv = self._create_cv()
    
    def _create_cv(self):
        # Creates the Cross-Validation object determined by the self.cv_type attribute
        # and instantiates it with various hyperparameters
        cv = CROSS_VAL_DICT[self.cv_type](
            n_splits = self.num_splits,
            shuffle = self.shuffle,
            random_state = self.seed
        )
        return cv
    
    def get_cv(self):
        return self._cv
    
    def get_metadata_dict(self):
        """Returns a dictionary of various metadata about the Cross Validation procedure
            namely the values of its attributes
        
        Returns:
            cv_metadata_dict: Dictionary containing the names of various attributes of the
                                cross validation with grid search class and their associated values, i.e.
                                the metadata of the procedure, e.g. type of cross validation procedure, 
                                number of data splits, random state seed, etc. 
        """
        cv_metadata_dict = {
            CV_TYPE_KEY: self.cv_type,
            RANDOM_STATE_KEY: self.seed, 
            SHUFFLE_KEY: self.shuffle,
            N_JOBS_KEY: self.n_jobs,
            OPTIMIZE_METRIC_KEY: self.optimize_metric,
            NUM_SPLITS_KEY: self.num_splits,
        }
        return cv_metadata_dict

    def compute_split_col_name_list(self):
        """Computes the name of the columns which store the scores of each unique hyperparameter combination on the test set for each split i

        Returns:
            split_col_name_list: List of the column names for column which store the scores of hyperparameter combinations on the 
                                    test set for that split. Each column name for split i is of the structure '{SPLIT_STR}{i}_{TEST_SCORE_STR}'
        """
        split_col_name_list = [f'{SPLIT_STR}{i}_{TEST_SCORE_STR}' for i in range(self.num_splits)]
        return split_col_name_list

    def compute_intermediate_results_df_col_name(self):
        """Computes the full list of columns of the intermediate results DataFrame when performing the procedure including 
            columns for storing the algorithm-specific hyperparameters, featurizations used, scores of the hyperparameter combinations
            on each split and their average and standard deviation of scores across the test sets in each of the splits
        
        Returns:
            df_col_name_list: List of column names in the intermediate results DataFrame namely:
                [PARAMETERS_COL_NAME, FEATURIZATION_COL_NAME, {SPLIT_STR}{0}_{TEST_SCORE_STR}, ..., {SPLIT_STR}{n}_{TEST_SCORE_STR}, MEAN_TEST_SCORE_COL_NAME, STD_TEST_SCORE_COL_NAME]
        """
        df_col_name_list = [PARAMETERS_COL_NAME, FEATURIZATION_COL_NAME] + self.compute_split_col_name_list() + [MEAN_TEST_SCORE_COL_NAME, STD_TEST_SCORE_COL_NAME]
        return df_col_name_list
    
    def _construct_base_cv_df(self):
        # Computes the base structure of a data frame (i.e. empty with correct columns) of intermediate results of the grid search cross validation procedure
        # for each combination of hyperparameters on each of the folds in the data
        cv_df_col_names = self.compute_intermediate_results_df_col_name()
        cv_df = pd.DataFrame(columns = cv_df_col_names)
        return cv_df
    
    def _print_results(
        self, 
        best_score: float,
        best_std: float,
        best_params: Dict[str, List[Union[str, float, int, None]]], 
        best_featurization_type: str, 
        best_featurization_named_parameters: Union[Dict[str, Union[int, bool]], None]
    ) -> None:
        # Prints the results of the cross validation procedure including the best average score, standard deviation
        # the best algorithm-specific hyperparameters & the best featurization associated with the best average score
        print('\nGrid Search Results:\n')
        mean_string = f'(avg. of test folds) %.2f%%' % (best_score * 100)
        std_string = f'(std. of test folds) %.2f%%' % (best_std * 100)
        print(f'    Best {self.optimize_metric}: {mean_string} / {std_string}')
        print(f'    Best parameters: {best_params}')
        print(f'    Featurization_type: {best_featurization_type} / Named Parameters For Vectorizer: {best_featurization_named_parameters}\n')

    def _prepare_splits_dict(
        self, 
        X: Union[np.ndarray, List[str]], 
        y: np.ndarray
    ) -> Dict[int, Dict[str, List[int]]]:
        # Prepares a dictionary using splittings of the data and labels in X & y for performing
        # the CV procedure by mapping a unique split ID to a dictionary containing a list of the indices
        # corresponding to the train fold and the test fold for that split. Of the structure:
        # {
        #     0: {
        #             TRAINING_INDICES_KEY: [...],
        #             TEST_INDICES_KEY: [...]
        #         },
        #     ...,
        #     n: {
        #             TRAINING_INDICES_KEY: [...],
        #             TEST_INDICES_KEY: [...]
        #         },
        # }
        splits_dict = compute_splits_dict(self._cv, X, y)
        return splits_dict
    
    def _prepare_final_results_dict(
        self,
        best_score: float,
        best_std: float,
        best_params: Dict[str, Union[str, float, int, bool, None]],
        best_featurization: Featurization, 
    ) -> Dict[str, Union[float, str, Featurization, Dict[str, Union[str, float, int, bool, None]]]]:
        # Prepares a dictionary containing the final results of the procedure
        # including the metric used to optimize for finding the best average score, the best average score, the associated standard deviation of the performance
        # score across test folds, the best algorithm-specific hyperparameters, and the featurization associated with
        # best performance 
        final_results_dict = {}
        final_results_dict[BEST_SCORE_KEY], final_results_dict[BEST_STD_KEY], final_results_dict[BEST_PARAMS_KEY] = best_score, best_std, best_params
        final_results_dict[OPTIMIZE_METRIC_KEY] = self.optimize_metric
        final_results_dict[BEST_FEATURIZATION_KEY] = best_featurization
        return final_results_dict
        
    def create_algo_grid_search_dict(self, algo_metadata: AlgorithmMetadata) -> Dict[str, object]:
        """Creates a dictionary of grid search objects for a combination of algorithm, algorithm-specific hyperparameters, featurizations,
            normalization applied to the inputs to the algorithm which can perform grid search using cross-validation. 
            
        Note: A grid search object is created for each featurization used as a hyperparameter, so although the dictionary contains multiple
            grid search objects (one for each featurization), the dictionary itself, when applied, represents one grid search ACROSS featurizations
        
        Args:
            algo_metadata: Metadata storing algorithm-specific hyperparameters & featurizations to use as inputs and the normalizer to use on the algorithm's
                        inputs

        Returns:
            algo_grid_search_dict: Dictionary mapping featurization type (must be in FEATURIZATIONS_SET) to a grid search object loaded with 
                algorithm-specific hyperparameters and the necessary normalization pipeline for inputs to the algorithm
                when performing grid-search, where the input given to that grid-search object will correspond
                to its key, the featurization type. Of the form: 
                {
                    FEATURIZATION_TYPE_1: grid_search_obj_1,
                    ...,
                    FEATURIZATION_TYPE_n: grid_search_obj_n
                }
                which together represents one grid-search procedure, across featurizations
        """
        algo_grid_search_dict = {}
        algo_name, hyperparameter_grid, featurization_grid, normalizer_type = unpack_algorithm_metadata(algo_metadata)
        # We create a grid-search object for each featurization provided for the algorithm, i.e. treating featurization type as an additional hyperparameter
        for featurization in featurization_grid:
            featurization_type = featurization.type
            pipe = build_pipe(algo_name, featurization, normalizer_type, seed = self.seed)
            featurization_gridcv = GridSearchCV(
                estimator = pipe,
                param_grid = hyperparameter_grid,
                scoring = self._scorer,
                n_jobs = self.n_jobs,
                cv = self._cv,
                verbose = 0,
                refit = True
            )
            algo_grid_search_dict[featurization_type] = featurization_gridcv
        return algo_grid_search_dict
    
    def _save_grid_search_results(
        self, 
        save_options: Dict[str, Union[str, bool]], 
        algo_metadata: AlgorithmMetadata, 
        splits_dict: Dict[int, Dict[str, List[int]]],
        final_results_dict: Dict[str, Union[float, str, Featurization, Dict[str, Union[str, float, int, bool, None]]]], 
        cv_df: pd.DataFrame
    ) -> None:
        # Saves the results of the grid search cross-validation procedure, namely the indices of the input data used for the train and test folds in each split
        # and the intermediate results of each hyperparameter and featurization combination on each split and final results
        # and if specified in save_options, also the metadata associated with the cross-validation procedure, the metadata associated with the algorithm employed
        # for the cross validation
        save_dir, save_algo_metadata, save_cv_metadata = save_options[SAVE_DIR_KEY], save_options[SAVE_ALGO_METADATA_KEY], save_options[SAVE_CV_METADATA_KEY]
        os.mkdir(save_dir)
        save_dict_as_json(save_dir, SPLITS_FILENAME, splits_dict)
        final_results_dict[BEST_FEATURIZATION_KEY] = named_tuple_as_dict(final_results_dict[BEST_FEATURIZATION_KEY])
        save_dict_as_json(save_dir, FINAL_RESULTS_FILENAME, final_results_dict)
        cv_df.to_csv(join(save_dir, INTERMEDIATE_RESULTS_CSV_FILENAME), index = False)
        if save_algo_metadata:
            save_dict_as_json(save_dir, ALGORITHM_METADATA_FILENAME, named_tuple_as_dict(algo_metadata))
        if save_cv_metadata:
            cv_metadata_dict = self.get_metadata_dict()
            save_dict_as_json(save_dir, CV_METADATA_FILENAME, cv_metadata_dict)

    def _run_grid_search_for_featurization(
        self, 
        grid_search_obj: object, 
        featurization: Featurization, 
        X: Union[np.ndarray, List[str]], 
        y: np.ndarray
    ) -> Tuple[object, Featurization, pd.DataFrame]:
        # Runs grid search for using the featurization described in featurization_tuple and represented in 
        # the data matrix X along with corresponding labels in y
        # Returns the fitted grid search object, the featurization_tuple, and the intermediate results found
        # during the grid search in gs_data_df
        df_data = {}
        grid_search_obj.fit(X, y)
        gs_results = grid_search_obj.cv_results_
        gs_param_set_array = gs_results[PARAMETERS_COL_NAME]
        # corresponds to each unique combination of  hyperparameters
        df_data[PARAMETERS_COL_NAME] = gs_param_set_array
        num_hyperparameter_sets = len(gs_param_set_array)
        featurization_array = np.array([named_tuple_as_dict(featurization) for _ in range(num_hyperparameter_sets)])
        # Since this method needs to be run for each featurization, we can use the same value for 
        # featurization type & named parameters for all unique hyperparameter combinations
        df_data[FEATURIZATION_COL_NAME] = featurization_array
        split_col_name_list = self.compute_split_col_name_list()
        for split_col_name in split_col_name_list:
            # We have access to the results of the hyperparameter combination performance on each test split
            # so we save this as a column for each test split
            gs_split_i_results_array = gs_results[split_col_name]
            df_data[split_col_name] = gs_split_i_results_array
        df_data[MEAN_TEST_SCORE_COL_NAME], df_data[STD_TEST_SCORE_COL_NAME] = gs_results[MEAN_TEST_SCORE_COL_NAME], gs_results[STD_TEST_SCORE_COL_NAME]
        # creates a DataFrame which stores all scores of each hyperparameter combination including the provided featurization on each test split and
        # the mean and standard deviation of those scores
        gs_data_df = pd.DataFrame(df_data)
        df_col_name_list = self.compute_intermediate_results_df_col_name() 
        # Puts the intermediate results columns in a specific order, e.g. hyperparameters, featurizations, split performances, and mean & standard deviation scores
        gs_data_df = gs_data_df[df_col_name_list].copy()
        return grid_search_obj, featurization, gs_data_df
        
    def run_grid_search(
        self, 
        algo_metadata: AlgorithmMetadata, 
        featurization_data_map: Dict[str, Union[np.ndarray, List[str]]], 
        y: np.ndarray, 
        save_options: Optional[Dict[str, Union[str, bool]]] = None, 
        verbose: bool = False
    ) -> Tuple[
        object,
        Featurization,
        Dict[int, Dict[str, List[int]]],
        Dict[str, Union[float, str, Featurization, Dict[str, Union[str, float, int, bool, None]]]],
        pd.DataFrame
    ]:
        """Performs grid search for a set of algorithm-specific hyperparameters and featurizations, returning the 
            model (as a fitted grid search object) with the optimal hyperparameter combination and featurization which gave the best performance across the 
            cross validation procedure. If desired, the cross validation procedure's metadata, the algorithm's metadata, the 
            indices associated with each train/test fold in each split, the final results of the procedure, and the intermediate 
            results on the splits can be saved in the save_options[SAVE_DIR_KEY] directory on the host's filesystem
        
        Args:
            algo_metadata: Metadata storing algorithm-specific hyperparameters & featurizations to use as inputs and the normalizer to use on the algorithm's
                        inputs
            featurization_data_map: Dictionary mapping featurization type to the corresponding version of the input data that aligns
                                        with that featurization type
            y: Integer labels array associated with the data in featurization_data_map
            save_options: Dictionary containing options for saving data on the host's filesystem, of the structure:
                        {
                            SAVE_DIR_KEY: '<path-to-dir-on-host>',
                            SAVE_ALGO_METADATA_KEY: True,
                            SAVE_CV_METADATA_KEY: True
                        }
            
                        The value of SAVE_DIR_KEY is the path to a directory on the host's filesystem which will be created to store the CV's metadata (saved as: CV_METADATA_FILENAME if SAVE_CV_METADATA_KEY value is True), 
                        the algorithm's metadata (saved as: ALGORITHM_METADATA_FILENAME if SAVE_ALGO_METADATA_KEY value is True), 
                        the splitting indices of the input data corresponding to the train and test folds of each of the splits (saved as: SPLITS_FILENAME), the final results (saved as: FINAL_RESULTS_FILENAME), and finally the
                        intermediate results on each of the split's for each of the unique hyperparameter and featurization combinations 
                        (saved as: INTERMEDIATE_RESULTS_CSV_FILENAME). Default is None, in which nothing is saved
            verbose: Boolean indicates if final results of the grid search including the should be printed. Default is False

        Returns:
            best_fitted_grid_search_obj: Fitted grid search object corresponding to the hyperparameter and featurization combination which gave 
                                            the highest average score across test folds. Can be used for inferencing and is fitted to the entire data set on which
                                            the cross-validation grid search procedure was performed
            best_featurization: Featurization which gave the best mean score across test folds
            splits_dict: Dictionary mapping each of the splits of the original data to a dictionary containing
                            the indices in the original data which are part of the training and test folds for each split of the following structure:
                            {
                                0: {
                                        TRAINING_INDICES_KEY: [...],
                                        TEST_INDICES_KEY: [...]
                                    },
                                ...,
                            }
            final_results_dict: Dictionary of final results from the grid search cross validation procedure of the following structure:
                             {
                                BEST_SCORE_KEY: best_mean_score
                                BEST_STD_KEY: best_std,
                                BEST_PARAM_KEY: {...},
                                BEST_FEATURIZATION_KEY: <featurization>
                                OPTIMIZE_METRIC_KEY: 'name-of-metric-being-optimized'
                            }
            cv_df: DataFrame containing the intermediate results of the grid-search cross validation procedure, including the scores of each unique hyperparameter + featurization combination
                    on each of the test folds as well as the mean score and standard deviation of the score across the test folds. Has columns names including:
                    [PARAMETERS_COL_NAME, FEATURIZATION_COL_NAME, {SPLIT_STR}{0}_{TEST_SCORE_STR}, ..., {SPLIT_STR}{n}_{TEST_SCORE_STR}, MEAN_TEST_SCORE_COL_NAME, STD_TEST_SCORE_COL_NAME]
        """
        cv_df = self._construct_base_cv_df()
        algo_name, hyperparameter_grid, featurization_grid, normalizer_type = unpack_algorithm_metadata(algo_metadata)
        sorted_featurization_grid = sort_featurization_grid(featurization_grid)
        featurization_best_performance_scores = []
        algo_grid_search_dict = self.create_algo_grid_search_dict(algo_metadata)
        print('\n')
        # perform grid_search
        for featurization in sorted_featurization_grid:
            # Perform grid search for each featurization
            featurization_type, featurization_named_params_dict = featurization.type, featurization.named_parameters
            print(f"Performing Grid Search with {featurization_type} featurization with Named Parameters {featurization_named_params_dict}...")
            data = featurization_data_map[featurization_type]
            fitted_grid_search_obj, featurization, cv_feat_df = self._run_grid_search_for_featurization(
                algo_grid_search_dict[featurization_type], featurization, data, y
            )
            algo_grid_search_dict[featurization_type] = fitted_grid_search_obj
            cv_df = pd.concat([cv_df, cv_feat_df]) # Vertically grow the dataframe by appending the df associated with each featurization hyperparameter
            best_score_featurization = algo_grid_search_dict[featurization_type].best_score_
            featurization_best_performance_scores.append(best_score_featurization)

        # Determine best hyperparameters + featurization tuple and associated scoring
        print(f'\nBest Mean Test {self.optimize_metric} Score for each featurization:\n')
        for featurization, featurization_best_score  in zip(sorted_featurization_grid, featurization_best_performance_scores):
            featurization_type, featurization_named_params_dict = featurization.type, featurization.named_parameters
            print(f'Featurization_type: {featurization_type} / Named Parameters For Vectorizer: {featurization_named_params_dict}')
            print(f'Score: {featurization_best_score}')
        max_avg_val_score = max(featurization_best_performance_scores)
        max_avg_val_score_idx = featurization_best_performance_scores.index(max_avg_val_score)
        best_featurization = sorted_featurization_grid[max_avg_val_score_idx]
        best_featurization_type, best_featurization_named_parameters = best_featurization.type, best_featurization.named_parameters
        best_fitted_grid_search_obj = algo_grid_search_dict[best_featurization_type]
        best_score, best_std, best_params = extract_best_score_std_params(best_fitted_grid_search_obj)
        placeholder_X = list(featurization_data_map.values())[0]
        splits_dict = self._prepare_splits_dict(placeholder_X, y)
        final_results_dict = self._prepare_final_results_dict(best_score, best_std, best_params, best_featurization)
        if verbose:
            self._print_results(best_score, best_std, best_params, best_featurization_type, best_featurization_named_parameters)
        if save_options:
            self._save_grid_search_results(save_options, algo_metadata, splits_dict, final_results_dict, cv_df)
        return best_fitted_grid_search_obj, best_featurization, splits_dict, final_results_dict, cv_df

class NestedCVWithGridSearch:
    """Class used for performing the Nested Cross Validation (Nested CV) procedure using grid search for different algorithm + hyperparameter grids
            different featurizations of the input data to enable algorithm (+ hyperparameter grid) selection

    Args:
        cv_type: Type of cross validation procedure to perform for both the inner and outer cv procedures. Must be a key in CROSS_VAL_DICT
        outer_splits_num: Number of splits of the data into train/test folds, where each data point is a part of the test set exactly once for the OUTER cv procedure
        inner_splits_num: Number of splits of the data into train/test folds, where each data point is a part of the test set exactly once for the INNER cv procedure
        optimize_metric: Metric used to determine best set of hyperparmeters + featurization set for the Nested CV procedure
        shuffle: Determines if data should be shuffled when creating the data splitting in both the inner and outer cross validation procedures. Default is True.
        n_jobs: Number indicating the number of cores to utilize in parallel when performing the grid-search procedure. Default is DEFAULT_N_JOBS
        seed: Default is DEFAULT_SEED. Seed used by stochatic algorithms and data shuffling for enabling reproducibility of the experiment. Default is DEFAULT_SEED
        
    Attributes:
        cv_type: Type of cross validation procedure to perform for both the inner and outer cv procedures. Must be a key in CROSS_VAL_DICT
        outer_splits_num: Number of splits of the data into train/test folds, where each data point is a part of the test set exactly once for the OUTER cv procedure
        inner_splits_num: Number of splits of the data into train/test folds, where each data point is a part of the test set exactly once for the INNER cv procedure
        optimize_metric: Metric used to determine best set of hyperparmeters + featurization set for the Nested CV procedure
        shuffle: Determines if data should be shuffled when creating the data splitting in both the inner and outer cross validation procedures. Default is True.
        n_jobs: Number indicating the number of cores to utilize in parallel when performing the grid-search procedure. Default is DEFAULT_N_JOBS
        seed: Default is DEFAULT_SEED. Seed used by stochatic algorithms and data shuffling for enabling reproducibility of the experiment. Default is DEFAULT_SEED
    """
    def __init__(
        self,
        cv_type: str,
        outer_splits_num: int, 
        inner_splits_num: int, 
        optimize_metric: str, 
        shuffle: bool = True, 
        n_jobs: Optional[int] = DEFAULT_N_JOBS, 
        seed: int = DEFAULT_SEED
    ) -> None:
        self.cv_type = cv_type
        self.outer_splits_num = outer_splits_num
        self.inner_splits_num = inner_splits_num
        self.optimize_metric = optimize_metric
        self._metric_func, self._scorer = get_metric_func_and_scorer(self.optimize_metric)
        self.shuffle = shuffle
        self.n_jobs = n_jobs
        self.seed = seed
        self._inner_cv, self._outer_cv = self._create_cv_objects()
    
    def get_inner_cv(self) -> CrossValidationWithGridSearch:
        """Returns the cross validation object for the inner cross validation procedure

        Returns:
            inner_cv: Cross validation object associated with inner cv capable of performing grid search using a specified algorithm, hyperparameter grid, and featurization
                        grid
        """
        return self._inner_cv
    
    def get_outer_cv(self) -> object:
        """Returns the cross validation object for the inner cross validation procedure

        Returns:
            outer_cv: Cross validation object associated with outer cv capable which can split input data into train/test folds for each split such that each data point is in the test fold 
                        exactly once
        """
        return self._outer_cv

    def _create_cv_objects(self) -> Tuple[CrossValidationWithGridSearch, object]:
        # Creates the appropriate cross validation objects for carrying out the inner cv (CrossValidationWithGridSearch)
        # and the outer cv (sklearn's cross validation object) using the metadata provided to the instantiated NestedCVWithGridSearch 
        inner_cv = CrossValidationWithGridSearch(
            self.cv_type,
            self.inner_splits_num,
            self.optimize_metric,
            shuffle = self.shuffle,
            n_jobs = self.n_jobs,
            seed = self.seed
        )
        outer_cv = CROSS_VAL_DICT[self.cv_type](
            n_splits = self.outer_splits_num,
            shuffle = self.shuffle,
            random_state = self.seed
        )
        return inner_cv, outer_cv
    
    def get_metadata_dict(self) -> Dict[str, Union[str, int, bool]]:
        """Returns the dictionary of metadata for the Nested CV procedure

        Returns:
            nested_cv_metadata_dict: Dictionary containing various pieces of metadata for the Nested CV procedure including
                                        the type of cross validation used for both the inner and outer cv's (e.g. StratifiedKFold CV) (key: CV_TYPE_KEY),
                                        the random state (i.e. seed) (key: RANDOM_STATE_KEY) to use for stochastic algorithms and data splitting,
                                        a boolean indicating whether or not to shuffle the data when splitting during cross validation (key: SHUFFLE_KEY),
                                        the number of cores to use to run parallel jobs to speed up grid search procedure (key: N_JOBS_KEY),
                                        the metric being to when finding the best set of hyperparameters + featurization in grid search (key: OPTIMIZE_METRIC_KEY),
                                        and the number of splits to use in the inner cv (key: INNER_SPLITS_NUM_KEY) and outer cv respectively (key: OUTER_SPLITS_NUM_KEY)
        """
        nested_cv_metadata_dict = {
            CV_TYPE_KEY: self.cv_type,
            RANDOM_STATE_KEY: self.seed, 
            SHUFFLE_KEY: self.shuffle,
            N_JOBS_KEY: self.n_jobs,
            OPTIMIZE_METRIC_KEY: self.optimize_metric,
            OUTER_SPLITS_NUM_KEY: self.outer_splits_num,
            INNER_SPLITS_NUM_KEY: self.inner_splits_num,
        }
        return nested_cv_metadata_dict
    
    def _save_outer_cv_results(
        self, 
        save_options: Dict[str, Union[str, bool]],
        algo_metadata: AlgorithmMetadata,
        outer_cv_performance_dict: Dict[str, float],
    ) -> None:
        # Saves the performance of an algorithm + hyperparater grid on the outer test folds of the outer cv in the nested CV procedure as the .json file named OUTER_CV_RESULTS_FILENAME
        # in the directory on the host's filesystem which is specified in save_options[SAVE_DIR_KEY]
        # Additionally, the algorithm's metadata dict algo_metadata_dict can also be saved under the ALGORITHM_METADATA_FILENAME (if the save_options[SAVE_ALGO_METADATA_KEY] is True)
        # in the save_options dictionary in the save_options[SAVE_DIR_KEY] directory. Lastly, the metadata associated with the nested cv cross validation procedure can be saved under the  
        # NESTED_CV_METADATA_FILENAME if (save_options[SAVE_CV_METADATA_KEY] is True)in the save_options[SAVE_DIR_KEY] directory.
        save_dir, save_algo_metadata, save_cv_metadata = save_options[SAVE_DIR_KEY], save_options[SAVE_ALGO_METADATA_KEY], save_options[SAVE_CV_METADATA_KEY]
        save_dict_as_json(save_dir, OUTER_CV_RESULTS_FILENAME, outer_cv_performance_dict)
        if save_algo_metadata:
            save_dict_as_json(save_dir, ALGORITHM_METADATA_FILENAME, named_tuple_as_dict(algo_metadata))
        if save_cv_metadata:
            cv_metadata_dict = self.get_metadata_dict()
            save_dict_as_json(save_dir, NESTED_CV_METADATA_FILENAME, cv_metadata_dict)

    def _prepare_nested_cv_folder_structure(
        self, 
        save_dir: Union[str, None], 
        all_algos_metadata: Dict[str, AlgorithmMetadata]
    ) -> Union[str, None]:
        # Prepares the directory structure for a nested CV procedure involving multiple algorithms and hyperparameter grid combinations.
        # If save_dir is a string, creates a new directory on the host's filesystem at the save_dir location, in which the metadata associated with
        # the nested CV procedure is saved in the save_dir directory (filename: NESTED_CV_METADATA_FILENAME). A directory in save_dir is created to save results
        # (directory name: RESULTS_DIR_NAME). Lastly, a directory for storing hyperparameters and settings used for each algorithm in the nested CV procedure 
        # is created inside save_dir (directory name: HYPERPARAMETERS_AND_SETTINGS_DIR_NAME), in which 
        # a json containing the hyperparameter grid, featurization grid, and settings used for that algorithm is saved (filename: ALGORITHM_METADATA_FILENAME) 
        if save_dir:
            os.mkdir(save_dir)
            # Save metadata of Nested CV used for experiment
            nested_cv_metadata_dict = self.get_metadata_dict()
            save_dict_as_json(save_dir, NESTED_CV_METADATA_FILENAME, nested_cv_metadata_dict)
            results_path = join(save_dir, RESULTS_DIR_NAME)
            hyperparameters_settings_path = join(save_dir, HYPERPARAMETERS_AND_SETTINGS_DIR_NAME)
            os.mkdir(results_path)
            os.mkdir(hyperparameters_settings_path)
            # Save hyperparameters of experiment
            all_algos_metadata = {algo_name: named_tuple_as_dict(algo_metadata) for algo_name, algo_metadata in all_algos_metadata.items()}
            save_dict_as_json(hyperparameters_settings_path, ALGORITHM_METADATA_FILENAME, all_algos_metadata)
        else:
            results_path = None
        return results_path
    
    def _perform_inner_cv(
        self,
        algo_metadata: AlgorithmMetadata, 
        featurization_data_map: Dict[str, Union[np.ndarray, List[str]]], 
        y: np.ndarray, 
        save_options: Union[Dict[str, Union[str, bool]], None], 
        verbose: Union[str, None]
    ) -> Tuple[
            object,
            Featurization,
            Dict[int, Dict[str, List[int]]],
            Dict[str, Union[float, str, Featurization, None, Dict[str, Union[str, float, int, bool, None]]]],
            pd.DataFrame
    ]:
        # Performs inner CV of Nested CV, i.e. runs grid search on the train fold of the current split of outer cv, returning the
        # best (by mean score on the test folds of the inner cv) grid search object refitted on the entire training fold of the outer cv,
        # best featurization tuple (featurization_type, featurization_named_params_dict) found from the grid-search,
        # the indices of the outer fold training fold data found for the train/test folds of each split in the inner cv,
        # the final results found on each test fold of the inner cv along with the associated best parameters,
        # and finally the intermediate results (as .csv) found for each hyperparameter + featurization combination on each test fold in the inner cv (grid search)
        best_fitted_grid_search_obj, best_featurization, splits_dict_inner_cv, final_results_dict_inner_cv, inner_cv_df = self._inner_cv.run_grid_search(
            algo_metadata, 
            featurization_data_map, 
            y,
            save_options = save_options, 
            verbose = verbose
        )
        return best_fitted_grid_search_obj, best_featurization, splits_dict_inner_cv, final_results_dict_inner_cv, inner_cv_df
        
    def _perform_outer_cv(
        self,
        algo_metadata: AlgorithmMetadata, 
        featurization_data_map: Dict[str, Union[np.ndarray, List[str]]], 
        y: np.ndarray, 
        save_options: Union[Dict[str, Union[str, bool]], None],
        verbose: Union[str, None]
    ) -> Tuple[Dict[str, float], Dict[int, Dict[str, Union[float, List[int]]]]]:
        # Performs outer CV of Nested CV, passing the training fold for a split to the inner CV procedure for grid search, and refits the algorithm with the best hyperparameters + featurization found
        # from grid-search (inner CV) refitted on the entire training fold and predicts and computes a score on the test fold returning the performance of an algorithm + hyperparameter grid on the test 
        # fold in each split of the outer CV along with the mean and standard deviation of the scores. Also returns the indices of the input data which form the training/test folds in each split of the outer
        # CV. If save_options is not None, creates a directory at the location specified at save_options[SAVE_DIR_KEY] to save the results of the nested CV procedure. To prevent redundant data from being saved, if save_options is not None,
        # creates a directory for each outer cv split, saving the results of the Inner CV on the training fold of that split along with the indices of the original data which form 
        # the train and test folds for that split, also saves the metadata (i.e. hyperparameter + featurization grid and settings, if save_options[SAVE_ALGO_METADATA_KEY] is True) in the save_dir,
        # lastly, saves the metadata of the nested CV procedure (if save_options[SAVE_CV_METADATA_KEY] is True) in save_options[SAVE_DIR_KEY]
        algo_name = algo_metadata.name
        if verbose:
            print(50 * '-', '\n')
            print('Algorithm: ', algo_name)

        outer_cv_splits_dict, outer_cv_performance_dict = {}, {}
        placeholder_X = list(featurization_data_map.values())[0]

        if save_options is None:
            save_dir = None
        else:
            save_dir = save_options[SAVE_DIR_KEY]
            os.mkdir(save_dir)

        # To create train/test folds of the outer cv
        for idx, (train_indices, test_indices) in enumerate(self._outer_cv.split(placeholder_X, y)):
            if verbose:
                print(f'\nOuter Split {idx}:')
                print(f'    Inner Loop (Grid Search):')
            subsetted_y = y[train_indices]
            subsetted_featurization_data_map = {
                featurization_type: data[train_indices] for featurization_type, data in featurization_data_map.items()
            }

            if save_dir is None:
                inner_cv_save_options = save_options
                outer_fold_i_dir = None
            else:
                outer_fold_i_dir = join(save_dir, f'outer_fold_{idx}')
                os.mkdir(outer_fold_i_dir)
                inner_cv_save_options = {
                    SAVE_DIR_KEY: join(outer_fold_i_dir, INNER_CV_RESULTS_DIR_NAME),
                    SAVE_ALGO_METADATA_KEY: False,
                    SAVE_CV_METADATA_KEY: False,
                }
            # Find best hyperparameter combination + featurization for algo using inner cv
            best_fitted_grid_search_obj, best_featurization, _, _, _ = self._perform_inner_cv(
                algo_metadata, 
                subsetted_featurization_data_map, 
                subsetted_y, 
                save_options = inner_cv_save_options, 
                verbose = verbose
            )
            best_featurization_type = best_featurization.type

            # predict and compute performance on test fold (test_indices)
            test_data = featurization_data_map[best_featurization_type][test_indices]
            test_preds, test_true = best_fitted_grid_search_obj.predict(test_data), y[test_indices]
            test_score = self._metric_func(y_pred = test_preds, y_true = test_true)
            
            # To save the indices in the dataset and the associated score of the best model (found from the inner cv) 
            # associated with each of the folds
            outer_loop_i_dict = {
                TRAINING_INDICES_KEY: train_indices.tolist(),
                TEST_INDICES_KEY: test_indices.tolist(),
                SCORE_STR: test_score
            }
            if outer_fold_i_dir:
                outer_loop_i_json_filename = f'outer_fold_{idx}_splits.json'
                save_dict_as_json(outer_fold_i_dir, outer_loop_i_json_filename, outer_loop_i_dict)
            outer_cv_splits_dict[idx] = outer_loop_i_dict

            split_score_key = f'{SPLIT_STR}_{idx}'
            outer_cv_performance_dict[split_score_key] = test_score
            print(f'\nOuter Split {idx} Test Fold Performance:')
            print(f'    {self.optimize_metric}: %.2f%%' % (test_score * 100))
        
        outer_cv_scores = list(outer_cv_performance_dict.values())
        outer_cv_mean_performance, outer_cv_performance_std = np.mean(outer_cv_scores), np.std(outer_cv_scores)
        outer_cv_performance_dict[MEAN_OUTER_FOLDS_SCORE_KEY] = outer_cv_mean_performance
        outer_cv_performance_dict[STD_OUTER_FOLDS_SCORE_KEY] = outer_cv_performance_std
        
        if verbose:
            print('\nOuter Loop:')
            print(f'    {self.optimize_metric} %.2f%% +/- %.2f' % (outer_cv_mean_performance * 100, outer_cv_performance_std * 100))
        
        if save_options:
            self._save_outer_cv_results(save_options, algo_metadata, outer_cv_performance_dict)
        return outer_cv_performance_dict, outer_cv_splits_dict

    def perform_nested_cv_for_algo(
        self,
        algo_metadata: AlgorithmMetadata,
        featurization_data_map: Dict[str, Union[np.ndarray, List[str]]],
        y: np.ndarray,  
        save_options: Optional[Dict[str, Union[str, bool]]] = None,
        verbose: bool = False
    ) -> Tuple[Dict[str, float], Dict[int, Dict[str, Union[float, List[int]]]]]:  
        """Performs Nested Cross Validation with a given algorithm which has an associated hyperparameter + featurization grid

        Args:
            algo_metadata: Metadata storing algorithm-specific hyperparameters & featurizations to use as inputs and the normalizer to use on the algorithm's
                        inputs
            featurization_data_map: Dictionary mapping featurization type to the corresponding version of the input data that aligns with that featurization type
            y: Integer labels array associated with the data in featurization_data_map
            save_options: Dictionary storing various options for saving the results of the nested CV procedure, including the path on the host's filesystem to the directory that will be created containing the results
                            and whether or not to save various metadata about the algorithm and the hyperparameter + featurization grid or the metadata dictionary for the nested cv procedure. 
                            Default is None, in which nothing is saved. If provided, of the structure:
                    {
                        SAVE_DIR_KEY: <path-to-directory>, # String path to directory on host's filesystem which will be created containing the results of the nested CV procedure,
                        SAVE_ALGO_METADATA_KEY: <bool-indicating-whether-to-save-algo-metadata>, # Boolean indicating whether or not to save algo_metadata_dict as a json
                        SAVE_CV_METADATA_KEY: <bool-indicating-whether-to-save-nested-cv-metadata>, # Boolean indicating whether or not to save the result of self.get_metadata_dict() as a json
                    }
            verbose: Bool indicating if intermediate results of the nested CV procedure should be printed (i.e. results of grid search (inner cv) as well as results on the outer CV).
                        Default is False

        Note:
            If save_options is not None, the resulting folder structure of the results is save follows:

            save_options[SAVE_DIR_KEY]              # path to directory that is created on the host's filesystem to store results
            ├── ALGORITHM_METADATA_FILENAME         # JSON containing algorithm-specific hyperparameters, featurizations, name of the algorithm, 
            │                                       # and the type of normalizer to apply to the input. Saved if save_options[SAVE_ALGO_METADATA_KEY] is True
            │
            ├── NESTED_CV_METADATA_FILENAME         # JSON containing metadata associated with nested CV procedure. Saved if save_options[SAVE_CV_METADATA_KEY] is True
            │
            ├── OUTER_CV_RESULTS_FILENAME           # JSON containing the scores on each split of the outer CV of the best hyperparameter + featurization combo found from the inner CV with the model refitted on the entire
            │                                       # training fold and tested on the test fold of the outer cv split. Also includes the mean (key: MEAN_OUTER_FOLDS_SCORE_KEY) and 
            │                                       # standard deviation (key: STD_OUTER_FOLDS_SCORE_KEY) of the score on the outer cv test folds
            │
            ├── outer_fold_0
            │   ├── outer_fold_0_splits.json        # JSON containing the indices of the original data in featurization_data_map which compose the train/test folds of split 0 
            │   │                                   # (Key: TRAINING_INDICES_KEY) & (Key: TEST_INDICES_KEY), respectively, as well as the score of refitted model on the test fold (Key: SCORE_STR)
            │   └── INNER_CV_RESULTS_DIR_NAME
            │       │
            │       ├── SPLITS_FILENAME             # JSON mapping each split index to a JSON containing the indices of the training data from the outer cv which composes the train/test folds of each split
            │       │                               # of the inner cv, these indices can be accessed using (Key: TRAINING_INDICES_KEY) & (Key: TEST_INDICES_KEY), respectively
            │       ├── INTERMEDIATE_RESULTS_CSV_FILENAME # .csv file storing the score of each unique hyperparameter + featurization combination on each test fold of the inner cv as well as the mean score and standard deviation
            │       └── FINAL_RESULTS_FILENAME      # JSON which stores various results including the name of the metric which was optimized in the nested CV (key: OPTIMIZE_METRIC_KEY),  best mean score (Key: BEST_SCORE_KEY), standard deviation (Key: BEST_STD_KEY) of 
            │                                       # the hyperparameter and featurization combination which gave the highest mean score on the test folds of the inner cv along with the corresponding
            │                                       # best algorithm-specific hyperparamers (key: BEST_PARAMS_KEY), best featurization (key: BEST_FEATURIZATION_KEY)
            └── ... # from outer_fold_0 to outer_fold_n         

        Returns:
            outer_cv_performance_dict: Dictionary mapping each split of the outer CV to the score on the test fold by the algorithm and the corresponding hyperparameter + featurization grid. Also
                                            includes the mean score and standard deviation across test folds. It has the structure:
                {
                    "split_0": <score-on-test-fold-of-split-0>,
                    ...,
                    "split_n": <score-on-test-fold-of-split-n>,
                    MEAN_OUTER_FOLDS_SCORE_KEY: <mean-score-across-splits>,
                    STD_OUTER_FOLDS_SCORE_KEY: <standard-deviation-of-score-across-splits>
                }
            outer_cv_splits_dict: Nested dictionary which stores the indices of the original data (in featurization_data_map) corresponding to the train/test folds of each split of the outer CV along with
                                    the score by the algorithm, hyperparameter + featurization grid on the test fold for that split. Of the structure:
                {
                    0: {
                        TRAINING_INDICES_KEY: <training-indices-list>, # List of indices corresponding to the stored data in featurization_data_map, which are used as training data in the train
                                                                        # fold for split 0
                        TEST_INDICES_KEY: <test-indices-list>,         # List of indices corresponding to the stored data in featurization_data_map, which are used as test data in the test
                                                                        # fold for split 0
                        SCORE_STR: <score-of-algo-hyperparameter-grid-on-test-fold> # Score by the algorithm fitted on the entirety of the data which correspond to <training-indices-list> using the
                                                                                    # the parameters which yielded the highest average score by the inner cv procedure
                    },
                    ...,
                }

        """
        outer_cv_performance_dict, outer_cv_splits_dict = self._perform_outer_cv(
            algo_metadata, 
            featurization_data_map, 
            y, 
            save_options = save_options, 
            verbose = verbose
        )
        return outer_cv_performance_dict, outer_cv_splits_dict

    def perform_nested_cv_for_multiple_algos(
        self, 
        all_algos_metadata: Dict[str, AlgorithmMetadata], 
        featurization_data_map: Dict[str, Union[np.ndarray, List[str]]],
        y: np.ndarray, 
        save_dir: Optional[str] = None, 
        verbose: bool = False,
    ) -> Dict[str, Dict[str, float]]:
        """Performs Nested CV for multiple algorithms (each with an associated hyperparameter and featurization grid). If desired, saves the results on the 
            host's filesystem in the created directory located at save_dir
        
        Args:
            all_algos_metadata: Dictionary mapping algorithm name to metadata which holds the algorithm-specific hyperparameters & featurizations to use as inputs 
                                    and the normalizer to use on the algorithm's featurized inputs
            featurization_data_map: Dictionary mapping featurization type to the corresponding version of the input data that aligns with that featurization type
            y: Integer labels array associated with the data in featurization_data_map
            save_dir: Path to directory on host's filesystem which will be created where results, hyperparameters, and metadata for the nested cv procedure are saved. Default is None, in which
                        nothing is saved
            verbose: Bool indicating if intermediate results of the nested CV procedure should be printed (i.e. results of grid search (inner cv) as well as results on the outer CV)
                        for each algorithm. Default is False
        
        Note:

            If save_dir is not None, the resulting folder structure of the results is save follows:

            save_dir                                # path to directory that is created on the host's filesystem to store results
            ├── NESTED_CV_METADATA_FILENAME         # JSON containing metadata associated with nested CV procedure
            │
            ├── NESTED_CV_RESULTS_FILENAME          # Nested JSON mapping each algorithm's name to a JSON containing the scores on each split of the outer CV of the best hyperparameter + featurization combo 
            │                                       # found from the inner CV with the model refitted on the entire training fold of the outer cv split and tested on the test fold,
            │                                       # Also includes the mean (key: MEAN_OUTER_FOLDS_SCORE_KEY) and standard deviation (key: STD_OUTER_FOLDS_SCORE_KEY) of the score on the outer cv test folds 
            ├── HYPERPARAMETERS_AND_SETTINGS_DIR_NAME
            │   └── ALGORITHM_METADATA_FILENAME      # Nested JSON mapping each algorithm's name to a JSON containing algorithm-specific hyperparameters, featurizations, name of the algorithm, 
            │                                        # and the type of normalizer to apply to the input
            │
            └── Results
               ├── <name-of-algo-1>
               │     ├── OUTER_CV_RESULTS_FILENAME           # JSON containing the scores on each split of the outer CV of the best hyperparameter + featurization combo found from the inner CV with the model refitted on the entire
               │     │                                       # training fold and tested on the test fold of the outer cv split. Also includes the mean (key: MEAN_OUTER_FOLDS_SCORE_KEY) and 
               │     │                                       # standard deviation (key: STD_OUTER_FOLDS_SCORE_KEY) of the score on the outer cv test folds
               │     ├── outer_fold_0
               │     │   ├── outer_fold_0_splits.json        # JSON containing the indices of the original data in featurization_data_map which compose the train/test folds of split 0 
               │     │   │                                   # (Key: TRAINING_INDICES_KEY) & (Key: TEST_INDICES_KEY), respectively, as well as the score of refitted model on the test fold (Key: SCORE_STR)
               │     │   └── INNER_CV_RESULTS_DIR_NAME
               │     │       │
               │     │       ├── SPLITS_FILENAME             # JSON mapping each split index to a JSON containing the indices of the training data from the outer cv which composes the train/test folds of each split
               │     │       │                               # of the inner cv, these indices can be accessed using (Key: TRAINING_INDICES_KEY) & (Key: TEST_INDICES_KEY), respectively
               │     │       ├── INTERMEDIATE_RESULTS_CSV_FILENAME # .csv file storing the score of each unique hyperparameter + featurization combination on each test fold of the inner cv as well as the mean score and standard deviation
               │     │       └── FINAL_RESULTS_FILENAME      # JSON which stores various results including the name of the metric which was optimized in the nested CV (key: OPTIMIZE_METRIC_KEY),  best mean score (Key: BEST_SCORE_KEY), standard deviation (Key: BEST_STD_KEY) of 
               │     │                                       # the hyperparameter and featurization combination which gave the highest mean score on the test folds of the inner cv along with the corresponding
               │     │                                       # best algorithm-specific hyperparamers (key: BEST_PARAMS_KEY), best featurization (key: BEST_FEATURIZATION_KEY)
               │     └── ... # from outer_fold_0 to outer_fold_n  
               │
               ... # from algo 1 to n

        Returns:
            nested_cv_algo_performance_dict: Nested dictionary mapping the name of an algorithm to its corresponding performance dictionary on the outer cv. 
                                                Of the structure:
                {
                    <algorithm-name-1>: {
                                            "split_0": <score-on-test-fold-of-split-0>,
                                            ...,
                                            "split_n": <score-on-test-fold-of-split-n>,
                                            MEAN_OUTER_FOLDS_SCORE_KEY: <mean-score-across-splits>,
                                            STD_OUTER_FOLDS_SCORE_KEY: <standard-deviation-of-score-across-splits>
                                        },
                    ...
                }
        """
        # Create folder structure for saving results
        results_path = self._prepare_nested_cv_folder_structure(save_dir, all_algos_metadata)
        nested_cv_algo_performance_dict = {}
        for algo_name, algo_metadata in all_algos_metadata.items():
            if results_path is None:
                outer_cv_save_options = None
            else:
                outer_cv_save_options = {
                    SAVE_DIR_KEY: join(results_path, algo_name),
                    SAVE_ALGO_METADATA_KEY: False,
                    SAVE_CV_METADATA_KEY: False
                }
            algo_performance_dict, _ = self.perform_nested_cv_for_algo( 
                algo_metadata, 
                featurization_data_map,
                y, 
                save_options = outer_cv_save_options,
                verbose = verbose
            )
            nested_cv_algo_performance_dict[algo_name] = algo_performance_dict
        
        # Save final results
        if save_dir:
            save_dict_as_json(save_dir, NESTED_CV_RESULTS_FILENAME, nested_cv_algo_performance_dict)

        return nested_cv_algo_performance_dict