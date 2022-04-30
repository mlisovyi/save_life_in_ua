import pandas as pd


def process_date(df: pd.DataFrame) -> pd.DataFrame:
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


def get_top_N_donations(df: pd.DataFrame) -> pd.DataFrame:
    col_m_uah = "amount, millions UAH"
    # the very first entry from 2021-12-31 is the aggregate over the last 8 years
    mask = df["date"] >= pd.to_datetime("2022-01-01")
    df_out = (
        df[mask]
        .nlargest(20, columns="amount")
        .reset_index(drop=True)
        .assign(**{col_m_uah: (lambda x: x["amount"] / 1e6)})[
            ["date", col_m_uah, "source"]
        ]
    )
    return df_out
