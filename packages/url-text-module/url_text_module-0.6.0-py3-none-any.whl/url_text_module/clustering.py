
import numpy as np
import pandas as pd

from tqdm import tqdm

from os.path import join

from copy import copy, deepcopy

from typing import Dict, Optional, Union, Tuple, List

from .constants import (
    CLUSTERING_ALGORITHMS,
    DEFAULT_CLUSTERING_OPTIONS,
    CLUSTERING_ALGORITHM_NAME,
    DEFAULT_NUM_COMPONENTS,
    PCA_NAME,
    TRANSFORMED_X_COL_NAME,
    DIMENSIONALITY_REDUCTION_ALGORITHMS,
    DIMENSIONALITY_REDUCTION_ALGORITHM_NAME,
    INPUT_COL_NAME,
    NUM_CLUSTERS_NAME,
    KMEANS_NAME,
    DEFAULT_MAX_K_CLUSTERS,
    CLUSTER_ID_COL_NAME,
    CLUSTER_CENTER_COORDINATES_COL_NAME,
    EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME,
    TOP_TFIDF_N_GRAMS_COL,
    EMBEDDING_TYPE_NAME,
    DEFAULT_SEED,
    DEFAULT_EMBEDDINGS_OPTIONS,
    DEFAULT_TFIDF_OPTIONS,
    NUM_COMPONENTS_NAME
)

from .vectorizer_utils import TFIDFVectorizer

from .dimensionality_reduction import reduce_dims

from .plotting_utils import plot_inertia_scores, plot_clustering

from .misc_utils import (
  latexify_wcss_df, 
  compute_euclid_dist,
  get_top_k_tfidf_n_grams
)

def fit_k_algo(
    X: np.ndarray, 
    cluster_options: Dict[str, Union[str, int]] = DEFAULT_CLUSTERING_OPTIONS, 
    seed: int = DEFAULT_SEED
) -> object:
    """Fits a clustering algorithm on a dataset X

    Args:
        X: Data matrix of shape (num. of data points, num. of features) to be cluster
        cluster_options: Dictionary of options for configuring the clustering algorithm including the name
                            of the clustering algorithm (key: CLUSTERING_ALGORITHM_NAME) and the number of clusters
                            to find using the algorithm (key: NUM_CLUSTERS_NAME). The value associated with key
                            CLUSTERING_ALGORITHM_NAME must be a key in the CLUSTERING_ALGORITHMS dictionary.
                            Default is DEFAULT_CLUSTERING_OPTIONS
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Defaults to DEFAULT_SEED
    
    Returns:
        fitted_cluster_algo: Fitted clustering algorithm with relevant properties pertaining to the cluster centers found for
                                a dataset which can also determine which cluster data points in the data set belong to
    """
    assert CLUSTERING_ALGORITHM_NAME in cluster_options
    assert NUM_CLUSTERS_NAME in cluster_options
    cluster_algo_name, n_clusters = cluster_options[CLUSTERING_ALGORITHM_NAME], cluster_options[NUM_CLUSTERS_NAME]
    assert cluster_algo_name in CLUSTERING_ALGORITHMS
    assert n_clusters >= 1
    cluster_algo = CLUSTERING_ALGORITHMS[cluster_algo_name]
    fitted_cluster_algo = cluster_algo(n_clusters = n_clusters, random_state = seed).fit(X)
    return fitted_cluster_algo

