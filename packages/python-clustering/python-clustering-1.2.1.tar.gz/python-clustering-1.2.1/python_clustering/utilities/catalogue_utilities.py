# python3 utilities/catalogue_utilities.py

import os
import json
from pytablewriter import MarkdownTableWriter
from . import dataset_utilities


class Catalogue:
    def __init__(self):
        data = json.load(open("./jsons/catalogue_info.json"))
        self.PATH_TO_ALL_DATASETS_FOLDER = data["PATH_TO_ALL_DATASETS_FOLDER"]
        self.PATH_TO_LOCAL = data["PATH_TO_LOCAL"]
        self.PATH_TO_GITHUB = data["PATH_TO_GITHUB"]
        self.SUBFOLDERS = data["SUBFOLDERS"]
        self.COLUMN_NAMES = data["COLUMN_PROPERTY_NAMES"]
        self.ROOT_NAMES = data["ROOT_PROPERTY_NAMES"]

    def append(self, filename, subfolder):
        path = f"{self.PATH_TO_ALL_DATASETS_FOLDER}/{subfolder}"
        dataset = dataset_utilities.Dataset(filename, path=path)
        with open(f"{self.PATH_TO_ALL_DATASETS_FOLDER}/dataset_info.json", "r") as f:
            catalogue = json.load(f)
        catalogue[filename.split(".")[-2]] = self.arrange_calculated_data(
            dataset, subfolder=subfolder, filename=filename
        )
        self.create_markdown_table(catalogue)
        self.create_dataset_info(catalogue)

    def create(self):
        catalogue = {}
        for subfolder in self.SUBFOLDERS:
            path = f"{self.PATH_TO_ALL_DATASETS_FOLDER}/{subfolder}"
            for filename in os.listdir(path):
                dataset = dataset_utilities.Dataset(filename, path=path)
                catalogue[filename.split(".")[-2]] = self.arrange_calculated_data(
                    dataset, subfolder=subfolder, filename=filename
                )
        self.create_markdown_table(catalogue)
        self.create_dataset_info(catalogue)

    def create_dataset_info(self, catalogue):
        with open(
            f"{self.PATH_TO_ALL_DATASETS_FOLDER}/dataset_info.json", "w"
        ) as json_file:
            json.dump(catalogue, json_file)

    def create_markdown_table(self, data):
        value_matrix = [[]] * len(data)
        for idx_file, file in enumerate(data):
            row = [None] * len(self.COLUMN_NAMES)
            for idx_col, col in enumerate(self.COLUMN_NAMES):
                if col in data[file]:
                    row[idx_col] = data[file][col]
                else:
                    row[idx_col] = data[file]["stats"][col]
            value_matrix[idx_file] = row
        writer = MarkdownTableWriter(
            table_name="Dataset Description",
            headers=self.COLUMN_NAMES,
            value_matrix=value_matrix,
        )
        with open(f"{self.PATH_TO_ALL_DATASETS_FOLDER}/README.md", "w") as f:
            writer.stream = f
            writer.write_table()
            f.write("\n")
            f.write("* anomaly percentage were calculated using zscore")

    def arrange_calculated_data(self, dataset, subfolder, filename):
        dataset_dict = {"stats": {}}
        for key, value in self.collect_calculated_data(
            dataset, subfolder, filename
        ).items():
            if key in self.ROOT_NAMES:
                dataset_dict[key] = value
            else:
                dataset_dict["stats"][key] = value
        return dataset_dict

    def collect_calculated_data(self, dataset, subfolder, filename):
        return {
            "name": dataset.name,
            "origin": dataset.origin,
            "filetype": filename.split(".")[-1],
            "local_filepath": f"{self.PATH_TO_LOCAL}/{filename}",
            "github_filepath": f"{self.PATH_TO_GITHUB}/{subfolder}/{filename}",
            "description": str(dataset.description),
            "is_imbalanced": dataset.is_imbalanced,
            "number_of_clusters": dataset.number_of_clusters,
            "number_of_datapoint": dataset.number_of_datapoint,
            "number_of_dimensions": dataset.number_of_dimensions,
            "weak_outlier_proportion": dataset.weak_outlier_proportion,
            "strong_outlier_proportion": dataset.strong_outlier_proportion,
            "estimated_max_overlap": dataset.estimate_max_overlap,
            "estimated_mean_overlap": dataset.estimate_mean_overlap,
            "missing_values_proportion": dataset.missing_values_proportion,
        }


if __name__ == "__main__":
    catalogue = Catalogue()
    catalogue.create()
