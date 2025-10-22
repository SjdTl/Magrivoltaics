import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
from modules.agriculture import agricultural
import os as os
import matplotlib.pyplot as plt
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
    latitude : float
        Latitude of the farm
    longitude : float
        Longitude of the farm
    elevation : float 
        Elevation of the farm
    height : float
        Height of the panels above the crops [m]
    azimuth : float
        Azimuth in degrees [deg]
    tilt : float 
        Angle in degrees [deg]
    row width : float
        Width of each row of panels [m]
    area : float
        Area in m2 [m^2]
    rated_power : float
        Rated power of the panels in Watt [W]
    panel_area : float
        Area of a single panel [m^2]
    lifetime : float 
        Lifetime of the system in years

    Returns
    -------
    monthly_df : pd.Dataframe
        Dataframe with all the monthly parameters:
        | Month    | Energy Output [kWh] | Irradiation Panels [kW/m^2] | Irradiation Crops [kW/m^2] | Energy Export [kWh] | Energy Usage [kWh] | Crop Impact [kW/m^2] |
        | -------- | ------------------- | --------------------------- | -------------------------- | ------------------- | ------------------ | -------------------- |
        | January  | 237886.351620       | 0.221792                    | 0.090966                   | 237886.351620       | 0                  | -0.017534            |
        | February | 259009.630191       | 0.260392                    | 0.109855                   | 259009.630191       | 0                  | 0.000000             |

    single_df : pd.Dataframe
        Dataframe with all the single-time parameters (that hold for the entire year or lifetime)
        |   | LCOE [EUR/MWh] | ROI      | Operation & Maintenance cost [EUR/y] | Energy price [EUR/kWh] |
        | - | -------------- | -------- | ------------------------------------ | ---------------------- |
        | 0 | 69.944184      | 5.556185 | 71199.264706                         | 0.1301                 |

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

    df_agricultural = agricultural(crop_type = crop_type, 
                                   irradiation_crop= np.array(df_energyOut["Irradiation crops [kW/m^2]"]))
    
    df_economicsSingle = economics(area = area,
                                   coverage = row_width/pitch,
                                   panel_area = panel_area,
                                   energy = df_energyOut["Energy export [kWh]"],
                                   subsidy = 0.0,
                                   lifetime = lifetime)
    
    monthly_df = pd.concat([df_energyOut, df_energyUse, df_agricultural], axis=1)
    single_df = pd.concat([df_economicsSingle], axis=1)

    return monthly_df, single_df

def vary_energy_output():
    areas = np.linspace(10,1e7, 10)
    monthly_dfs = []
    single_dfs = []

    for area in areas:
        monthly_df, single_df = interface(area=area)
        monthly_dfs.append(monthly_df)
        single_dfs.append(single_df)

    energies = [db["Energy export [kWh]"].mean() for db in monthly_dfs]
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    savefile = os.path.join(dir_path, f"")
    
    
    fig, ax = plt.subplots()
    ax.plot(areas, energies, label="")
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    plt.show()
    # fig.savefig(f"{savefile}.svg", transparent=True)


def main():
    montly_df, single_df = interface()
    df_name = os.path.join(dir_path, "output", f"total_df_monthly.csv")
    montly_df.to_csv(df_name)
    print(montly_df)
    df_name = os.path.join(dir_path, "output", f"total_df_onetime.csv")
    single_df.to_csv(df_name)
    print(single_df)

vary_energy_output()
# main()
