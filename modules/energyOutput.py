import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def energy_output(latitude: float = 10, 
                  longitude : float = 10,
                  elevation : float = 10,
                  azimuth : float = 10,
                  tilt : float = 10,
                  area : float = 10,
                  coverage : float = 0.5,
                  rated_power : float = 10,
                  efficiency : float = 0.5,
                  ):
    """
    Description
    -----------
    Determines the energy output per month of a solar plant at a certain location with certain parameters
    
    Parameters
    ----------
    latitude : float
        Latitude of the farm
    longitude : float
        Longitude of the farm
    elevation : float 
        Elevation of the farm
    azimuth : float
        Azimuth in degrees [deg]
    tilt : float 
        Angle in degrees [deg]
    area : float
        Area in m2 [m^2]
    coverage : float
        How much the panels cover the area in fractions [ ]
    rated_power : float
        Rated power of the panels in Watt [W]
    efficiency : float
        Efficiency of the panels in fractions [ ]

    Returns
    -------
    energy : pd.Dataframe
        Energy per month in a pandas dataframe AND the solar irradiation according to the following format:
        | Month    | Energy output [kWh] | Irradiation crop [kWh/m^2] | Irradiation panel [kWh/m^2]    |
        | -------- | ------------------- | ---------------------      | ------------------------------ |
        | January  | xxx                 | xxx                        | xxx                            |
        | February | xxx                 | xxx                        | xxx                            |
    
    Raises
    ------
    ValueError
        Value error for efficiency and coverage if they are not given in fractions
    
    Notes
    -----
    Do not consider on-site usage of energy

    Examples
    --------
    >>> database = energy_output(coverage=0.4)
    >>> print(database)
        | Month    | Energy output [kWh] | Irradiation crop [kWh/m^2] | Irradiation panel [kWh/m^2]    |
        | -------- | ------------------- | ---------------------      | ------------------------------ |
        | January  | xxx                 | xxx                        | xxx                            |
        | February | xxx                 | xxx                        | xxx                            |
    """
    if efficiency > 1 or efficiency < 0:
        raise ValueError("Efficiency should be in fractions, ranging from 0.0 to 1.0")
    if coverage > 1 or coverage < 0:
        raise ValueError("Coverage should be in fractions, ranging from 0.0 to 1.0")



    energy = 12*[12]
    irradiation_panel = 12*[25]
    irradiation_crop = 12*[20]

    energy = pd.DataFrame(np.transpose([energy, irradiation_crop, irradiation_panel]), 
                          columns=["Energy output [kWh]", "Irradiation crop [kWh/m^2]", "Irradiation panel [kWh/m^2]"], 
                          index=months)
    return energy

if __name__ == '__main__':
    database = energy_output()
    print(database)