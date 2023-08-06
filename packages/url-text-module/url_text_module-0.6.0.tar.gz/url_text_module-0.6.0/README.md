# Urban Risk Lab (URL) Text Analysis Module

The goal of this module is to utilize various machine learning algorithms and featurizations of text string inputs to yield efficient and accurate predictions from text data in crowdsourced crisis reports in order to provide quick categorization that can be used to construct an aggregate summary of the unfolding crisis event. Beyond classification, this module embeds utilities for performing exploratory data analysis (EDA) and clustering of the text data. The module provides utilities for experimenting with various text embeddings including unigrams, bigrams, TF-IDF, and pretrained BERT with CLS pooling embeddings for both classification and clustering experiments. For the experiments mentioned above, the module provides analysis tools for performing EDA, visualizing clustering results, classification model performance, and any associated plotting.

This project is compatible with Python version >= 3.7.

### **Instructions to Install**
**Using PyPI -- latest version of package on PyPI**
```
pip install url-text-module
```
**Using GitLab Credentials -- using most recent commit**
1. Get `.env` file by requesting it from url_googleai@mit.edu, use subject headline `[Read Credentials URL Text Module GitLab]` and your plans for using it.
2. Load variables into the environment:
`source <path_to_.env>`
3. run `pip install -e git+https://$GITLAB_TOKEN_USER:$GITLAB_TOKEN@gitlab.com/react76/url-text-module.git@master#egg=url-text-module`

### **How to use in Python**
At the moment, all classes, constants, and functions can be imported at the root level of the package, like so:
```python
from url_text_module import (
    ...
)
```

### **Package Structure & Utilities**
This module provides various utilites for conducting reproducible experiments on crowdsourced crisis report text. These utilities include: 

##### **Preprocessing & Featurizing Text Data**

* [preprocessing_utils.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/preprocessing_utils.py) - Utilities for preprocessing and cleaning raw text inputs, e.g. tokenizing, removing stopwords, lemmatizing. 
   * Includes language specific utilites such as `tokenize_with_fugashi` for Japanese text and the `PretrainedBERTTokenizerAndModel` class for a paired tokenizer and BERT model pretrained on a large language-specific corpus to enable the creation of contextualized feature embedding (or feature vector) of an input text document with minimal preprocessing. 
   * Also contains utilties for normalizing the input featurizations/embeddings as input to a machine learning model (see `standardize_X`)
   * A function for using the metadata of a parameterized featurization to load the correct raw input string preprocessor in order to provide the proper input to the corresponding featurizer object (see `create_input_string_preprocessor`)
* [vectorizer_utils.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/vectorizer_utils.py) - Contains the language-agnostic Bag-of-Words (BOW) (see `BOWVectorizer`) and TF-IDF vectorizers (see `TFIDFVectorizer`) for the featurization of preprocessed, tokenized text data prior to being inputted to a machine learning model. Once fitted on a training text data corpus, the vectorizers store various useful attributes including the vocabulary of unique n-grams found for the training document corpus and a mapping from the n-gram to the coresponding index in the featurization vector. **Note:** Using these vectorizers might make private information that might need to be scrubbed (i.e. names, addresses, etc.) public via the vocabulary attributes if models using these vectorizers on the inputs are open-sourced

##### **Classifying Text Data**

* [classification.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/classification.py) - Utilities for performing classification on crisis text data including:
   * Performing cross-validation (CV) for tuning using grid search and a grid of hyperparameters to use for an algorithm and featurizations to apply to the input text (see `CrossValidationWithGridSearch`)
   * Performing algorithm selection using Nested Cross Validation (nested CV) (see `NestedCVWithGridSearch`)
   * Utilties for saving the results of classification experiments using cross validation or nested CV.
   * A function for developing a dummy classifier baseline for a classification experiment (see `get_dummy_classifier_preds_and_probs`)

##### **Clustering Text Data**

* [dimensionality_reduction.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/dimensionality_reduction.py) - Utilities for reducing the dimensionality of featurized text data
* [clustering.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/clustering.py) - Contains utilities for performing clustering experiments:
   * For experimenting with different K values for a clustering algorithm (see `run_clustering_experiment`)
   * For experimenting with various hyperparameter combinations including the type of featurization to use on input data (unigrams, bigrams, TF-IDF, and BERT with CLS pooling), the type of dimensionality reduction algorithm (None, PCA, and t-SNE) to use on the featurized text data, and the type of clustering algorithm (K-means and K-medoids) to use to cluster the data points (see `clustering_tuning`)
   * For a specific combination of hyperparameters mentioned above, also has auxillary utilities useful for the analysis of each cluster found including seeing the n text data inputs which are closest to the cluster center and finding the top n-grams with highest TF-IDF score for a cluster by forming a cluster-level document corpus by concatenating the documents of each cluster to form a new document representing the cluster (see `visualize_cluster_results` & `save_cluster_dfs`)


##### **Plotting Utilities**

