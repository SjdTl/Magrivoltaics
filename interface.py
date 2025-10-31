import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
from modules.agriculture import agricultural
from modules.utils import save_plot
import os as os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import time
import scienceplots

dir_path = os.path.dirname(os.path.realpath(__file__))

def interface(crop_type : str = "potatoes", 
              area : float  = 100000,
              latitude : float = 36,
              longitude  : float= 14.5,
              elevation : float = 10,
              height : float = 3,
              azimuth : float = 180, 
              tilt : float = 30, 
              row_width : float = 4,
              pitch : float = 9,
              panel_area : float = 2.42,
              rated_power : float = 580,
              lifetime : float = 30,
              measure_time : bool = False,
            #   tilt_tracking : bool = False,
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
    row_width : float
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
        | Month    | Energy Output [kWh] | Irradiation Panels [kW/m^2] | Irradiation Crops [W/m^2]  | Energy Export [kWh] | Energy Usage [kWh] | Crop Impact [kW/m^2] |
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

    if measure_time == True:
        start_time = time.time()
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
                                # tilt_tracking = tilt_tracking,
                                )
    if measure_time == True:
        print("Energy out module")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        
    df_energyUse = energy_usage()
    df_energyOut["Energy export [kWh]"] = df_energyOut["Energy output [kWh]"] - df_energyUse["Energy usage [kWh]"]

    if measure_time == True:
        print("Energy use module")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

    df_agricultural = agricultural(crop_type = crop_type, 
                                   irradiation_crop= np.array(df_energyOut["Irradiation crops [W/m^2]"]))
    
    if measure_time == True:
        print("Agricultural module")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

    df_economicsSingle = economics(area = area,
                                   coverage = row_width/pitch,
                                   panel_area = panel_area,
                                   energy = df_energyOut["Energy export [kWh]"],
                                   subsidy = 0.0,
                                   lifetime = lifetime)
    
    if measure_time == True:
        print("Economics module")
        print("--- %s seconds ---" % (time.time() - start_time))

    monthly_df = pd.concat([df_energyOut, df_energyUse, df_agricultural], axis=1)
    single_df = pd.concat([df_economicsSingle], axis=1)

    return monthly_df, single_df

def vary_energy_output():
    plt.style.use(['science','ieee'])
    areas = np.linspace(10,2e5, 10)
    monthly_dfs = []
    single_dfs = []

    input_file = "ideal_inputs"
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, "inputs", rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    for area in tqdm(areas):
        monthly_df, _ = interface(crop_type      = str(input_data['crop_type']), 
                                  area           = float(input_data['area']),
                                  latitude       = float(input_data['latitude']),
                                  longitude      = float(input_data['longitude']),
                                  elevation      = float(input_data['elevation']),
                                  height         = float(input_data['height']),
                                  azimuth        = float(input_data['azimuth']), 
                                  tilt           = float(input_data['tilt']), 
                                  row_width      = float(input_data['row_width']),
                                  pitch          = float(input_data['pitch']),
                                  panel_area     = float(input_data['panel_area']),
                                  rated_power    = float(input_data['rated_power']),
                                  lifetime       = float(input_data['lifetime']),
                                  measure_time   = str(input_data['measure_time']) == "True",
                              )
        monthly_df, single_df = interface(area=area)
        monthly_dfs.append(monthly_df)
        single_dfs.append(single_df)

    energies = np.array([db["Energy export [kWh]"].sum() for db in monthly_dfs])
    
    fig, ax = plt.subplots()
    ax.plot(areas*1e-6, energies*1e-6)
    
    ax.set_xlabel("Area [km$^2$]")
    ax.set_ylabel("Energy export [GWh/y]")
    ax.set_title("Area vs energy export")
    plt.tight_layout()
    save_plot(os.path.join(dir_path, "output", rf"determine_area.svg"))

