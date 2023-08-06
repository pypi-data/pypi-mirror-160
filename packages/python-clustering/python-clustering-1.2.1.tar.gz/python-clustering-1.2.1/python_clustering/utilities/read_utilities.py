from typing import List
import arff
import os
from scipy.io import arff as scipy_arff
import json
import pandas as pd
import requests
from . import preprocessing_utilities


def read_arff(filepath: str, mode: str = "scipy_arff"):
    """
    Reading aiff format.
    By default scipy.io arff reader is used (mode: scipy_arff).

    Args:
        filepath - str: full path to aiff file
        mode - str: scipy_arff | arff

    Return:
        arff reade format
    """
    if mode == "scipy_arff":
        return scipy_arff.loadarff(filepath)
    elif mode == "arff":
        return arff.load(open(filepath, "r"))
    return None


def get_root_folder() -> str:
    """
    Get root folder

    Return:
        os.path: root folder
    """
    return os.path.dirname(os.path.dirname(__file__))


def get_dataset_info(name: str):
    """
    Get information regarding particular {name} dataset

    Args:
        name: str

    Return:
        dict or None: specified dict by name from dataset_info.json
    """
    data = load_dataset_info()
    if name in data:
        return data[name]
    else:
        print(
            f"Dataset {name} not present in the local catalogue. To update catalogue, run update_local_info()"
        )
        return None


def load_catalogue_info(root_folder: str = None) -> dict:
    """
    Loading content of catalogue_info.json.
    Contains information regarding datasets paths and configs

    Args:
        root_folder:str - root folder

    Return:
        dict: catalogue_info.json content
    """
    if not root_folder:
        root_folder = get_root_folder()
    return json.load(open(f"{root_folder}/jsons/catalogue_info.json"))


def load_dataset_info(root_folder: str = None) -> dict:
    """
    Loading content of dataset_info.json.
    Contains information regarding datasets paths and configs

    Args:
        root_folder:str - root folder

    Return:
        dict: dataset_info.json content
    """
    if not root_folder:
        root_folder = get_root_folder()
    return json.load(open(f"{root_folder}/jsons/dataset_info.json"))


def load_description(name: str, path: str = "") -> str or None:
    """
    Loading dataset decsription by name

    Args:
        name : str - dataset name

    Return:
        description: str or None - cluster dataset in pandas Dataframe.
        None if file isn't found in dataset folder.

    Errors:
        NotImplementedError - if some functionality isn't implemented in scipy.io arff method
        FileNotFoundError - dataset file isn't present
    """
    if not path:
        root_folder = get_root_folder()
        dataset_info = get_dataset_info(name)
        path = f'{root_folder}/{dataset_info["local_filepath"]}'
    try:
        data = read_arff(f"{path}")
        description = pd.DataFrame(data[1])
    except NotImplementedError:
        data = read_arff(f"{path}", mode="arff")
        description = pd.DataFrame(data["description"])
    except FileNotFoundError:
        print(
            f"Dataset {name} not present in the local catalogue. To update catalogue, run update_local_info()"
        )
        return None
    return description


def load(name: str, path: str = "") -> pd.DataFrame or None:
    """
    Loading dataset by name

    Args:
        name : str - dataset name

    Return:
        df: pd.DataFrame or None - cluster dataset in pandas Dataframe.
        None if file isn't found in dataset folder.

    Errors:
        NotImplementedError - if some functionality isn't implemented in scipy.io arff method
        FileNotFoundError - dataset file isn't present
    """
    if not path:
        root_folder = get_root_folder()
        dataset_info = get_dataset_info(name)
        path = f'{root_folder}/{dataset_info["local_filepath"]}'
    try:
        data = read_arff(f"{path}")
        df = pd.DataFrame(data[0])
        df.columns = df.columns.str.lower()
    except NotImplementedError:
        data = read_arff(f"{path}", mode="arff")
        df = pd.DataFrame(
            data["data"], columns=[x[0].lower() for x in data["attributes"]]
        )
    except FileNotFoundError:
        print(
            f"Dataset {name} not present in the local catalogue. To update catalogue, run update_local_info()"
        )
        return None
    df = preprocessing_utilities.preprocessing(df)
    return df


def download(datasets: str or List[str], overwrite: bool = False):
    """
    Download dataset from github repo.

    Args:
        datasets: str or List[str] - one or single dataset names
        overwrite: bool - overwrite if dataset is present
    """
    if isinstance(datasets, str):
        datasets = [datasets]
    status_datasets = {
        "Dataset_not_found_in_catalogue": [],
        "Download_success": [],
        "Filepath_not_valid": [],
    }
    root_folder = get_root_folder()
    dataset_info = load_dataset_info(root_folder)
    for dataset in datasets:
        if dataset not in dataset_info:
            status_datasets["Dataset_not_found_in_catalogue"].append(dataset)
        else:
            github_path = dataset_info[dataset]["github_filepath"]
            r = requests.get(github_path, allow_redirects=True)
            if r.status_code != 200:
                status_datasets["Filepath_not_valid"].append(dataset)
            open(
                f'{root_folder}/datasets/{dataset_info[dataset]["name"]}.{dataset_info[dataset]["filetype"]}',
                "w",
            ).write(r.text)
            status_datasets["Download_success"].append(dataset)

    for status in status_datasets:
        if status_datasets[status]:
            print(f"{status}: {status_datasets[status]}")


def list_local_datasets() -> List:
    """
    Listing all available datasets locally.

    Return:
        filename: List - list of all locally avaliable datasets
    """
    root_folder = get_root_folder()
    catalogue_info = load_catalogue_info(root_folder)
    dataset_info = load_dataset_info(root_folder)
    local_filepath_dict = {
        dataset_info[filename]["local_filepath"]: filename for filename in dataset_info
    }
    filenames = [
        local_filepath_dict[f'{catalogue_info["PATH_TO_LOCAL"]}/{x}']
        if f'{catalogue_info["PATH_TO_LOCAL"]}/{x}' in local_filepath_dict
        else x
        for x in os.listdir(f'{root_folder}/{catalogue_info["PATH_TO_LOCAL"]}')
    ]
    return filenames


def update_local_jsons():
    root_folder = get_root_folder()
    catalogue_info = load_catalogue_info()
    github_path = catalogue_info["PATH_TO_GITHUB"]
    for file in ["catalogue_info.json", "dataset_info.json"]:
        r = requests.get(f"{github_path}/{file}", allow_redirects=True)
        if r.status_code == 200:
            with open(f"{root_folder}/jsons/{file}", "w") as outfile:
                json.dump(r.json(), outfile)
            print(f"{file} successfully updated")
        else:
            print(f"{file} wasn't updated")


if __name__ == "__main__":
    pass
