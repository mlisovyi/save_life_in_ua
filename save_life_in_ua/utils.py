from pathlib import Path
from typing import Tuple

import pandas as pd
import requests

URL = "https://onedrive.live.com/download?resid=B0264747CBB7E393!16208&ithint=file%2cxlsx&authkey=!AMSRszH4rLFy_dE"


def download_data(fout: Path) -> None:
    fout.parent.mkdir(exist_ok=True, parents=True)
    resp = requests.get(URL)
    with open(fout, "wb") as f:
        f.write(resp.content)
    print(f"Done downloading into {fout}")


def read_data(file_data: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
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
    # 25569 is a magic number from https://stackoverflow.com/a/34721924/9640384
    # direct usage of `origin` set in `pd.to_datetime` leads to a shift of 2 days
    ms2unix_shift_in_days = 25569
    sec_in_day = 24 * 60 * 60
    df["datetime"] = pd.to_datetime(
        (df["datetime"] - ms2unix_shift_in_days) * sec_in_day, unit="s"
    )
    # some entries contain not only the date, but also the exact time (fondy.eu)
    df["date"] = df["datetime"].dt.date
    del df["datetime"]
    return df


def get_daily_total(df: pd.DataFrame) -> pd.Series:
    df_date = df.groupby("date")["amount"].sum() / 1e6
    return df_date


def process_type_of_expenses(s: pd.Series) -> pd.DataFrame:
    pattern = r"(?<!\S)[^а-яА-Я\s]+(?!\S)"
    s_final = (
        s.str.replace("\n", "")
        .str.replace(pattern, "")
        .str.replace(r"\d*шт", "")
        .str.replace(",.", "")
        .str.strip()
    )
    return s_final


def get_term_counts(s: pd.Series) -> pd.Series:
    s_out = s.value_counts()
    return s_out
