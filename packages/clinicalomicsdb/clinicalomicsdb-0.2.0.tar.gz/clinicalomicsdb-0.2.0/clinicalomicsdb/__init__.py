#   Copyright 2022 Chang In Moon changin.moon@bcm.edu
__version__ = '0.2.0'

import io
import pandas as pd
from .database_download import download, get_dataset_link
from .file_download import download_text as _download_text
from .exceptions import BaseError, BaseWarning, InvalidParameterError, NoInternetError, OldPackageVersionWarning


def list_datasets():
    """List all available datasets."""

    dataset_list_url = "https://bcm.box.com/shared/static/v24wiuyy73rhv8jn44tyjbs0al8wa6oe.csv"

    try:
        dataset_list_text = _download_text(dataset_list_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None

    return pd.read_csv(io.StringIO(dataset_list_text), header=0)
