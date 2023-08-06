from typing import NamedTuple, Union, Dict, List

class Featurization(NamedTuple):
    """Featurization used for input data

    Attributes:
        type: Type of featurization, e.g. BERT. Note: Must be in FEATURIZATIONS_SET
        named_parameters: Named parameters of the vectorizer corresponding to the featurization type
        metadata: Metadata dictionary corresponding to the type of preprocessing or model used for constructing the
                embeddings associated with the featurization
    """
    type: str
    named_parameters: Union[Dict[str, Union[int, bool, None]], None]
    metadata: Union[Dict[str, str], Dict[str, Union[bool, str, Dict[str, str]]]]

class AlgorithmMetadata(NamedTuple):
    """Metadata associated with an Algorithm, specifically when used in Nested Cross Validation or Cross Validation

    Attributes:
        name: Name of the algorithm. Note: Must be key in ALGO_DICT
        hyperparameters_grid: List of hyperparameters and associated lists of values to use in the search optimization procedure (e.g. Grid Search)
        featurization_grid: List of featurizations to use on the input to the algorithm during the search optimization procedure. Note: 
                                is considered a part of the hyperparameter search space, or grid when performing a search optimization procedure
        normalizer_type: Type of normalization to apply to the input featurization prior to being inputted to the algorithm. Must be key in NORMALIZER_DICT
    """
    name: str
    hyperparameters_grid: List[Dict[str, List[Union[str, float, int, bool, None]]]]
    featurization_grid: List[Featurization]
    normalizer_type: str

class ModelMetadata(NamedTuple):
    """Metadata associated with a fitted model

    Attributes:
        name: Name of the model
        fitted_model: Fitted model
        class_to_idx: Dictionary mapping string class name to idx
        hyperparameters: Dictionary mapping the names of various hyperparameters to the values used to fit the model
        featurization: Featurization applied to the input to the model
        normalizer_type: Type of normalization to apply to the input featurization prior to being inputted to the model. Must be key in NORMALIZER_DICT
        seed: Random seed used when fitting the model, to enable reproducibility
    """
    name: str
    fitted_model: object
    class_to_idx: Dict[str, int]
    hyperparameters: Dict[str, Union[str, float, int, bool, None]]
    featurization: Featurization
    normalizer_type: str
    seed: int


