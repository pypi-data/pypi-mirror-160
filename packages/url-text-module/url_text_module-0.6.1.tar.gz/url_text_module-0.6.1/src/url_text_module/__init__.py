"""
:mod: `url_text_module` is a package used for preprocessing crisis text data and applying
various classification & clustering algorithms on that data.
"""

from .constants import *
from .eda_utils import *
from .preprocessing_utils import *
from .vectorizer_utils import *
from .dimensionality_reduction import *
from .clustering import *
from .classification import *
from .classes import *
from .plotting_utils import *
from .metric_utils import *
from .misc_utils import *

print(f'Using Version {get_version()} of URL Text Module')

del constants
del eda_utils
del preprocessing_utils
del vectorizer_utils
del dimensionality_reduction
del clustering
del classification
del classes
del plotting_utils
del metric_utils
del misc_utils
