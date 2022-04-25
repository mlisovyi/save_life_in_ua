# %%
from pathlib import Path
import datetime as dt
import pandas as pd

import save_life_in_ua as sliu

# %%
file_data = Path("data/militarnyy_2022_tmp.xlsb")
# sliu.download_data(file_data)

# %%
df_in, df_out = sliu.read_data(file_data)

# %%
df_in = sliu.process_date(df_in)
df_out = sliu.process_date(df_out)

# %%
pd.set_option("max_colwidth", 200)
df_in[df_in["date"] >= dt.date(2022, 1, 1)].nlargest(20, columns="amount")

# %%
# aggregate and transform values into millions
df_in_date = sliu.get_daily_total(df_in)
df_out_date = sliu.get_daily_total(df_out)
# %%
sliu.plot_daily_inout(df_in_date, df_out_date)
sliu.plot_cum_daily_inout(df_in_date.cumsum(), df_out_date.cumsum())
# %%
s_final = sliu.process_type_of_expenses(df_out["type"])

sliu.plot_word_cloud_expenses(s_final)

# %%