* [plotting_utils.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/plotting_utils.py) - Utilities for producing visualizations for conducting analysis including exploratory data analysis and analysis of the results of clustering and classification experiments:
   * EDA:
      * Plotting a histogram of a feature's distribution, e.g. character count of text strings in a dataset (see `plot_data_hist`)
      * Plotting a box-and-whisker plot of a feature's distribution (see `plot_data_box_plot`)
      * Plotting a side-by-side comparison via box-and-whisker plots of a feature's distribution between two text datasets (see `plot_box_plot_data_comparison`)
   * Classification:
      * Plotting the results of various algorithms and an associated hyperparameter + featurization grid for a Nested Cross Validation procedure for Algorithm Selection (see `plot_nested_cv_results`)
      * Plotting the precision-recall curve for a binary classifier (see `plot_precision_recall_curve_for_model`)
   * Clustering:
      * Plotting the Within-Cluster Sum-of-Squares (WCSS) scores for different values of K (i.e. the "Elbow" plot) (see `plot_inertia_scores`)
      * Plotting the results of clustering data which has been reduced to 2D (e.g. by first applying a dimensionality reduction technique on the data and then applying a cluster algorithm) (see `plot_clustering`)

##### **Miscellaneous Utilities**

* [eda.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/eda_utils.py) - Utilities for performing non-plotting exploratory data analysis on crisis text datasets, e.g. computing the skew of a distribution (see `compute_distribution_skew`)

* [metric_utils.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/metric_utils.py) - Utilities for computing metric scores (F2, AUCPR etc.) by comparing ground truth labels against model predictions and creating scorer functions for a grid search procedure

* [classes.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/classes.py)- Defines classes that are useful across the package:
   * Named tuple for structuring metadata for a parameterized input featurization (see `Featurization` class)
   * Named tuple for storing metadata for an algorithm to be used in a cross-validation or nested cross-validation procedure, e.g. the name of the algorithm, 
   the hyperparameter + featurization grid to use and the type of normalization to apply to the input featurizations (see `AlgorithmMetadata`)
   * Named tuple for storing metadata for a fitted model including the
        hyperparameters used to train it, the featurization to apply to the input data, the normalization type to apply to the featurized inputs, and the version of the package used to fit the model (see `ModelMetadata` class)

* [constants.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/constants.py) - Defines various constants used throughout the package, including:
   * Keys and names of defaults, algorithms, featurization types, metadata, filenames, column names of pandas dataframes, etc. for consistent naming in dictionaries, pandas dataframes, and saved metadata (e.g. see `INPUT_COL_NAME`, `UNIGRAM_NAME`, `ALGO_NAME_KEY`)
   * Dictionaries mapping the name or types of algorithms, metrics, etc. to their corresponding object type or callable which can be instantiated or called -- these are the models/metrics/cross validation types/etc. which are compatible with the package (e.g. see `METRIC_FUNC_DICT`, `NORMALIZER_DICT`, `DIMENSIONALITY_REDUCTION_ALGORITHMS`, `CLUSTERING_ALGORITHMS`, `CROSS_VAL_DICT`, `ALGO_DICT`, `VECTORIZER_MAP`, `HF_BERT_MODELS`, etc.
   * Sets refering to compatible types of featurizations (see `FEATURIZATIONS_SET`), pretrained tokenizers (see `PRETRAINED_TOKENIZERS_SET`), algorithms which do not use random state (see `DOESNT_USE_RANDOM_STATE_SET`), strategies for a dummy classifier (see `DUMMY_CLASSIFIER_STRATEGIES`), etc.

* [misc_utils.py](https://gitlab.com/react76/url-text-module/-/blob/master/src/url_text_module/misc_utils.py) - Miscellaneous utilities which are useful across the package for ensuring reproducibility, saving metadata, making tables for latex, etc. (e.g. see `seed_everything`, `latexify_num`, `save_dict_as_json`, etc.)

 ## **For Maintainers**

 #### **Updating GitLab Repository**
 To add all modified files, commit those files, push to GitLab repo, and update repo with changes and tag number run:
```
sh update_repo.sh -t <tag> -m <commit message>
```

When updating dependencies, make sure to use:
1. `pipenv install <name-of-package>`
2. Update requirements.txt, run:  `sh update_requirements.sh`
3. Commit & push with the update command above

#### **Adding New Files to Python Package**
If you want add a file which contains new functionality, i.e. merits it own file separate from the existing, you must add it to the `__init__.py` file, like so:

You can do the following to import specific functions, classes, etc. from the file into the python package. Anything that isn't imported can't be used by the end-user
##### in `__init__.py` (specific imports):
```python
from .name_of_new_file import (
   specific_function_you_want_to_import,
   specific_class_you_want_to_import,
   ...
)
...
del name_of_new_file
```

If you want all functionality from the file to be available to the end-user, do the following:
##### in `__init__.py` (import everything):
```python
from .name_of_new_file import *
...
del name_of_new_file
```

#### **Publish Package to PyPI**
1. Launch virtual environment with `pipenv shell`
2. Install dependencies with `pipenv install`
3. Run `python setup.py bdist_wheel sdist`. To test, run:
   1. `sh test.sh`
   2. Run `import url_text_module` -- should give no errors if it's working properly
4. Run `twine upload dist/*`. Note: You will need login credentials for the URL PyPI Account in order to publish to PyPI. 

#### **Notes**
Installing torch with pipenv is a bit of a hassle. This GitHub [post](https://github.com/pypa/pipenv/issues/4961#issuecomment-1045679643) was helpful in figuring it out. To install torch with pipenv that have both CPU & GPU capabilities, this needs to be run:
`pipenv install --extra-index-url https://download.pytorch.org/whl/cu113/ "torch==1.9.0"`