def dim_red_and_cluster(
    X: np.ndarray,
    dim_red_options: Optional[Dict[str, Union[str, int]]] = None,
    cluster_options: Dict[str, Union[str, int]] = DEFAULT_CLUSTERING_OPTIONS,
    seed: int = DEFAULT_SEED
) -> Tuple[np.ndarray, object]:
    """Convience method which reduces the dimension (if specified) of data matrix X, and clusters the data
    
    Args:
        X: Data matrix to be reduced (if specified), and then clustered
        dim_red_options: Dictionary of options for configuring the dimensionality reduction algorithm including the name of the
                            algorithm (key: DIMENSIONALITY_REDUCTION_ALGORTIHM_NAME) to use and the number of 
                            components (key: NUM_COMPONENTS_NAME) to reduce the data embeddings to. 
                            Dimensionality reduction algorithm name must be a key in DIMENSIONALITY_REDUCTION_ALGORITHMS dictionary.
                            Defaults to None in which no dimensionality reduction is applied, and the selected embeddings are used
        cluster_options: Dictionary of options for configuring the clustering algorithm including the name
                            of the clustering algorithm (key: CLUSTERING_ALGORITHM_NAME) and the number of clusters
                            to find using the algorithm (key: NUM_CLUSTERS_NAME). The value associated with key
                            CLUSTERING_ALGORITHM_NAME must be a key in the CLUSTERING_ALGORITHMS dictionary.
                            Default is DEFAULT_CLUSTERING_OPTIONS
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Defaults to DEFAULT_SEED
    
    Returns:
        transformed_X: Reduced data if dim_red_options is not None, otherwise it's a copy of the original data, X.
        fitted_cluster_algo: Fitted clustering algorithm with relevant properties pertaining to the cluster centers found for
                                the reduced data which can also determine which cluster data points in the data set belong to
    """
    transformed_X = reduce_dims(X, dim_red_options = dim_red_options, seed = seed)
    fitted_cluster_algo = fit_k_algo(transformed_X, cluster_options = cluster_options, seed = seed)
    return transformed_X, fitted_cluster_algo

def run_k_clustering_algo(
    X: np.ndarray, 
    K_vals: List[int], 
    cluster_algo_name: str = KMEANS_NAME, 
    seed: int = DEFAULT_SEED
) -> List[float]:
    """Computes Within-Cluster Sum of Squares (WCSS) scores of clustering for each value of K clusters in K_vals

    Args:
        X: Data matrix to be clustered
        K_vals: List of consecutive positive integer values of K, each denoting the number of clusters to cluster data X
                    into
        cluster_algo_name: Name of the algorithm which will perform the clustering. Name must be a key in the CLUSTERING_ALGORITHMS
                            dictionary
        
    Returns:
        inertia_scores: List of Within-Cluster Sum of Squares scores, or inertia for each K in K_vals
    """
    inertia_scores = []
    for k in tqdm(K_vals):
        cluster_options = {
            CLUSTERING_ALGORITHM_NAME: cluster_algo_name, NUM_CLUSTERS_NAME: k
        }
        fitted_clusters = fit_k_algo(X, cluster_options = cluster_options, seed = seed)
        inertia_scores.append(fitted_clusters.inertia_)
    return inertia_scores

def run_clustering_experiment(
    X_embeddings_dict: Dict[str, np.ndarray],
    K_vals: List[int],
    X_options: Dict[str, str] = DEFAULT_EMBEDDINGS_OPTIONS,
    dim_red_options: Optional[Dict[str, Union[str, int]]] = None,
    cluster_algo_name: str = KMEANS_NAME,
    seed: int = DEFAULT_SEED
) -> Tuple[List[float], str]:
    """Convience method which selects an embedding to use of the original data, reduces the dimension 
        (if specified), and clusters the data for various values of K in the K_vals parameter, computing 
        the Within-Cluster Sum of Squares scores, or inertia for each value of K.
    
    Args:
        X_embeddings_dict: Dictionary mapping types of embeddings to the corresponding embedded data
        K_vals: List of consecutive positive integer values of K, each denoting the number of clusters to cluster the data
                    into
        X_options: Dictionary with options for selecting an embedding of the data to use including the name 
                    of the type of the embedding (key: EMBEDDING_TYPE_NAME). The value associated with the EMBEDDING_TYPE_NAME must be 
                    a key in X_embeddings_dict. Default is DEFAULT_EMBEDDINGS_OPTIONS
        dim_red_options: Dictionary of options for configuring the dimensionality reduction algorithm including the name of the
                            algorithm (key: DIMENSIONALITY_REDUCTION_ALGORTIHM_NAME) to use and the number of 
                            components (key: NUM_COMPONENTS_NAME) to reduce the data embeddings to. 
                            Dimensionality reduction algorithm name must be a key in DIMENSIONALITY_REDUCTION_ALGORITHMS dictionary.
                            Defaults to None in which no dimensionality reduction is applied, and the selected embeddings are used
        cluster_algo_name: Name of the algorithm which will perform the clustering. Name must be a key in the CLUSTERING_ALGORITHMS
                            dictionary
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Defaults to DEFAULT_SEED
    
    Returns:
        inertia_scores: List of Within-Cluster Sum of Squares scores, or inertia for each K in K_vals
        hyperparams_path: Concatenated string for the various hyperparameters used for computing the clustering, namely
                            the name of the type of embedding used, the dimensionality reduction algorithm used (with the number
                            of components used), and the clustering algorithm used
    """
    embedding_type = X_options[EMBEDDING_TYPE_NAME]
    X = X_embeddings_dict[embedding_type]
    print(f"Using embedding_type: {embedding_type}")
    print(f"Using Dim. Reduction Settings: {dim_red_options}")
    print(f"Using clustering algorithm: {cluster_algo_name}")
    X = reduce_dims(X, dim_red_options = dim_red_options, seed = seed)
    inertia_scores = run_k_clustering_algo(X, K_vals, cluster_algo_name = cluster_algo_name, seed = seed)
    hyperparams_path = f"{embedding_type} + "
    if dim_red_options is not None:
        hyperparams_path += f"{dim_red_options[DIMENSIONALITY_REDUCTION_ALGORITHM_NAME]} ({dim_red_options[NUM_COMPONENTS_NAME]} comps) + "
    hyperparams_path += f"{cluster_algo_name}"
    return copy(inertia_scores), hyperparams_path

