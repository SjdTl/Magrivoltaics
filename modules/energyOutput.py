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
                  angle : float = 10,
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
    angle : float 
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
        Energy per month in a pandas dataframe according to the following format:
        | Month    | Energy output [kWh] | 
        | -------- | ------------------- |
        | January  | xxx kWh             | 
        | February | xxx kWh             | 
    
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
        | Month    | Energy output [kWh] |
        | -------- | ------------------- |
        | January  | xxx kWh             | 
        | February | xxx kWh             | 
    """
    if efficiency > 1 or efficiency < 0:
        raise ValueError("Efficiency should be in fractions, ranging from 0.0 to 1.0")
    if coverage > 1 or coverage < 0:
        raise ValueError("Coverage should be in fractions, ranging from 0.0 to 1.0")
    






    energy = 12*[12]
    

    energy = pd.DataFrame(energy, columns=["Energy output [kWh]"], index=months)
    return energy

if __name__ == '__main__':
    database = energy_output()
    print(database)