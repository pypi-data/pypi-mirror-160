import numpy as np

from sklearn.metrics import *

from typing import Callable

def f2_func(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute F2 score (F-beta score where beta = 2) by comparing ground-truth array y_true
         against model predictions in y_pred
    
    Args:
        y_true: Ground-truth labels array
        y_pred: Model predictions array
    
    Returns:
        f2_score: Computed F2 score
    """
    f2_score = fbeta_score(y_true, y_pred, beta = 2)
    return f2_score

def make_scorer_from_func(metric_func: Callable) -> Callable:
    """Creates callable scorer using metric function, metric_func

    Args:
        metric_func: function which will be made into a scorer

    Returns:
        scorer: Scorer object using metric_func 
    """
    return make_scorer(metric_func)

def compute_aucpr(y_test: np.ndarray, pos_class_probs_or_decision_func_scores: np.ndarray) -> float:
    """Computes the Area Under the Precision-Recall Curve (AUCPR). We note that AUCPR is a good classification
        metric in the case of imbalanced datasets and covers all thresholds a classifier can take in making a
        prediction

    Note:
        This implementation is only compatible with binary classification

    Args:
        y_test: Ground-truth labels for the test data points
        pos_class_probs_or_decision_func_scores: The probabilities given to the positive class by the classifier
                                                    or the scores given by the decision function to the test data points
    
    Returns:
        aucpr_score: AUCPR score of the model on the test data
    """ 
    precision, recall, thresholds = precision_recall_curve(y_test, pos_class_probs_or_decision_func_scores)
    aucpr_score = auc(recall, precision)
    return aucpr_score