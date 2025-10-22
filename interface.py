import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
from modules.agriculture import agricultural
import os as os
import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))

def combine_dataframes(crop_type = "potatoes"):
    df_energyOut = energy_output()
    df_energyUse = energy_usage()
    df_energyOut["Energy export [kWh]"] = df_energyOut["Energy output [kWh]"] - df_energyUse["Energy usage [kWh]"]

    df_agricultural = agricultural(crop_type = crop_type, irradiation_crop= np.array(df_energyOut["Irradiation crops [kWh/m^2]"]))
    df_economicsSingle = economics(area=10000,
                                   coverage =0.5,
                                   rows =10,
                                   length_rows =1000,
                                   height_panel = 2,
                                   energy = np.linspace(5,20,12),
                                   subsidy=0.0,
                                   lifetime = 30):
    

    monthly_df = pd.concat([df_energyOut, df_energyUse, df_agricultural], axis=1)
    single_df = pd.concat([df_economicsSingle], axis=1)

    return monthly_df, single_df

def main():
    montly_df, single_df = combine_dataframes()
    df_name = os.path.join(dir_path, "output", f"total_df.csv")
    montly_df.to_csv(df_name)
    print(montly_df)
    print(single_df)


main()
