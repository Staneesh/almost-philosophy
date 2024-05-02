"""
`Almop` module is a collection of functions useful 
for analysing causal structures of time series data.
"""

import tomli


def parse_config(config_name: str):
    with open(config_name, mode="rb") as fp:
        return tomli.load(fp)