def clustering_tuning(
    X_embedding_dict: Dict[str, np.ndarray],
    max_k: int = DEFAULT_MAX_K_CLUSTERS,
    n_components: int = DEFAULT_NUM_COMPONENTS,
    seed: int = DEFAULT_SEED,
    save_path: Optional[str] = None,
    title: Optional[str] = None,
) -> Tuple[pd.DataFrame, List[float]]:
    """For each combination of embedding type, dimensionality reduction algorithm (with n_components), and clustering algorithm,
        performs various clustering experiments for values of K from 2 to max_K, plotting the Within-Cluster Sum-of-Squares (WCSS) plot, or Elbow plot, 
        saving the plots to save_path, and returning a DataFrame and matrix the Within-Cluster Sum-of-Squares scores for each combination across values of K
        The DataFrame and a latex compatible version of the DataFrame are saved to the save_path directory.
    
    Args:
        X_embeddings_dict: Dictionary mapping types of embeddings to the corresponding embedded data
        max_k: Integer denoting the maximum K clusters for which clustering will be applied from 2 clusters to max_k clusters.
                Default is DEFAULT_MAX_K_CLUSTERS
        n_components: Integer denoting the number of components to reduce the embedded data to with a dimensionality reduction algorithm. 
                        Default is DEFAULT_NUM_COMPONENTS
        seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Defaults to DEFAULT_SEED
        save_path: Directory on host's filesystem to save the generated .png files from plotting the elbow plot for each hyperparameter combination. 
                    as well as where to save the DataFrame of WCSS values for each hyperparameter combination. Default is None
        title: Title for the generated elbow plots. Default is None
    
    Returns:
        wcss_df: DataFrame with hyperparameter columns for 
                    embedding type (col name: EMBEDDING_TYPE_NAME), 
                    dimensionality reduction algorithm used (col name: DIMENSIONALITY_REDUCTION_ALGORTIHM_NAME), 
                    number of components used for dim. red. algorithm (col name: NUM_COMPONENTS_NAME),
                    clustering algorithm used, (col name: CLUSTERING_ALGORITHM_NAME)
                    and columns for storing the WCSS score for each value of K (col name: "K = i") from i = 2 to max_k
                    associated with the hyperparameter combination values in the same row 
        wcss_scores: Numpy array of the WCSS scores where each row corresponds to a hyperparameter combination
                        and each column with index i, is the WCSS score for K = i + 2, that is, each row
                        is the WCSS scores for K = 2 to max_K for a unique hyperparameter combination
    """
    num_K = max_k - 1
    K_vals = [k for k in range(2, max_k + 1)]
    embeddings_type_list = list(X_embedding_dict.keys())
    dim_red_algos_list = [None] + list(DIMENSIONALITY_REDUCTION_ALGORITHMS.keys())
    cluster_algos_list = list(CLUSTERING_ALGORITHMS.keys())
    cluster_algo_hyperparams, dim_red_hyperparams, n_comps_hyperparams, embedding_hyperparams = [], [], [], []
    num_combos = len(cluster_algos_list)*len(dim_red_algos_list)*len(embeddings_type_list)
    wcss_scores = np.zeros((num_combos, num_K))
    i = 0
    
    for embedding_type in embeddings_type_list:
        for dim_red_algo_name in dim_red_algos_list:
            if dim_red_algo_name is not None:
                dim_red_options = {
                    DIMENSIONALITY_REDUCTION_ALGORITHM_NAME: dim_red_algo_name,
                    NUM_COMPONENTS_NAME: n_components
                }
            else:
                dim_red_options, dim_red_algo_name = None, None
            for cluster_algo_name in cluster_algos_list:
                X_options = {
                    EMBEDDING_TYPE_NAME: embedding_type
                }
                cluster_algo_hyperparams.append(cluster_algo_name)
                dim_red_hyperparams.append(dim_red_algo_name)
                n_comps_hyperparams.append(None if dim_red_algo_name is None else n_components)
                embedding_hyperparams.append(embedding_type)
                inertia_scores, hyperparams_path = run_clustering_experiment(
                    X_embedding_dict,
                    K_vals,
                    X_options = X_options,
                    dim_red_options = dim_red_options,
                    cluster_algo_name = cluster_algo_name,
                    seed = seed
                )
                wcss_scores[i, :] = inertia_scores
                plot_inertia_scores(inertia_scores, label = hyperparams_path, title = title, path = save_path)
                i += 1
    hyperparams_data = np.array(list(zip(embedding_hyperparams, dim_red_hyperparams, n_comps_hyperparams, cluster_algo_hyperparams)))
    wcss_df = pd.DataFrame(hyperparams_data, columns=[
        EMBEDDING_TYPE_NAME, DIMENSIONALITY_REDUCTION_ALGORITHM_NAME, NUM_COMPONENTS_NAME, CLUSTERING_ALGORITHM_NAME
    ])
    i = 0
    K_col_names = []
    for K in K_vals:
        K_col_str = f'K = {K}'
        K_col_names.append(K_col_str)
        wcss_df[K_col_str] = wcss_scores[:, i]
        i += 1
    if save_path:
        wcss_df.to_csv(join(save_path, 'wcss_scores.csv'), index = False)
        latexified_wcss_df = latexify_wcss_df(wcss_df, K_col_names)
        latexified_wcss_df.to_csv(join(save_path, 'latexified_wcss_scores.csv'), index = False)
    return wcss_df, wcss_scores