def panel_placement(name="panel_placement", parameter_1 = "tilt", parameter_2 = "azimuth"):
    plt.style.use(['science','ieee'])

    input_file = "ideal_inputs"
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, "inputs", rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    N = 10
    energy_outputs = np.array([[0]*N]*N)
    crop_impacts = np.array([[0]*N]*N, dtype=np.float16)

    interface_lambda = lambda az, til, pit : interface(crop_type      = str(input_data['crop_type']), 
                                                       area           = float(input_data['area']),
                                                       latitude       = float(input_data['latitude']),
                                                       longitude      = float(input_data['longitude']),
                                                       elevation      = float(input_data['elevation']),
                                                       height         = float(input_data['height']),
                                                       azimuth        = az, 
                                                       tilt           = til, 
                                                       row_width      = float(input_data['row_width']),
                                                       pitch          = pit,
                                                       panel_area     = float(input_data['panel_area']),
                                                       rated_power    = float(input_data['rated_power']),
                                                       lifetime       = float(input_data['lifetime']),
                                                       measure_time   = str(input_data['measure_time']) == "True",
                                                       )

    def extract_data(monthly_df):
        monthly_df.loc[monthly_df["Crop impact [W/m^2]"] > 0, "Crop impact [W/m^2]"]=0
        out = monthly_df.mean()
        energy_outputs[t, a] = out["Energy output [kWh]"]
        crop_impacts[t, a] = out["Crop impact [W/m^2]"]

    def plot_results(data, title, unit, xlabel, ylabel, xlabeldata, ylabeldata, subname):
        print("Plotting ...")
        fig, ax = plt.subplots(figsize=(6, 5))

        im = ax.imshow(data, origin='lower', cmap='viridis')
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
        cbar.set_label(rf'{title} [{unit}]', fontsize=12)

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, fontsize=14)

        ax.set_xticks(np.arange(N))
        ax.set_yticks(np.arange(N))

        ax.set_xticklabels(np.round(xlabeldata, 1), rotation=45, ha='right')
        ax.set_yticklabels(np.round(ylabeldata, 1))

        fig.tight_layout()
        save_plot(os.path.join(dir_path, "output", rf"{name}_{subname}.svg"))

    if parameter_1 == "tilt" and parameter_2 == "azimuth":
        tilts = np.linspace(10, 50, N)
        azimuths = np.linspace(120, 240, N)
        for t, tilt in (enumerate(tqdm(tilts))):
            for a, azimuth in enumerate(azimuths):
                monthly_df, _ = interface_lambda(azimuth, tilt, float(input_data['pitch']))
                extract_data(monthly_df)
        plot_results(energy_outputs,'Average Energy Output', "kWh", "Azimuth Angle [degrees]", "Tilt angle [degrees]", azimuths, tilts, "energy")
        plot_results(crop_impacts, 'Average Crop Impact', "W/m$^2$", "Azimuth Angle [degrees]", "Tilt angle [degrees]", azimuths, tilts, "crop")
        
    if parameter_1 == "tilt" and parameter_2 == "pitch":
        tilts = np.linspace(10, 50, N)

        min_pitch = float(input_data["row_width"])
        pitchs = np.linspace(min_pitch+1, min_pitch + 10, N)
        for t, tilt in (enumerate(tqdm(tilts))):
            for a, pitch in enumerate(pitchs):
                monthly_df, _ = interface_lambda(float(input_data['azimuth']), tilt, pitch)
                extract_data(monthly_df)
        plot_results(energy_outputs,'Average Energy Output', "kWh", "Pitch [m]", "Tilt angle [degrees]", pitchs, tilts, "energy")
        plot_results(crop_impacts, 'Average Crop Impact', "W/m$^2$", "Pitch [m]", "Tilt angle [degrees]", pitchs, tilts, "crop")

