from fugashi import Tagger
from transformers import AutoModelForMaskedLM

# Preprocessing
from sklearn.preprocessing import StandardScaler

# Supervised Methods
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

# Unsupervised Methods
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from sklearn_extra.cluster import KMedoids

# Evaluation
from sklearn.model_selection import StratifiedKFold

from typing import Callable, Dict, Union, Set, Optional, Tuple

from ._version import get_versions

from .vectorizer_utils import BOWVectorizer, TFIDFVectorizer
from .metric_utils import f2_func, make_scorer_from_func

__version__: str = get_versions()['version']
del get_versions
"""Version of URL Text Module
"""

###############################
# Text Data & Properties Keys #
###############################
INPUT_COL_NAME: str = 'input'
"""Name of column in dataframe which stores original text strings
"""

CHAR_COUNT_COL_NAME: str = 'character_count'
"""Name of column in dataframe which stores character length of
    the input text strings.
"""

EMBEDDINGS_COL_NAME: str = 'embeddings'
"""Name of column in dataframe which stores numerical embeddings of
    the input text strings.
"""

TRANSLATION_COL_NAME: str = 'translation'
"""Name of column in dataframe which stores a translation of the input in
    INPUT_COL_NAME
"""

#####################
# Japanese-Specific #
#####################

# Defaults
FUGASHI_TAGGER: Tagger = Tagger()
"""Tagger developed on Japanese text, capable of taking an input string and providing a list of word tokens
    and other associated metadata for each token, i.e. its lemma representation
"""

##############
# EMBEDDINGS #
##############

UNIGRAM_NAME: str = 'unigram'
"""Name associated with unigram (i.e. token frequency) embeddings of data
"""

BIGRAM_NAME: str = 'bigram'
"""Name associated with bigram (i.e. bigram frequency) embeddings of data
"""

TFIDF_NAME: str = 'TF-IDF'
"""Name associated with TF-IDF embeddings of data
"""

N_PARAM_STR: str = 'n'
"""Name of parameter to TextVectorizer class which determines the type of n-gram to use for featurization
"""

K_HIGHEST_PARAM_STR: str = 'k_highest'
"""Name of parameter to TextVectorizer class which determines the number of most frequent n-grams to keep
    in final featurization
"""

TF_NORMALIZE_PARAM_STR: str = 'tf_normalize'
"""Names of parameter to TF-IDF Vectorizer, which determines whether to use the raw or relative term frequency
    of an n-gram in a document
"""

BERT_NAME: str = 'BERT'
"""Name asscociated with BERT embeddings of data
"""

FEATURIZATIONS_SET: Set[str] = {
    UNIGRAM_NAME,
    BIGRAM_NAME,
    TFIDF_NAME,
    BERT_NAME,
}
"""Set of types of featurizations to use as inputs to algorithms
"""

EMBEDDING_TYPE_NAME: str = 'embedding_type'
"""Property name for specifying the type of embedding to use for a dataset
"""

FEATURIZATION_TYPE_KEY: str = 'type'
"""Key name specifying type of featurization being used
"""

VECT_NAMED_PARAMS_KEY: str = 'named_parameters'
"""Key name specifying dictionary which stores the named parameters and values of a vectorizer
"""

FEATURIZATION_METADATA_KEY: str = 'metadata'
"""Key name specifying the dictionary which stores metadata about the
    featurization, e.g. the model on huggingface used to create the featurization,
    the pretrained tokenizer used, etc.
"""

FUGASHI_STR: str = 'fugashi'
"""String corresponding to the pretrained Fugashi tokenizer for Japanese text
"""

PRETRAINED_TOKENIZERS_SET: Set[str] = {
    FUGASHI_STR
}
"""Set of pretrained tokenizers
"""

TOKENIZED_WITH_KEY: str = 'tokenized_with'
"""Key specifying the pretrained tokenizer which tokenized the input text
"""