def compute_cluster_dfs(
  transformed_X: np.ndarray, 
  data_df: pd.DataFrame, 
  fitted_cluster_algo: object, 
  tokens_col_name: str, 
  translations_col_name: Optional[str] = None
) -> List[pd.DataFrame]:
  """Computes a DataFrame for each cluster found with the clustering object fitted_cluster_algo object

  Args:
    transformed_X: Numpy data matrix containing the (possibly dimensionality reduced) data used to fit the clustering algorithm fitted_cluster_algo
    data_df: DataFrame containing the original input text in the INPUT_COL_NAME column, tokenized versions of these inputs in the tokens_col_name column, and
              possibly translations of the input text in the translations_col_name column. The rows of data_df, i.e. the data points correspond to 
              the rows of transformed_X data matrix
    fitted_cluster_algo: Fitted clustering algorithm with relevant properties pertaining to the cluster centers found for
                                  transformed_X which can also determine which cluster data points in transformed_X belong to
    tokens_col_name: Name of the column in data_df which contains the tokenized version of the INPUT_COL_NAME column
    translations_col_name: Name of the column in data_df which contains a translation of the input text in INPUT_COL_NAME column. Default is None
  
  Returns:
    cluster_df_list: List of DataFrames where the index of the DataFrame corresponds to the cluster id, i.e. cluster_df_list[0] is the DataFrame associated with cluster ID 0. 
                      Each cluster DataFrame stores various important metadata about the cluster including the data points in data_df which belong to the cluster including 
                      the input text (column name: INPUT_COL_NAME), the tokens associated with the input text (column text: tokens_col_name), 
                      possibly translations of the input text (column name: translations_col_name), the id of the cluster (column name: CLUSTER_ID_COL_NAME), the reduced dimensionality, 
                      or "transformed" data transformed_X subsetted to rows which belongs in that cluster, and finally the coordinates of the cluster center (column name: CLUSTER_CENTER_COORDINATES_COL_NAME) & 
                      the euclidean distance of the vector in transformed_X to its cluster's center (column name: EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME). 

  """
  cluster_df_list = []
  columns_to_preserve = [INPUT_COL_NAME, tokens_col_name, translations_col_name] if translations_col_name else [INPUT_COL_NAME, tokens_col_name]
  clusters_df = data_df[columns_to_preserve].copy(deep = True)
  clusters_df[CLUSTER_ID_COL_NAME] = fitted_cluster_algo.labels_
  cluster_coordinates = fitted_cluster_algo.cluster_centers_.tolist()
  num_clusters = len(cluster_coordinates)
  clusters_df[CLUSTER_CENTER_COORDINATES_COL_NAME] = clusters_df[CLUSTER_ID_COL_NAME].apply(lambda cluster_id: cluster_coordinates[cluster_id]) 
  clusters_df[TRANSFORMED_X_COL_NAME] = transformed_X.tolist()
  # Compute distances to cluster center
  clusters_df[EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME] = clusters_df.apply(lambda row: compute_euclid_dist(row[CLUSTER_CENTER_COORDINATES_COL_NAME], row[TRANSFORMED_X_COL_NAME]), axis = 1)
  for c in range(num_clusters):
    subsetted_df = clusters_df[clusters_df[CLUSTER_ID_COL_NAME] == c].copy(deep = True)
    cluster_df_list.append(subsetted_df)
  return cluster_df_list

