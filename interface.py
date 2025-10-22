import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
from modules.agriculture import agricultural
import os as os
import numpy as np
dir_path = os.path.dirname(os.path.realpath(__file__))

def interface(crop_type : str = "potatoes", 
              area : float  = 10000,
              latitude : float = 35,
              longitude  : float= 15,
              elevation : float = 10,
              height : float = 2.5,
              azimuth : float = 180, 
              tilt : float = 30, 
              row_width : float = 2*2.385,
              pitch : float = 8,
              panel_area : float = 1.7,
              rated_power : float = 440,
              lifetime : float = 30,
              ):
    """
    Description
    -----------
    Interface between the energy output, usage, agricultural and economical module.
    For the interconnections, see the figure.

    Parameters
    ----------
    crop_type : string
        Crop used
    area : float
        Area covered by the solar panels in m^2

    Returns
    -------
    monthly_df : pd.Dataframe
        Dataframe with all the monthly parameters:

    single_df : pd.Dataframe
        Dataframe with all the single-time parameters (that hold for the entire year or lifetime)

    Notes
    -----
    See overview.svg
    """

    df_energyOut = energy_output(latitude = latitude, 
                                longitude  = longitude,
                                elevation  = elevation,
                                height  = height,
                                azimuth  = azimuth,
                                tilt  = tilt,
                                row_width  = row_width,
                                pitch  = pitch,
                                area  = area,
                                panel_area  = panel_area,
                                rated_power  = rated_power,
                                )
    df_energyUse = energy_usage()
    df_energyOut["Energy export [kWh]"] = df_energyOut["Energy output [kWh]"] - df_energyUse["Energy usage [kWh]"]

    df_agricultural = agricultural(crop_type = crop_type, irradiation_crop= np.array(df_energyOut["Irradiation crops [kW/m^2]"]))
    df_economicsSingle = economics(area = area,
                                   coverage = 0.5,
                                   row_width = row_width,
                                   panel_area = panel_area,
                                   height_panel =  height,
                                   energy = df_energyOut["Energy export [kWh]"],
                                   subsidy = 0.0,
                                   lifetime = lifetime)
    
    monthly_df = pd.concat([df_energyOut, df_energyUse, df_agricultural], axis=1)
    single_df = pd.concat([df_economicsSingle], axis=1)

    return monthly_df, single_df

def main():
    montly_df, single_df = interface()
    df_name = os.path.join(dir_path, "output", f"total_df_monthly.csv")
    montly_df.to_csv(df_name)
    print(montly_df)
    df_name = os.path.join(dir_path, "output", f"total_df_onetime.csv")
    single_df.to_csv(df_name)
    print(single_df)


main()
