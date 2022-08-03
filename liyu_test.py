import pandas as pd
data = pd.read_csv("electricity_hourly_dataset.ts", sep=";", index_col=0, parse_dates=True, decimal=",")
    # data: pd.DataFrame = data.resample("1H", label="left", closed="right").sum()
data.fillna(0, inplace=True)
data = data.melt(var_name="custom", value_name="elec_load", ignore_index=False)
data.reset_index(inplace=True)
data.rename(columns={"index": "datetime"}, inplace=True)

# remove starting zero for each group, since it no meaning for the model
start_idx = (pd.concat((data["custom"], data["elec_load"] != 0), axis=1)
        .groupby(["custom"])
        .transform("idxmax")["elec_load"])
end_idx = (pd.concat((data["custom"], data.index.to_frame(name="end_idx")), axis=1)
        .groupby(["custom"])
        .transform("nth", -1)["end_idx"]
    )
data = data[(data.index <= end_idx) & (data.index >= start_idx)].reset_index(drop=True)
print(data)