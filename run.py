import re

import pandas as pd


def get_length(x):
    return len(x)


df = pd.read_csv("order_num.csv")
df = df[["Instrument_ID", "max_limit_orders"]]
df["symbol_type"] = df["Instrument_ID"].apply(
    lambda x: re.search("\D+", x).group(0))
df = df[~df["Instrument_ID"].str.contains("EFP")]
df = df[~df["Instrument_ID"].str.contains("efp")]
df = df[~df["Instrument_ID"].str.contains("-P-")]
df = df[~df["Instrument_ID"].str.contains("-C-")]
df["Instrument_ID_length"] = df["Instrument_ID"].apply(get_length)
df = df[df["Instrument_ID_length"] < 8]
all_symbols = set(df["symbol_type"])
mapping_dict = {}
for symbol in all_symbols:
    max_v = max(
        df.loc[df["symbol_type"] == symbol, "max_limit_orders"])
    min_v = min(
        df.loc[df["symbol_type"] == symbol, "max_limit_orders"])
    print("symbol%s max %s min %s diff %s" %
          (symbol, max_v, min_v, max_v - min_v))
    mapping_dict[symbol] = max_v
print(mapping_dict)
