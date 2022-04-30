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
