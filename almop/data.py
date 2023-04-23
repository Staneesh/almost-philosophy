"""
`Almop` data module is a collection of functions useful 
for obtaining and caching time series datasets.
"""

import eurostat as es


def get_hpi(only_these_country_codes: list = []):
    """
    Returns a DataFrame containing quarter-on-quarter
    changes (in percent) for (optionally) restricted
    list of country codes.
    """

    # Downloading House Price Index data
    hpi = es.get_data_df("PRC_HPI_Q")
    # Filter only if list of countries restricted by caller
    if not only_these_country_codes:
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