def compute_cluster_tfidf_top_n_grams_list(
  cluster_df_list: pd.DataFrame,  
  tokens_col_name: str,
  k: int = 20, 
  tfidf_vect_options: Dict[str, Union[int, None, bool]] = DEFAULT_TFIDF_OPTIONS
) -> List[List[Tuple[Tuple[str, ...], float]]]:
  """Computes k top n-grams for each cluster in cluster_dfs_list by TFIDF score formed by the concatenation of all tokenized documents in each cluster, forming a document
      for the entire cluster, which using all cluster-level documents forms a cluster-level document corpus with which TF-IDF scores can be computed for the n-grams in each cluster to give
      a measure of the importance of an n-gram to a cluster

  Args:
    cluster_df_list: List of DataFrames where the index of the DataFrame corresponds to the cluster id, i.e. cluster_df_list[0] is the DataFrame associated with cluster ID 0. 
                        Each cluster DataFrame stores various important metadata about the cluster including the input text data which belongs to the cluster including 
                        the input text (column name: INPUT_COL_NAME), the tokens associated with the input text (column text: tokens_col_name) which is used to build the 
                        cluster-level document corpus
    tokens_col_name: Name of the column in each of the cluster_dfs_list DataFrames which has the tokens for each input document
    k: Number of top n-grams to show for each cluster in the returned top_tfidf_n_grams list. Default is 20
    tfidf_vect_options: Dictionary mapping the parameters of the TFIDFVectorizer to values used to instantiate the vectorizer used for computing
                          TFIDF scores for n-grams in cluster-level documents. Default is DEFAULT_TFIDF_OPTIONS
  
  Returns:
    tfidf_doc_list: Nested list, where each list contains tuples of the top k n-grams ordered by TFIDF score for that cluster. Each index corresponds to the cluster id, i.e.
                      tfidf_doc_list[0] is the list of top k n-grams for the cluster 0's document and tfidf_doc_list[0][0] is the tuple corresponding to the top n-gram for cluster 0's document
                      where tfidf_doc_list[0][0][0] is the n-gram tuple and tfidf_doc_list[0][0][1] is the actual TF-IDF score for that n-gram
  """
  num_clusters = len(cluster_df_list)
  tfidf_doc_list = []
  for c in range(num_clusters):
    cluster_tokens = []
    for tokenized_doc in cluster_df_list[c][tokens_col_name].tolist():
      tokenized_doc_list = tokenized_doc.tolist()
      cluster_tokens.extend(tokenized_doc_list)
    tfidf_doc_list.append(cluster_tokens)
  tfidf_vectorizer = TFIDFVectorizer(**tfidf_vect_options)
  cluster_tfidf_embeddings = tfidf_vectorizer.fit_transform(tfidf_doc_list)
  idx_to_n_gram = copy(tfidf_vectorizer.idx_to_n_gram)
  top_tfidf_n_grams = []
  for c in range(num_clusters):
    cluster_tfidf_embedding = cluster_tfidf_embeddings[c]
    top_tfidf_n_grams_cluster = get_top_k_tfidf_n_grams(cluster_tfidf_embedding, idx_to_n_gram, k = k)
    top_tfidf_n_grams.append(top_tfidf_n_grams_cluster)
  return top_tfidf_n_grams

