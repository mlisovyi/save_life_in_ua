# %%
from pathlib import Path

import pandas as pd

import save_life_in_ua as sliu

# %%
file_data = Path("data/militarnyy_2022_tmp.xlsb")
# sliu.download_data(file_data)

# %%
df_in, df_out = sliu.read_and_preprocess_data(file_data)

# %%
# Largest donations
pd.set_option("max_colwidth", 200)
sliu.get_top_N_donations(df_in)

# %%
# aggregate and transform values into millions
df_in_date = sliu.get_daily_total(df_in)
df_out_date = sliu.get_daily_total(df_out)

# %%
# plot daily sums
sliu.plot_daily_inout(
    df_in_date, df_out_date, date_start="2022-02-01", fout=Path("docs/figs/daily.png")
)
sliu.plot_cum_daily_inout(
    df_in_date,
    df_out_date,
    date_start="2022-02-01",
    fout=Path("docs/figs/daily_cum.png"),
)
# %%
# plot word counts in the
s_final = sliu.process_type_of_expenses(df_out["type"])

sliu.plot_word_cloud_expenses(s_final)