STOPWORDS_KEY: str = 'stopwords'
"""Key specifying the stopwords metadata dictionary or indicating that no stopwords were used
"""

STOPWORDS_URL_KEY: str = 'url'
"""Key specifying the url which the stopwords list/set was fetched from
"""

LEMMATIZE_KEY: str = 'lemmatize'
"""Key for specifying whether or not lemmatization occured in the preprocessing of tokens
"""

MODEL_BASE_TYPE_KEY: str = 'model_base_type'
"""Key used for specifying type of HuggingFace model used for creating featurization
"""

MODEL_HF_HUB_NAME_KEY: str = 'model_hf_name'
"""Key used for denoting the name of the model on HuggingFace's model hub where the pretrained model lives
"""

AUTO_MODEL_MASKED_ML_STR: str = 'AutoModelForMaskedLM'
"""String for the HuggingFace Masked Language Modeling Auto Model construct
"""

HF_BERT_MODELS: Dict[str, type] = {
    AUTO_MODEL_MASKED_ML_STR: AutoModelForMaskedLM
}

REVISION_HASH_KEY: str = 'revision_hash'
"""Key used for specifying the hash to use for pretrained model on HuggingFace's model hub
"""

VECTORIZER_MAP: Dict[str, Optional[type]] = {
    TFIDF_NAME: TFIDFVectorizer,
    UNIGRAM_NAME: BOWVectorizer,
    BIGRAM_NAME: BOWVectorizer,
    BERT_NAME: None
}
"""Dictionary mapping type of featurization to corresponding vectorizer
"""

SORTED_FEATURIZATIONS_DICT: Dict[int, str] = {
    0: UNIGRAM_NAME,
    1: BIGRAM_NAME,
    2: TFIDF_NAME,
    3: BERT_NAME,
}
"""Dictionary putting the featurizations in the order in which to investigate them when performing
    tuning
"""

#############################
# Classification Algorithms #
#############################

CLASS_NAME_TO_IDX_KEY: str = 'class_idx_dict'
"""Key used for storing the dictionary mapping string class name to integer label
"""

CLASS_NAME_TO_IDX_FILENAME: str = 'class_idx_dict.json'
"""Filename of the json which stores the class string to integer label metadata for 
    a classification algorithm
"""

LOGISTIC_REGRESSION_KEY: str = 'Logistic Regression'
RANDOM_FOREST_KEY: str = 'Random Forest'
DECISION_TREE_KEY: str = 'Decision Tree'
MULTINOMIAL_NAIVE_BAYES_KEY: str = 'Multinomial Naive Bayes'
K_NEAREST_NEIGHBORS_KEY: str = 'K-Nearest Neighbors'
SUPPORT_VECTOR_MACHINE_KEY: str = 'Support Vector Machine'
"""Various keys used for developing dictionaries for classification experiments
"""

ALGO_DICT: Dict[str, type] = {
    LOGISTIC_REGRESSION_KEY: LogisticRegression,
    RANDOM_FOREST_KEY: RandomForestClassifier,
    DECISION_TREE_KEY: DecisionTreeClassifier,
    MULTINOMIAL_NAIVE_BAYES_KEY: MultinomialNB,
    K_NEAREST_NEIGHBORS_KEY: KNeighborsClassifier,
    SUPPORT_VECTOR_MACHINE_KEY: SVC,
}
"""Dictionary storing the classes for various classification algorithms
"""

DOESNT_USE_RANDOM_STATE_SET: Set[str] = {
    MULTINOMIAL_NAIVE_BAYES_KEY, 
    K_NEAREST_NEIGHBORS_KEY
}
"""Set denoting which classification algorithms which do not have a random state parameter
"""

ALGO_NAME_KEY: str = 'algo_name'
"""Key used to store name of the algorithm
"""

ALGO_PARAM_GRID_KEY: str = 'algo_param_grid'
"""Key used for storing algorithm-specific hyperparameter grids
"""