def show_n_closest_data_points_to_cluster_center(
  cluster_df_list: List[pd.DataFrame], 
  n: int = 20, 
  translation_col_name: Optional[str] = None
) -> None:
  """For each cluster in cluster_df_list, shows n text inputs which were closest (by euclidean distance) to the cluster center.

  Args:
    cluster_df_list: List of DataFrames where the index of the DataFrame corresponds to the cluster id, i.e. cluster_df_list[0] is the DataFrame associated with cluster ID 0. 
                        Each cluster DataFrame stores various important metadata about the cluster including the input text data which belongs to the cluster including 
                        the input text (column name: INPUT_COL_NAME), and the translations corresponding to translations of the input text data 
                        (column name: translations_col_name) if provided
    n: Number of closest text inputs to show. Default is 20
    translation_col_name: Name of the column in each cluster DataFrame in cluster_df_list which stores machine-generated 
                            translations of the text inputs stored in INPUT_COL_NAME. Default is None
  """
  for cluster_id in range(len(cluster_df_list)):
    print(f"Cluster {cluster_id}")
    subsetted_df = cluster_df_list[cluster_id]
    num_data_points_in_cluster = len(subsetted_df)
    n_actual = min(n, num_data_points_in_cluster)
    print(f"  There are {num_data_points_in_cluster} data points in Cluster {cluster_id}")
    print(f"  Showing {n_actual} Closest Data Points to Cluster Center:")
    top_n_closest_data_points_df = subsetted_df.sort_values(EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME, kind = 'stable').head(n)
    i = 1
    for _, row in top_n_closest_data_points_df.iterrows():
      input_txt, euclid_dist = row[INPUT_COL_NAME], row[EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME]
      if i == 1:
        print(f"    {i}. Cluster Center, Euclid Distance from Cluster Center: {euclid_dist}")
      else:
        print(f"    {i}. Euclid Distance from Cluster Center: {euclid_dist}")
      print(f"      Original Input Text: {input_txt}")
      if translation_col_name:
        translation_txt = row[translation_col_name]
        print(f"      Translation Text: {translation_txt}")
      i += 1

