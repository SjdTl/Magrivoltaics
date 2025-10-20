import pandas as pd
import numpy as np
import pvlib
from pvlib.tools import cosd
import matplotlib.pyplot as plt

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def energy_output(latitude: float = 35, 
                  longitude : float = 15,
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
    
    location = pvlib.location.Location(latitude=35, longitude=15)
    times = pd.date_range('2020-06-28', periods=24*60, freq='1min', tz='UTC')
    solpos = location.get_solarposition(times)
    clearsky = location.get_clearsky(times, model='ineichen')
    
    height = 2.6  # [m] height of torque above ground
    pitch = 12  # [m] row spacing
    row_width = 2 * 2.384  # [m] two modules in portrait, each 2 m long
    gcr = row_width / pitch  # ground coverage ratio [unitless]
    axis_azimuth = 0  # [degrees] north-south tracking axis
    max_angle = 55  # [degrees] maximum rotation angle

    tracking_orientations = pvlib.tracking.singleaxis(
        apparent_zenith=solpos['apparent_zenith'],
        solar_azimuth=solpos['azimuth'],
        axis_azimuth=axis_azimuth,
        max_angle=max_angle,
        backtrack=True,
        gcr=gcr,
    )


    # energy = 12*[12]

    energy = pd.DataFrame(energy, columns=["Energy output [kWh]"], index=months)
    return energy

if __name__ == '__main__':
    database = energy_output()
    print(database)