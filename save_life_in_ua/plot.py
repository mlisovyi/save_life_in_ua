import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import datetime as dt


def add_y_grid_lines() -> None:
    plt.grid(which="major", axis="y", ls="--")


def add_war_start_line() -> None:
    plt.axvline(x=dt.date(2022, 2, 24), ls="--", c="k", label="Russia's invasion")


def plot_daily_inout(s_in: pd.Series, s_out: pd.Series) -> None:
    plt.figure(figsize=(12, 5))
    s_in.plot.line("-", marker=".", label="Income")
    s_out.plot.line("-", marker=".", label="Expenses")
    plt.xlabel("Date")
    plt.ylabel("Donations/Expenses per day, millions UAH")
    add_y_grid_lines()
    add_war_start_line()
    plt.legend()
    plt.tight_layout()


def plot_cum_daily_inout(s_in: pd.Series, s_out: pd.Series) -> None:
    _, axs = plt.subplots(
        2, 1, figsize=(12, 7), sharex="col", gridspec_kw={"height_ratios": [2.5, 1]}
    )
    # top figure with the cumulative distribution of donations and expenses
    plt.sca(axs[0])
    s_in.plot.line("-", marker=".", label="Income")
    s_out.plot.line("-", marker=".", label="Expenses")
    plt.xlabel("Date")
    plt.ylabel("Cumulative each day, millions UAH")
    add_y_grid_lines()
    add_war_start_line()
    plt.legend()
    # bottom figure with the savings
    plt.sca(axs[1])
    df_inout = pd.concat([s_in.rename("in"), s_out.rename("out")], axis=1)
    max_date = df_inout.idxmax().min()
    df_inout = df_inout[:max_date].fillna(method="ffill")
    s_diff = df_inout["in"] - df_inout["out"]
    s_diff.plot.line("-", marker=".", label="Savings", c="r")
    plt.xlabel("Date")
    plt.ylabel("Savings, millions UAH")
    add_y_grid_lines()
    add_war_start_line()
    plt.legend()
    plt.tight_layout()


def plot_word_cloud_expenses(df_expense_counts: pd.DataFrame) -> None:
    wc = WordCloud(width=600, height=400, collocations=False, background_color="white")
    wc = wc.generate_from_frequencies(df_expense_counts.value_counts().to_dict())
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