FEATURIZATION_HYPERPARAM_KEY: str = 'featurization_grid'
"""Key used for storing featurizations used for evaluating an algorithm
"""

FEATURIZATION_KEY: str = 'featurization'
"""Key used for storing the featurization used for inputs to a model
"""

HYPERPARAMETERS_KEY: str = 'hyperparameters'
"""Key used for storing hyperparameter dictionary which is composed of algorithm-specific hyperparameters
    and various featurizations to use as input to the algorithm
"""

NORMALIZER_TYPE_KEY: str = 'normalizer_type'
"""Key used for storing the type of preprocessing normalizer used for the input to an algorithm
"""

ALGORITHM_METADATA_FILENAME: str = 'algorithm_metadata.json'
"""Name of the .json file which stores algorithm metadata for a Nested CV experiment
"""

CV_METADATA_FILENAME: str = 'cv_metadata.json'
"""Name of the .json file which stores metadata for a CV procedure
"""

NESTED_CV_METADATA_FILENAME: str = 'nested_cv_metadata.json'
"""Name of the .json file which stores metadata for a Nested CV procedure
"""

OUTER_CV_RESULTS_FILENAME: str = 'outer_cv_results.json'
"""Name of the .json file which stores the results on the outer CV of Nested Cross Validation
"""

MODEL_METADATA_FILENAME: str = 'model_metadata.json'
"""Filename for JSON which stores metadata about a fitted model including its hyperparameters, featurization of the input,
    the normalizer used for the inputs to the model, and the random state used for the model
"""

INTERMEDIATE_RESULTS_CSV_FILENAME: str = 'intermediate_results.csv'
"""Name of .csv which stores the intermediate results of the Gridsearch CV for each hyperparameter combination and 
    data split
"""

SPLITS_FILENAME: str = 'splits.json'
"""Name of the .json file which stores the train/test indices of the original data used in the splits by the CV procedure
"""

FINAL_RESULTS_FILENAME: str = 'final_results.json'
"""Name of the .json file which stores the final results of CV procedure
"""

NESTED_CV_RESULTS_FILENAME: str = 'nested_cv_outer_folds_results.json'
"""Name of the .json file which stores the results of the Nested CV procedure
"""

NESTED_CV_RESULTS_PLOT_FILENAME: str = 'nested_cv.png'
"""Name of the .png file which plots the results of Nested CV for various algorithms on the test folds of the outer cv procedure
"""

INNER_CV_RESULTS_DIR_NAME: str = 'Inner CV Results'
"""Name of the directory which stores the results of the inner cross validation procedure (of Nested Cross Validation) for the
    outer loop of Nested CV
"""

RESULTS_DIR_NAME: str = 'Results'
"""Name of the directory which stores the results from an experiment
"""

HYPERPARAMETERS_AND_SETTINGS_DIR_NAME: str = 'Hyperparameters and Settings'
"""Name of the directory which stores the hyperparamters and settings for experiments
"""

SAVE_DIR_KEY: str = 'save_dir'
"""Name of the key which stores the path to a directory in which files (e.g. .json, .csv, etc.) will be saved
"""

SAVE_ALGO_METADATA_KEY: str = 'save_algo_metadata'
"""Name of the key which stores whether or not algorithm metadata should be saved
"""

SAVE_CV_METADATA_KEY: str = 'save_cv_metadata'
"""Name of the key which stores whether or not to save the metadata associated with the cross-validation procedure
"""

#############################
# Classification Evaluation #
#############################

# Cross Validation Metadata
STRATIFIED_K_CV_NAME: str = 'stratified_k_fold'
"""Name of the stratified K-fold cross validation procedure in which
    label distributions in the data are preserved in the splittings
"""

CROSS_VAL_DICT: Dict[str, type] = {
    STRATIFIED_K_CV_NAME: StratifiedKFold
}
"""Dictionary storing various types of cross validation procedures
"""

