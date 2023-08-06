import numpy as np

from .constants import (
    DIMENSIONALITY_REDUCTION_ALGORITHM_NAME,
    NUM_COMPONENTS_NAME,
    DIMENSIONALITY_REDUCTION_ALGORITHMS,
    DEFAULT_SEED
)

from typing import Dict, Optional

def reduce_dims(
    full_dim_X: np.array,
    dim_red_options: Optional[Dict[str, str]] = None, 
    seed: int = DEFAULT_SEED
) -> np.ndarray:
  """Reduces dimensionality of full_dim_X using a dimensionality reduction algorithm, e.g. PCA w/ 2 components

  Args:
    full_dim_X: Original data matrix of shape (num. of data points, num. of features) to be reduced
    dim_red_options: Dictionary of options for configuring the dimensionality reduction algorithm including the name of the
                        algorithm (key: DIMENSIONALITY_REDUCTION_ALGORTIHM_NAME) to use and the number of 
                        components (key: NUM_COMPONENTS_NAME) to reduce full_dim_X to. 
                        Dimensionality reduction algorithm name must be a key in DIMENSIONALITY_REDUCTION_ALGORITHMS dictionary.
                        Defaults to None in which no dimensionality reduction is applied
    seed: Seed used by stochatic algorithms for enabling reproducibility of the experiment. Defaults to DEFAULT_SEED

  Returns:
    transformed_X: Reduced data if dim_red_options is not None, otherwise it's a copy of the original data, X.
  """
  X = full_dim_X.copy()
  if dim_red_options is not None:
    assert DIMENSIONALITY_REDUCTION_ALGORITHM_NAME in dim_red_options
    assert NUM_COMPONENTS_NAME in dim_red_options
    dim_red_algo_name, n_components = dim_red_options[DIMENSIONALITY_REDUCTION_ALGORITHM_NAME], dim_red_options[NUM_COMPONENTS_NAME]
    assert n_components >= 1
    dim_red_algo = DIMENSIONALITY_REDUCTION_ALGORITHMS[dim_red_algo_name]
    transformed_X = dim_red_algo(n_components = n_components, random_state = seed).fit_transform(X)
  else:
    transformed_X = X
  return transformed_X