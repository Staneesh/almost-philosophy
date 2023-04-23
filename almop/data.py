"""
`Almop` data module is a collection of functions useful 
for obtaining and caching time series datasets.
"""

import eurostat as es
import pandas as pd
import os
import logging
from enum import Enum
import pathlib


class SourceType(Enum):
    EUROSTAT = 1


def dataset_persist_dir_full(config: dict):
    persist_dir: str = config["dataset_persist_dir"]
    if persist_dir.endswith("/"):
        persist_dir = persist_dir[:-1]
    return f"{persist_dir}/almop_datasets"


def load_dataset(config: dict, source: SourceType, dataset_name: str):
    dataset_subdir = (
        f"{dataset_persist_dir_full(config)}/{source.name.lower()}/{dataset_name}/"
    )
    dataset_path = f"{dataset_subdir}/data.csv"

    if os.path.exists(dataset_path):
        try:
            data = pd.read_csv()
            if data:
                return data
        except:
            pass  # Do nothing if loading from file failed. We will not early-return and the dataset will be loaded later.
    else:
        logging.info(
            f"Directory for persisting {dataset_name} not found. Creating {dataset_subdir}..."
        )
        pathlib.Path(dataset_subdir).mkdir(parents=True, exist_ok=True)

    # At this point the directory for data is surely created and the dataset needs
    # to be re-loaded either because it's not there at all or `pandas` is unable to read it.
    data = es.get_data_df(dataset_name)  # This can throw!
    data.to_csv(dataset_path)
    return data


def get_hpi(config: dict, only_these_country_codes: list = []):
    """
    Returns a DataFrame containing quarter-on-quarter
    changes (in percent) for (optionally) restricted
    list of country codes.
    """

    # Downloading House Price Index data
    hpi = load_dataset(
        config=config, source=SourceType.EUROSTAT, dataset_name="PRC_HPI_Q"
    )
    # Filter only if list of countries restricted by caller
    if only_these_country_codes:
        hpi = hpi.loc[hpi["geo\TIME_PERIOD"].isin(only_these_country_codes)]
    # Consider relative QoQ change only
    hpi = hpi.loc[hpi["unit"] == "RCH_Q"]
    # Consider total purchases only
    hpi = hpi.loc[hpi["purchase"] == "TOTAL"]
    # Remove unnecessary columns after filtering for specific values
    hpi = hpi.iloc[:, 3:]
    # Change a bogus column name to a more meaningful one
    hpi = hpi.rename(columns={hpi.columns[0]: "country"})
    # `country` should be a primary key & data transposed to have a row per time point
    hpi = hpi.set_index("country", drop=True).T

    return hpi