CV_TYPE_KEY: str = 'cv_type'
"""Key storing the type of cross validation procedure being employed in the procedure
    Value must be a key in CROSS_VAL_DICT
"""

RANDOM_STATE_KEY: str = 'seed'
"""Key used to store the random seed used for stochastic algorithms being
    evaluated using the CV procedure
"""

RANDOM_STATE_STR: str = 'random_state'
"""String representing parameter name of many sklearn utitities to enable reproducibility
"""

SHUFFLE_KEY: str = 'shuffle'
"""Key used to store the boolean indicating if data should be shuffled randomly
    when creating the splits to run the CV procedure
"""

N_JOBS_KEY: str = 'n_jobs'
"""Key storing the number of jobs to run in parallel. Limited by the number of available 
    processors on the host
"""

OPTIMIZE_METRIC_KEY: str = 'optimize_metric'
"""Key used to store the metric being computed in the cross validation procedure
"""

NUM_SPLITS_KEY: str = 'num_splits'
"""Key used to store the number of splits used in a cross validation procedure
"""

# Constant Keys for saving intermediate & final results of CV
TRAINING_INDICES_KEY: str = 'training_indices'
"""Key used for storing the indices associated with the training fold in a split of the CV procedure
"""

TEST_INDICES_KEY: str = 'test_indices'
"""Key used for storing the indices associated with the test fold in a split of the CV procedure
"""

SCORE_STR: str = 'score'
"""Key used for storing the score of a fitted model on a test fold
"""

BEST_PARAMS_KEY: str = 'best_parameters'
"""Key used for storing the best algorithm-specific hyperparameters found for an algorithm from a CV procedure
"""

BEST_FEATURIZATION_KEY: str = 'best_featurization'
"""Key used for storing the best featurization applied to the input found for an algorithm from a CV procedure
"""

BEST_SCORE_KEY: str = 'best_score'
"""Key used for storing the best average score across test folds for the best hyperparameter combination found from
    applying the grid-search cross validation procedure
"""

BEST_STD_KEY: str = 'best_std'
"""Key used for storing the standard deviation found for the score across test folds for the best hyperparameter combination found from
    applying the grid-search cross validation procedure
"""

# scikit-learn's Grid search result keys
PARAMETERS_COL_NAME: str = 'params'
"""Key used for accessing scikitlearn's grid search object for accessing the array of algorithm-specific hyperparameters which form the
    grid investgated in the grid search and for saving intermediate results of grid cross validation
"""

MEAN_TEST_SCORE_COL_NAME: str = 'mean_test_score'
"""Column used for storing the mean score on the test folds in a cross validation procedure for a hyperparameter combination.
    Also used for accessing scikitlearn's grid search object for the array which stores the mean scores across the test folds for each
    hyperparameter combination in the grid
"""

STD_TEST_SCORE_COL_NAME: str = 'std_test_score'
"""Column used for storing the standard devation of a score on the test folds in a cross validation procedure for a hyperparameter combination.
    Also used for accessing scikitlearn's grid search object for the array which stores the standard deviation of the scores across the test folds for 
    hyperparameter combination in the grid
"""

SPLIT_STR: str = 'split'
"""String used as part of building the columns names for saving the intermediate results of cross validation, i.e. 
    saving the results of each hyperparameter combination on the test fold in each split
"""

TEST_SCORE_STR: str = 'test_score'
"""String used as part of building the columns names for saving the intermediate results of cross validation, i.e. 
    saving the results of each hyperparameter combination on the test fold in each split
"""

FEATURIZATION_COL_NAME: str = 'featurization'
"""Column name used for storing the featurization used in the cross validation procedure
"""

# Nested CV Metadata
OUTER_SPLITS_NUM_KEY: str = 'outer_splits_num'
"""Key which stores the number of splits to use in the outer cv of the Nested CV procedure
"""

INNER_SPLITS_NUM_KEY: str = 'inner_splits_num'
"""Key which stores the number of splits to use in the outer cv of the Nested CV procedure
"""

