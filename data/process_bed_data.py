from pathlib import Path

import numpy as np
import pandas as pd

_BED_DATA_PATH = Path(__file__).parent / "world_bank_bed_data.csv"


def _get_latest_bed_estimate(row):
    non_empty_estimates = [float(x) for x in row.values if float(x) > 0]
    try:
        return non_empty_estimates[-1]
    except IndexError:
        return np.nan


def preprocess_bed_data(path=_BED_DATA_PATH):
    df = pd.read_csv(path, header=2)
    df.rename({"Country Name": "Country/Region"}, axis=1, inplace=True)
    df.drop(["Country Code", "Indicator Name", "Indicator Code"], axis=1, inplace=True)
    df.set_index("Country/Region", inplace=True)
    df["Latest Bed Estimate"] = df.apply(_get_latest_bed_estimate, axis=1)

    # Rename countries to match demographics and disease data
    df = df.rename(index={
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "Korea, South",
        "Russian Federation": "Russia",
        "Egypt, Arab Rep.": "Egypt",
        "Slovak Republic": "Slovakia",
        "Congo, Dem. Rep.": "Congo (Kinshasa)",
        # "Brunei Darussalam": "Brunei",
    })

    return df
