import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
import os as os
import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))

def combine_dataframes():
    df_energyOut = energy_output()
    df_energyUse = energy_usage()
    df_energyExport = df_energyOut["Energy output [kWh]"] - df_energyUse["Energy usage [kWh]"]
    df_energyExport.name = "Energy export [kWh]"

    df_economicsSingle, df_economisMontly = economics(energy = np.array(df_energyExport))
    

    monthly_df = pd.concat([df_energyOut, df_energyUse, df_economisMontly, df_energyExport],axis=1)
    single_df = pd.concat([df_economicsSingle], axis=1)

    return monthly_df, single_df

def main():
    montly_df, single_df = combine_dataframes()
    df_name = os.path.join(dir_path, "output", f"total_df.csv")
    montly_df.to_csv(df_name)
    print(montly_df)
    print(single_df)


main()