def visualize_cluster_results(
    data_df: pd.DataFrame,
    embedding_dict: Dict[str, np.ndarray],
    tokens_col_name: str,
    X_options: Dict[str, str] = DEFAULT_EMBEDDINGS_OPTIONS,
    dim_red_options: Optional[Dict[str, Union[str, int]]] = None,
    cluster_options: Dict[str, Union[str, int]] = DEFAULT_CLUSTERING_OPTIONS,
    translations_col_name: Optional[str] = None,
    num_data_points_to_show: int = 20,
    seed: int = DEFAULT_SEED,
    path: Optional[str] = None,
    cluster_category_names: Optional[Dict[int, str]] = None
) -> Tuple[np.ndarray, List[pd.DataFrame]]:
  """Using a specified combination of hyperparameters for type of embedding which featurizes the data, dimensionality reduction technique (with specified number of components), 
      and clustering algorithm (with specified number of clusters), prints the num_data_points_to_show text inputs in data_df of the closest data points (by euclidean distance) to the center
      of each cluster and also the translations of the text inputs if translations_col_name is provided which is the name of the column in data_df which stores the translations.
      Also plots the clustering of the data points in 2D if the data is 2D or has been reduced to 2D (i.e. n_components == 2), labels the clusters using human-interpreted labels in the 
      cluster_category_names dictionary and and saves the plot at the path path

  Args:
    data_df: DataFrame containing input text data which corresponds to the embeddings in embedding_dict
    tokens_col_name: Name of column in data_df which contains the tokenized versions of the input text documents 
                      in the INPUT_COL_NAME column in data_df
    embedding_dict: Dictionary mapping types of embeddings to the corresponding matrices of embedded data, which is derived from the
                      the text inputs in the INPUT_COL_NAME column of data_df
    X_options: Dictionary with options for selecting an embedding of the data to use including the name 
                of the type of the embedding (key: EMBEDDING_TYPE_NAME). The value associated with the EMBEDDING_TYPE_NAME must be 
                a key in X_embeddings_dict. Default is DEFAULT_EMBEDDINGS_OPTIONS
    dim_red_options: Dictionary of options for configuring the dimensionality reduction algorithm including the name of the
                        algorithm (key: DIMENSIONALITY_REDUCTION_ALGORTIHM_NAME) to use and the number of 
                        components (key: NUM_COMPONENTS_NAME) to reduce the data embeddings to. 
                        Dimensionality reduction algorithm name must be a key in DIMENSIONALITY_REDUCTION_ALGORITHMS dictionary.
                        Defaults to None in which no dimensionality reduction is applied, and the selected embeddings are used as is
    cluster_options: Dictionary of options for configuring the clustering algorithm including the name
                        of the clustering algorithm (key: CLUSTERING_ALGORITHM_NAME) and the number of clusters
                        to find using the algorithm (key: NUM_CLUSTERS_NAME). The value associated with key
                        CLUSTERING_ALGORITHM_NAME must be a key in the CLUSTERING_ALGORITHMS dictionary.
                        Default is DEFAULT_CLUSTERING_OPTIONS
    translations_col_name: Column name of column in data_df which stores translations of the input text data in INPUT_COL_NAME column. 
                            Default is None, i.e. no translations provided
    num_data_points_to_show: Number of closest text inputs of closest data points to print. Default is 20
    seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Default is DEFAULT_SEED
    path: Path to .png filename on host's system the clustering plot will be saved as. Default is None
    cluster_category_names: Dictionary mapping interger cluster id to the human-interpreted label string to show on cluster plot. Default is None
  
  Returns:
    X_red: Data matrix of possibly reduced data which was clustered
    cluster_dfs_list: List of DataFrames where the index of the DataFrame corresponds to the cluster id, i.e. cluster_df_list[0] is the DataFrame associated with cluster ID 0. 
                        Each cluster DataFrame stores various important metadata about the cluster including the input text data which belongs to the cluster including 
                        the input text (column name: INPUT_COL_NAME), the tokens associated with the input text (column name: tokens_col_name) which is used to build the 
                        cluster-level document corpus, and translations of the input text (column name: translations_col_name) if provided, and the possibly reduced data points
                        that are a part of that cluster (column name: TRANSFORMED_X_COL_NAME)
  """
  embedding_type = X_options[EMBEDDING_TYPE_NAME]
  print(f"Embedding Type: {embedding_type}")
  print(f"cluster_options: {cluster_options}")
  print(f"dim_red_options: {dim_red_options}")
  selected_embedding = embedding_dict[embedding_type]
  X_red, fitted_cluster_algo = dim_red_and_cluster(
    selected_embedding,
    dim_red_options = dim_red_options,
    cluster_options = cluster_options,
    seed = seed
  )
  if X_red.shape[1] == 2:
    cluster_algo_name = cluster_options[CLUSTERING_ALGORITHM_NAME]
    if dim_red_options is not None:
      dim_red_algo_name, n_comps = dim_red_options[DIMENSIONALITY_REDUCTION_ALGORITHM_NAME], dim_red_options[NUM_COMPONENTS_NAME]
      if dim_red_algo_name == PCA_NAME:
        x_label, y_label = 'Principal Component 1', 'Principal Component 2'
      else:
        x_label, y_label = None, None
      title = f'{embedding_type} Features + {dim_red_algo_name} + {cluster_algo_name} Clustering'
    else:
      x_label, y_label = None, None
      title = f'{embedding_type} Features + {cluster_algo_name} Clustering'

    plot_clustering(
        X_red, 
        fitted_cluster_algo.labels_, 
        fitted_cluster_algo.cluster_centers_, 
        x_label = x_label, 
        y_label = y_label, 
        title = title, 
        path = path, 
        cluster_category_names = cluster_category_names)

  cluster_dfs_list = compute_cluster_dfs(
    X_red, 
    data_df, 
    fitted_cluster_algo,
    tokens_col_name,
    translations_col_name = translations_col_name
  )
  
  show_n_closest_data_points_to_cluster_center(cluster_dfs_list, n = num_data_points_to_show, translation_col_name = translations_col_name)

  return X_red, cluster_dfs_list

