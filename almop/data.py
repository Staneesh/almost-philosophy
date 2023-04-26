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
    """Supported data source types"""

    EUROSTAT = 1


def dataset_persist_dir_full(config: dict):
    """Get the path to the directory where `almop` stores datasets."""
    persist_dir: str = config["dataset_persist_dir"]
    if persist_dir.endswith("/"):
        persist_dir = persist_dir[:-1]
    return f"{persist_dir}/almop_datasets"


def load_dataset(
    config: dict, source: SourceType, dataset_name: str, no_persist: bool = False
):
    """
    Loads a dataset from a given source from the internet and persists it to disk.

    Expects that `config` has `dataset_persist_dir` key which is pointing to a proper path on disk.
    `no_persist` flag should be used for unit testing purposes only.
    """

    dataset_subdir = (
        f"{dataset_persist_dir_full(config)}/{source.name.lower()}/{dataset_name}"
    )
    dataset_path = f"{dataset_subdir}/data.csv"
    dataset_source_name = f"'{source.name.lower()}/{dataset_name}'"

    if os.path.exists(dataset_path):
        try:
            data = pd.read_csv(dataset_path, index_col=0)
            if not data.empty:
                logging.info(f"Successfully loaded {dataset_source_name} from disk.")
                return data
        except:
            pass  # Do nothing if loading from file failed. We will not early-return and the dataset will be loaded later.
    else:
        logging.info(
            f"Directory for persisting '{dataset_name}' not found. Creating '{dataset_subdir}'..."
        )
        if not no_persist:
            pathlib.Path(dataset_subdir).mkdir(parents=True, exist_ok=True)

    # At this point the directory for data is surely created and the dataset needs
    # to be re-loaded either because it's not there at all or `pandas` is unable to read it.
    logging.info(f"Pulling {dataset_source_name} from the internet...")
    if source == SourceType.EUROSTAT:
        data = es.get_data_df(dataset_name)  # This can throw!
        if data.empty:
            raise ValueError(f"Could not load {dataset_source_name} dataset.")
    else:
        raise ValueError(f"Data source {source} is not supported!")

    logging.info(f"Pulling {dataset_source_name} complete.")
    if not no_persist:
        data.to_csv(dataset_path, index=False)
        logging.info(f"Persisted {dataset_source_name} dataset.")
    return data


def get_hpi(
    config: dict, only_these_country_codes: list = [], no_persist: bool = False
):
    """
    Returns a DataFrame containing quarter-on-quarter
    changes (in percent) for (optionally) restricted
    list of country codes.

    `no_persist` should be used for unit testing purposes only.
    """

    # Downloading House Price Index data
    hpi = load_dataset(
        config=config,
        source=SourceType.EUROSTAT,
        dataset_name="PRC_HPI_Q",
        no_persist=no_persist,
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


def get_gdp(
    config: dict, only_these_country_codes: list = [], no_persist: bool = False
):
    """
    Returns a DataFrame containing quarter-on-quarter
    changes (in percent) for (optionally) restricted
    list of country codes.

    `no_persist` should be used for unit testing purposes only.
    """

    # Downloading House Price Index data
    gdp = load_dataset(
        config=config,
        source=SourceType.EUROSTAT,
        dataset_name="NAMQ_10_GDP",
        no_persist=no_persist,
    )

    # Filter only if list of countries restricted by caller
    if only_these_country_codes:
        gdp = gdp.loc[gdp["geo\TIME_PERIOD"].isin(only_these_country_codes)]

    gdp = gdp.loc[gdp["unit"] == "CP_MEUR"]  # Millions of Euro
    gdp = gdp.loc[gdp["s_adj"] == "SCA"]  # Seasonally and calendar adjusted
    gdp = gdp.loc[gdp["na_item"] == "B1GQ"]  # GDP at market price

    # Remove unnecessary columns after filtering for specific values
    gdp = gdp.iloc[:, 3:]
    # Change a bogus column name to a more meaningful one
    gdp = gdp.rename(columns={gdp.columns[0]: "country"})
    # `country` should be a primary key & data transposed to have a row per time point
    gdp = gdp.set_index("country", drop=True).T

    return gdp


def get_infl(
    config: dict, only_these_country_codes: list = [], no_persist: bool = False
):
    """
    TODO
    `no_persist` should be used for unit testing purposes only.
    """

    # Downloading House Price Index data
    infl = load_dataset(
        config=config,
        source=SourceType.EUROSTAT,
        dataset_name="EI_CPHI_M",
        no_persist=no_persist,
    )

    # Filter only if list of countries restricted by caller
    if only_these_country_codes:
        infl = infl.loc[infl["geo\TIME_PERIOD"].isin(only_these_country_codes)]

    infl = infl.loc[infl["unit"] == "RT12"]  # TODO
    infl = infl.loc[infl["s_adj"] == "NSA"]  # Not Seasonally Adjusted (NSA)
    infl = infl.loc[infl["indic"] == "CP-HI00"]  # TODO

    # Remove unnecessary columns after filtering for specific values
    infl = infl.iloc[:, 3:]
    # Change a bogus column name to a more meaningful one
    infl = infl.rename(columns={infl.columns[0]: "country"})
    # `country` should be a primary key & data transposed to have a row per time point
    infl = infl.set_index("country", drop=True).T

    return infl