def crop_testing(name="crop_testing"):
    plt.style.use(['science','ieee'])

    input_file = "ideal_inputs"
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, "inputs", rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    monthly_df, _ = interface(crop_type      = str(input_data['crop_type']), 
                              area           = float(input_data['area']),
                              latitude       = float(input_data['latitude']),
                              longitude      = float(input_data['longitude']),
                              elevation      = float(input_data['elevation']),
                              height         = float(input_data['height']),
                              azimuth        = float(input_data['azimuth']), 
                              tilt           = 33, 
                              row_width      = float(input_data['row_width']),
                              pitch          = float(input_data['pitch']),
                              panel_area     = float(input_data['panel_area']),
                              rated_power    = float(input_data['rated_power']),
                              lifetime       = float(input_data['lifetime']),
                              measure_time   = str(input_data['measure_time']) == "True",
                              )
    print(monthly_df)
    fig, ax = plt.subplots(figsize=(4, 3))

    ax.plot(np.linspace(1,12,12), monthly_df["Irradiation crops [W/m^2]"], label="33 degree tilt")

    monthly_df, _ = interface(crop_type      = str(input_data['crop_type']), 
                              area           = float(input_data['area']),
                              latitude       = float(input_data['latitude']),
                              longitude      = float(input_data['longitude']),
                              elevation      = float(input_data['elevation']),
                              height         = float(input_data['height']),
                              azimuth        = float(input_data['azimuth']), 
                              tilt           = 0, 
                              row_width      = float(input_data['row_width']),
                              pitch          = float(input_data['pitch']),
                              panel_area     = float(input_data['panel_area']),
                              rated_power    = float(input_data['rated_power']),
                              lifetime       = float(input_data['lifetime']),
                              measure_time   = str(input_data['measure_time']) == "True",
                              )
    
    ax.plot(np.linspace(1,12,12), monthly_df["Irradiation crops [W/m^2]"], label="0 degree tilt")
    
    ax.plot(np.linspace(1,12,12), monthly_df["Irradiation panels [W/m^2]"], label="Horizontal irradiation")
    ax.plot(np.linspace(1,12,12), monthly_df["Minimum crop [W/m^2]"], "-o", label="Minimum irradiation")

    ax.set_xlabel("Months")
    ax.set_ylabel("Irradiation [W/m$^2$]")
    ax.set_title("Irradiation with and without panels")
    ax.legend(loc = 'upper right', fancybox=True, frameon=True, bbox_to_anchor=(1.05, 1.05))
    fig.tight_layout()

    save_plot(os.path.join(dir_path, "output", rf"{name}.svg"))


def main(input_file = "verification_inputs.csv"):
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, "inputs", rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    monthly_df, single_df = interface(crop_type      = str(input_data['crop_type']), 
                                     area           = float(input_data['area']),
                                     latitude       = float(input_data['latitude']),
                                     longitude      = float(input_data['longitude']),
                                     elevation      = float(input_data['elevation']),
                                     height         = float(input_data['height']),
                                     azimuth        = float(input_data['azimuth']), 
                                     tilt           = float(input_data['tilt']), 
                                     row_width      = float(input_data['row_width']),
                                     pitch          = float(input_data['pitch']),
                                     panel_area     = float(input_data['panel_area']),
                                     rated_power    = float(input_data['rated_power']),
                                     lifetime       = float(input_data['lifetime']),
                                     measure_time   = str(input_data['measure_time']) == "True",
                                     )

    monthly_df["Crop impact [W/m^2]"][monthly_df["Crop impact [W/m^2]"] > 0]=0
    
    df_name = os.path.join(dir_path, "output", f"{input_file}_monthly.csv")
    monthly_df.to_csv(df_name)
    df_name = os.path.join(dir_path, "output", f"{input_file}_onetime.csv")
    single_df.to_csv(df_name)

    print(monthly_df)
    print(monthly_df.mean())
    print(single_df)

# main("verification_inputs.csv")
# main("ideal_inputs.csv")
# vary_energy_output()
# panel_placement("tilt_azimuth", "tilt", "azimuth")
# panel_placement("tilt_pitch", "tilt", "pitch")
crop_testing()