MEAN_OUTER_FOLDS_SCORE_KEY: str = 'mean_outer_folds_score'
"""Key used for storing the mean score of an algorithm + hyperparameter grid on the outer cv test folds of nested CV 
"""

STD_OUTER_FOLDS_SCORE_KEY: str = 'std_outer_folds_score'
"""Key used for storing the standard deviation of the score of an algorithm + hyperparameter grid on the outer cv test folds of nested CV 
"""

# Metrics
F2_NAME: str = 'f2'
"""Name of key used for metric computation used in evaluation
"""

METRIC_FUNC_DICT: Dict[str, Callable] = {
    F2_NAME: f2_func,
}
"""Dictionary storing metric function for each metric
"""

METRIC_SCORER_DICT: Dict[str, Callable] = {
    F2_NAME: make_scorer_from_func(f2_func)
}
"""Dictionary storing scorer for each metric
"""

def get_metric_func_and_scorer(metric_name: str) -> Tuple[Callable, Callable]:
    """Returns function and scorer associated with metric, metric_name

    Args:
        metric_name: Name of the metric which the function and scorer are being fetched. Must be
                        a key in METRIC_FUNC_SCORER_DICT
    Returns:
        func: Function which computes the metric, metric_name
        scorer: SKlearn scorer which uses func associated with metric name
    """
    func, scorer = METRIC_FUNC_DICT[metric_name], METRIC_SCORER_DICT[metric_name]
    return func, scorer

SCORER_KEY: str = "scorer"
"""Key used for storing a callable scorer when performing evaluation, i.e. cross-validation
"""

METRIC_FUNC_KEY: str = "metric_func"
"""Key used for storing the funtion which computes a metric score when computing
    classification performance
"""

CONSTANT_STR: str = 'constant'
"""String specifying constant classifier strategy in which a classifier always predicts a constant
    class provided by the user
"""

STRATIFIED_STR: str = 'stratified'
"""String specifying stratified classifier strategy in which a classifier makes predictions by respecting
    the class distribution of the training data
"""

DUMMY_CLASSIFIER_STRATEGIES: Set[str] = {
    CONSTANT_STR,
    STRATIFIED_STR
}
"""Different strategies to use for a Dummy Classifier baseline
"""

STRATEGY_KEY: str = 'strategy'
"""Key used for specifying the strategy used by a dummy classifier
"""

CONSTANT_KEY: str = 'constant'
"""Key used for user-specified class to predict for a 'constant' strategy dummy classifier
"""

#################
# Preprocessing #
#################

STANDARD_SCALER_KEY: str = 'standard_scaler'
"""Key name of the standard scaler preprocessing normalization, in which all
    features are made to have zero-mean & unit variance
"""

NORMALIZER_DICT: Dict[str, type] = {
    STANDARD_SCALER_KEY: StandardScaler
}
"""Dictionary storing various data preprocessing objects
"""


###########################
# Unsupervised Algorithms #
###########################

# Dimensionality Reduction
PCA_NAME: str = 'PCA'
"""Name of the Principle Component Analysis algorithm
"""

TSNE_NAME: str = 't-SNE'
"""Name of the t-distributed Stochastic Neighboring Embedding algorithm
"""

DIMENSIONALITY_REDUCTION_ALGORITHMS: Dict[str, type] = {
      PCA_NAME: PCA,
      TSNE_NAME: TSNE
}
"""Dictionary storing default dimensionality reduction algorithms for ease of access
"""

# Useful key names for dimensionality reduction
DIMENSIONALITY_REDUCTION_ALGORITHM_NAME: str = 'dim_red_algo_name'
"""Property name for name of dimensionality reduction algorithm name
"""

NUM_COMPONENTS_NAME: str = 'n_components'
"""Property name for specifying number of components to use for dimensionality reduction algorithm
"""

