from pathlib import Path
from typing import Tuple

import pandas as pd
import requests

# specific download URL for the financial report of the fund
URL = "https://onedrive.live.com/download?resid=B0264747CBB7E393!16208&ithint=file%2cxlsx&authkey=!AMSRszH4rLFy_dE"


def download_data(fout: Path) -> None:
    """The function to download the original data as a file locally on disc.

    Args:
        fout (Path): the file to dump the data into
    """
    fout.parent.mkdir(exist_ok=True, parents=True)
    resp = requests.get(URL)
    with open(fout, "wb") as f:
        f.write(resp.content)
    print(f"Done downloading into {fout}")


def read_data(file_data: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Read in the input file and output the data on donations and expenses

    Args:
        file_data (Path): the file to read

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: the data on donations and expenses (respectively)
    """
    df_in = pd.read_excel(
        file_data,
        sheet_name="Надходження",
        usecols="A:D",
        names=["datetime", "amount", "type", "source"],
        engine="pyxlsb",
    )
    df_out = pd.read_excel(
        file_data,
        sheet_name="Витрати",
        usecols="A:D",
        names=["datetime", "type", "amount", "source"],
        engine="pyxlsb",
    )
    return df_in, df_out


def process_date(df: pd.DataFrame) -> pd.DataFrame:
    """Do pre-processing of the raw data.

    In particular:

    - convert the timestamp from the binary Excel representation into the pandas datetime
    - extract separately the date of the transaction

    Args:
        df (pd.DataFrame): the data on donations or expenses

    Returns:
        pd.DataFrame: processed data
    """
    # 25569 is a magic number from https://stackoverflow.com/a/34721924/9640384
    # direct usage of `origin` set in `pd.to_datetime` leads to a shift of 2 days
    ms2unix_shift_in_days = 25569
    sec_in_day = 24 * 60 * 60
    df["datetime"] = pd.to_datetime(
        (df["datetime"] - ms2unix_shift_in_days) * sec_in_day, unit="s"
    )
    # some entries contain not only the date, but also the exact time (fondy.eu)
    df["date"] = df["datetime"].dt.floor("D")
    del df["datetime"]
    return df


def read_and_preprocess_data(file_data: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """A wrapper to read in and process the data

    Args:
        file_data (Path): the file to read

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: preprocessed data on donations and expenses (respectively)
    """
    df_in, df_out = read_data(file_data)

    df_in = process_date(df_in)
    df_out = process_date(df_out)

    max_date_in = df_in["date"].max().strftime("%Y/%m/%d")
    max_date_out = df_out["date"].max().strftime("%Y/%m/%d")
    print(f"Latest date in the data: {max_date_in=}, {max_date_out=}")

    return df_in, df_out
