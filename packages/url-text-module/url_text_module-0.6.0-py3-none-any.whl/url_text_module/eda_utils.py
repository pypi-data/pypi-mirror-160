from scipy.stats import skew
from pandas import Series

def compute_distribution_skew(data_series: Series) -> float:
    """Computes skew of a data distribution

    Args:
      data_series: Series of data for which its distribution's skew is computed
    
    Returns:
      skew: float denoting skew of the data_series distribution. A positive value indicates right-skewedness
        and a negative value is left-skewedness.
    """
    return skew(data_series)