def save_cluster_dfs(
  cluster_dfs_list: List[pd.DataFrame],
  tokens_col_name: str,
  path: str,  
  num_data_points_to_keep: int = 20, 
  num_top_tfidf_n_grams: int = 20,
  tfidf_vect_options: Dict[str, Union[int, None, bool]] = DEFAULT_TFIDF_OPTIONS,
  translation_col_name: Optional[str] = None
) -> None:
  """Saves DataFrames with useful metadata about each cluster in cluster_dfs_list, including a DataFrame containing the closest num_data_points_to_keep text inputs to the cluster center
      of each cluster, the associated translations (if translation_col_name is provided), and the top ngrams for the cluster by TFIDF score. Also saves a DataFrame which contains 
      the top num_top_tfidf_n_grams n-grams with highest TF-IDF score as well as the score value for the document made from the concatenation of all tokenized documents in a cluster, 
      for each cluster in cluster_dfs_list

  Args:
    cluster_df_list: List of DataFrames where the index of the DataFrame corresponds to the cluster id, i.e. cluster_df_list[0] is the DataFrame associated with cluster ID 0. 
                        Each cluster DataFrame stores various important metadata about the cluster including the input text data which belongs to the cluster including 
                        the input text (column name: INPUT_COL_NAME), the tokenized versions of the input text (column name: tokens_col_name), and the translations corresponding 
                        to translations of the input text data (column name: translations_col_name) if provided
    tokens_col_name: Name of the column in each of the cluster_dfs_list DataFrames which has the tokens for each input document
    path: Path to the directory on host's filesystem where the cluster metadata DataFrames will be saved on the host's filesystem as CSVs
    num_data_points_to_keep: Number of text inputs associated with closest data points (by euclidean distance) to keep in the cluster metadata dataframe, for each cluster. 
                              Default is 20
    num_top_tfidf_n_grams: Number of n-grams with top TF-IDF scores for a cluster document to keep in the cluster-tfidf DataFrame. Default is 20
    tfidf_vect_options: Dictionary mapping the parameters of the TFIDFVectorizer to values used to instantiate the vectorizer used for computing
                          TFIDF scores for n-grams of cluster-level documents. Default is DEFAULT_TFIDF_OPTIONS. Default is DEFAULT_TFIDF_OPTIONS
    translation_col_name: Name of the column in each cluster DataFrame in cluster_df_list which stores machine-generated 
                            translations of the text inputs stored in the column named INPUT_COL_NAME in each cluster DataFrame. Default is None
  """
  num_clusters = len(cluster_dfs_list)
  top_tfidf_n_grams_list = compute_cluster_tfidf_top_n_grams_list(
    cluster_dfs_list, tokens_col_name, k = num_top_tfidf_n_grams, tfidf_vect_options = tfidf_vect_options
  )
  top_tfidf_n_grams_in_cluster = [[tfidf_tup[0] for tfidf_tup in cluster_list] for cluster_list in top_tfidf_n_grams_list]
  top_tfidf_vals_in_cluster = [[tfidf_tup[1] for tfidf_tup in cluster_list] for cluster_list in top_tfidf_n_grams_list]
  full_df_data, tfidf_df_data = {}, {}
  for c in range(num_clusters):
    cluster_df = cluster_dfs_list[c]
    cluster_df_sorted_by_dist = cluster_df.sort_values(EUCLIDEAN_DISTANCE_TO_CENTER_COL_NAME, kind = 'stable').head(num_data_points_to_keep)
    if translation_col_name:
      sorted_cluster_df = cluster_df_sorted_by_dist[[INPUT_COL_NAME, translation_col_name]]
      full_df_data[f"{INPUT_COL_NAME}.{c}"], full_df_data[f"{translation_col_name}.{c}"] = sorted_cluster_df[INPUT_COL_NAME].tolist(), sorted_cluster_df[translation_col_name].tolist()
    else:
      sorted_cluster_series = cluster_df_sorted_by_dist[INPUT_COL_NAME]
      full_df_data[f"{INPUT_COL_NAME}.{c}"] = sorted_cluster_series.tolist()
    full_df_data[f"{TOP_TFIDF_N_GRAMS_COL}.{c}"] = top_tfidf_n_grams_in_cluster[c]
    tfidf_df_data[f"Cluster {c} Top TFIDF N-Grams"] = top_tfidf_n_grams_in_cluster[c]
    tfidf_df_data[f"Cluster {c} Top TFIDF Values"] = top_tfidf_vals_in_cluster[c]
  full_df, tfidf_df = pd.DataFrame(full_df_data), pd.DataFrame(tfidf_df_data)
  full_df.to_csv(join(path, 'all_clusters.csv'), index = False, encoding = 'utf-8')
  tfidf_df.to_csv(join(path, 'tfidf_cluster.csv'), index = False, encoding = 'utf-8')
  
  