"""The main script to read in data, process and dump the markdown report.
"""
# %%
from pathlib import Path

import pandas as pd

import save_life_in_ua as sliu

# %%
if __name__ == "__main__":
    # %%
    file_data = Path("data/militarnyy_2022.xlsb")
    # this will download the data
    sliu.download_data(file_data)

    # %%
    df_in, df_out = sliu.read_and_preprocess_data(file_data)

    # %%
    # Largest donations
    pd.set_option("max_colwidth", 200)
    df_top_n = sliu.get_top_N_donations(df_in)
    # df_top_n

    # %%
    # aggregate and transform values into millions
    df_in_date = sliu.get_daily_total(df_in)
    df_out_date = sliu.get_daily_total(df_out)

    # %%
    dir_out = Path("docs/figs/")
    # plot daily sums
    # generate plots and dump plotsthat will be picked up by the Markdown
    sliu.plot_daily_inout(
        df_in_date, df_out_date, date_start="2022-02-01", fout=dir_out / "daily.png"
    )
    sliu.plot_cum_daily_inout(
        df_in_date,
        df_out_date,
        date_start="2022-02-01",
        fout=dir_out / "daily_cum.png",
    )
    # %%
    # plot word counts in the
    s_final = sliu.process_type_of_expenses(df_out["type"])

    sliu.plot_word_cloud_expenses(s_final)

    # %%
    # generate the final markdown report
    sliu.generate_markdown(df_top_n)

# %%
