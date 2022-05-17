import datetime as dt
from pathlib import Path

import pandas as pd


def get_daily_total(df: pd.DataFrame) -> pd.Series:
    df_date = df.groupby("date")["amount"].sum() / 1e6
    return df_date


def process_type_of_expenses(s: pd.Series) -> pd.DataFrame:
    pattern = r"(?<!\S)[^а-яА-Я\s]+(?!\S)"
    s_final = (
        s.str.replace("\n", "", regex=False)
        .str.replace(pattern, "", regex=True)
        .str.replace(r"\d*шт", "", regex=True)
        .str.replace(",.", "", regex=False)
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


def generate_markdown(df_full_n: pd.DataFrame) -> None:
    template_md = Path("docs/README.template")
    out_md = template_md.parent / f"{template_md.stem}.md"
    with open(str(template_md), "r") as template_file:
        template = template_file.read()
        df_out = df_full_n.assign(date=df_full_n["date"].dt.date)
        docs = template.format(
            LARGEST_DONATIONS=df_out.to_markdown(floatfmt=".2f", tablefmt="github"),
            DATE=dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        )
    with open(str(out_md), "w") as out_file:
        out_file.write(docs)
