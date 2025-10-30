import pandas as pd
from modules.energyOutput import energy_output
from modules.energyUsage import energy_usage
from modules.economics import economics
from modules.agriculture import agricultural
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
                                   irradiation_crop= np.array(df_energyOut["Irradiation crops [kW/m^2]"]))
    
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
    areas = np.linspace(10,1e7, 10)
    monthly_dfs = []
    single_dfs = []

    for area in tqdm(areas):
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

def panel_placement(name="panel_placement"):
    plt.style.use(['science','ieee'])

    # Use the verification file, since the other parameters have not yet been determined
    input_file = "verification_inputs"
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    N = 10
    tilts = np.linspace(10, 50, N)
    azimuths = np.linspace(120, 240, N)

    energy_outputs = np.array([[0]*N]*N)
    crop_impacts = np.array([[0]*N]*N)
    
    for t, tilt in (enumerate(tqdm(tilts))):
        for a, azimuth in enumerate(azimuths):
            montly_df, _ = interface(crop_type      = str(input_data['crop_type']), 
                            area           = float(input_data['area']),
                            latitude       = float(input_data['latitude']),
                            longitude      = float(input_data['longitude']),
                            elevation      = float(input_data['elevation']),
                            height         = float(input_data['height']),
                            azimuth        = azimuth, 
                            tilt           = tilt, 
                            row_width      = float(input_data['row_width']),
                            pitch          = float(input_data['pitch']),
                            panel_area     = float(input_data['panel_area']),
                            rated_power    = float(input_data['rated_power']),
                            lifetime       = float(input_data['lifetime']),
                            measure_time   = str(input_data['measure_time']) == "True",
                            )
            out = montly_df.abs().mean()
            energy_outputs[t, a] = out["Energy output [kWh]"]
            crop_impacts[t, a] = out["Crop impact [W/m^2]"]

    print(energy_outputs)
    print(crop_impacts)

    fig, ax = plt.subplots(figsize=(8, 6))

    im = ax.imshow(energy_outputs, origin='lower', cmap='viridis')
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Average Energy Output [kWh]', fontsize=12)

    ax.set_title('Average Energy Output', fontsize=16, fontweight='bold')
    ax.set_xlabel('Azimuth Angle [degrees]', fontsize=14)
    ax.set_ylabel('Tilt Angle [degrees]', fontsize=14)

    ax.set_xticks(np.arange(N))
    ax.set_yticks(np.arange(N))

    ax.set_xticklabels(np.round(azimuths, 1), rotation=45, ha='right')
    ax.set_yticklabels(np.round(tilts, 1))

    fig.tight_layout()
    plt.savefig(rf"{name}_energy.svg", transparent=True)

    
    fig, ax = plt.subplots(figsize=(8, 6))

    im = ax.imshow(crop_impacts, origin='lower', cmap='viridis')
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Absolute Average Crop Impact [W/$m^2$]', fontsize=12)

    ax.set_title('Average Crop Impact', fontsize=16, fontweight='bold')
    ax.set_xlabel('Azimuth Angle [degrees]', fontsize=14)
    ax.set_ylabel('Tilt Angle [degrees]', fontsize=14)

    ax.set_xticks(np.arange(N))
    ax.set_yticks(np.arange(N))

    ax.set_xticklabels(np.round(azimuths, 1), rotation=45, ha='right')
    ax.set_yticklabels(np.round(tilts, 1))

    fig.tight_layout()
    plt.savefig(rf"{name}_crop.svg", transparent=True)



def main(input_file = "verification_inputs.csv"):
    if input_file.split('.')[-1] == "csv":
        input_file = input_file.replace(".csv", "")

    input_data_path = os.path.join(dir_path, rf"{input_file}.csv")
    input_data = pd.read_csv(input_data_path, skipinitialspace=True, index_col=0, header=None).transpose()
    input_data = (input_data.to_dict(orient="records"))[0]

    montly_df, single_df = interface(crop_type      = str(input_data['crop_type']), 
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
    
    df_name = os.path.join(dir_path, "output", f"{input_file}_monthly.csv")
    montly_df.to_csv(df_name)
    df_name = os.path.join(dir_path, "output", f"{input_file}_onetime.csv")
    single_df.to_csv(df_name)

    print(montly_df)
    print(montly_df.mean())
    print(single_df)

# vary_energy_output()
# main()
panel_placement()

