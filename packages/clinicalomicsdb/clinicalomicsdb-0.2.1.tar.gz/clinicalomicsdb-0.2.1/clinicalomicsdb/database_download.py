# Copyright 2022 Chang In Moon changin.moon@bcm.edu
# will implement a better structure for downloading data in future versions...
# we want to try import a csv file that contains each study name and it's box link
import io
import pandas as pd
from .file_download import download_text as _download_text #add .
from .exceptions import BaseError, BaseWarning, InvalidParameterError, NoInternetError, OldPackageVersionWarning #add .

def get_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/1rs6wid9em7tewjpqchnar4wlr75l3ml.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def download(input):
    input = input.upper()
    data_link = get_dataset_link()
    target = data_link.loc[data_link['Series'] == input]
    url = target.iloc[0,1]
    try:
        dataset_text = _download_text(url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_text), header=0)

def get_patient_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/yt0ldc2nptxn96ovnna3hjxtlntzfvig.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)


def download_patient_data(input):
    input = input.upper()
    data_link = get_patient_dataset_link()
    target = data_link.loc[data_link['Series'] == input]
    url = target.iloc[0,1]
    try:
        dataset_text = _download_text(url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_text), header=0)