TRANSFORMED_X_COL_NAME: str = 'transformed_X'
"""Name of the column in a DataFrame which stores the reduced data vectors, X after applying a dimensionality reduction algorithm on the original data
"""

# Clustering
KMEANS_NAME: str = 'K-means'
"""Name of the K-means clustering algorithm
"""

KMEDOIDS_NAME: str = 'K-medoids'
"""Name of the K-medoids clustering algorithm
"""

CLUSTERING_ALGORITHMS: Dict[str, type] = {
      KMEANS_NAME: KMeans, 
      KMEDOIDS_NAME: KMedoids
}
"""Dictionary storing default clustering algorithms for ease of access
"""

# Useful key names for clustering algorithms
CLUSTERING_ALGORITHM_NAME: str = 'cluster_algo_name'
"""Property name for specifying which clustering algorithm to use
"""

NUM_CLUSTERS_NAME: str = 'n_cluster'
"""Property name for specifying number of clusters to use when applying a clustering
    algorithm
"""

CLUSTER_ID_COL_NAME: str = 'cluster_id'
"""Name of column in DataFrame which stores the ID of the cluster a datapoint is a part of
"""

CLUSTER_CENTER_COORDINATES_COL_NAME: str = 'cluster_center_coords'
"""Name of column in DataFrame which stores the Numpy array corresponding to the
    center of a cluster
"""

EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME: str = 'euclid_dist_to_center'
"""Name of the column in DataFrame which stores the euclidean distance to the center of the cluster
"""

TOP_TFIDF_N_GRAMS_COL: str = 'top_tfidf_n_grams'
"""Name of the column in a DataFrame which shows the n-grams with the highest TF-IDF score for a cluster-level document for a cluster-level document corpus, i.e.
    where all documents in a cluster are concatenated to form a new document
"""

############
# DEFAULTS #
############
DEFAULT_SEED: int = 1
"""Default seed for enabling reproducibility
"""

DEFAULT_N_JOBS: int = -1
"""Default number of parallel jobs to perform. -1 means to use all available
    processors to perform the jobs
"""

DEFAULT_NUM_COMPONENTS: int = 2
"""Default number of components to use in dimsionality reduction algorithms
"""

DEFAULT_DIM_RED_OPTIONS: Dict[str, Union[str, int]] = {
    DIMENSIONALITY_REDUCTION_ALGORITHM_NAME: PCA_NAME, 
    NUM_COMPONENTS_NAME: DEFAULT_NUM_COMPONENTS
}
"""Default options for configuring a dimensionality reduction algorithm
"""

DEFAULT_NUM_CLUSTERS: int = 2
"""Default number of clusters to group a dataset into
"""

DEFAULT_MAX_K_CLUSTERS: int = 20
"""Default max number of clusters to use when performing a clustering experiment for various values of K
"""

DEFAULT_CLUSTERING_OPTIONS: Dict[str, Union[str, int]] = {
    CLUSTERING_ALGORITHM_NAME: KMEANS_NAME, NUM_CLUSTERS_NAME: DEFAULT_NUM_CLUSTERS
}
"""Default options for configuring a clustering algorithm
"""

DEFAULT_EMBEDDINGS_OPTIONS: Dict[str, str] = {
    EMBEDDING_TYPE_NAME: TFIDF_NAME
}
"""Default options for selecting an embedding type for the original data
"""

DEFAULT_TFIDF_OPTIONS: Dict[str, Union[int, bool, None]] = {
    N_PARAM_STR: 1, K_HIGHEST_PARAM_STR: None, TF_NORMALIZE_PARAM_STR: True
}
"""Default options used for instantiating a TFIDF vectorizer
"""

#################
# Miscellaneous #
#################
PACKAGE_VERSION_KEY: str = 'url_text_module_version'
"""Key used for storing version of URL Text Module used
"""

PICKLE_EXTENSION: str = '.pkl'
"""Extension for saving pickle files
"""