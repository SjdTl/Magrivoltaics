import pandas as pd
import numpy as np
import pvlib
from pvlib.tools import cosd
import matplotlib.pyplot as plt

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
    Irradiation is the 
    
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

     # --- 1. Location and time setup (yearly hourly timeseries)
    location = pvlib.location.Location(latitude, longitude, altitude=elevation)
    times = pd.date_range('2024-01-01', '2024-12-31 23:00', freq='1h', tz='UTC')

    solpos = location.get_solarposition(times)
    clearsky = location.get_clearsky(times, model='ineichen')
    dni_extra = pvlib.irradiance.get_extra_radiation(times)

    # --- 2. Ground coverage ratio from coverage input
    gcr = coverage  # directly use user-specified ratio
    height = 2.5    # assumed tracker height for agrivoltaic system
    row_width = 2*2.384 # assumed row_width 
    pitch = row_width / gcr

    # --- 3. Simple fixed-tilt POA model
    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solpos['apparent_zenith'],
        solar_azimuth=solpos['azimuth'],
        dni_extra=dni_extra,
        model='haydavies'
    )

    # --- 4. PVWatts power model
    temp_air = 20  # °C, assumed
    temp_cell = pvlib.temperature.faiman(
        poa_global=poa['poa_global'], temp_air=temp_air
    )
    gamma_pdc = -0.004  # power temp coefficient
    N_modules = 100
    power_dc = pvlib.pvsystem.pvwatts_dc(
        effective_irradiance=poa['poa_global'],
        temp_cell=temp_cell,
        pdc0= rated_power * N_modules,  
        gamma_pdc=gamma_pdc
    )

     # --- 5. Apply efficiency and panel area scaling (optional realism)
    power_kw = (power_dc * efficiency / 1000.0)

    # --- 6. Monthly aggregation
    monthly_avg_power = power_kw.resample('ME').mean()
    monthly_avg_power.index = monthly_avg_power.index.strftime('%B')

    result = pd.DataFrame({
        'Month': monthly_avg_power.index,
        'Average Power (kW)': monthly_avg_power.values
    })

    return result
    # energy = 12*[12]
    # irradiation_panel = 12*[25]
    # irradiation_crop = 12*[20]

    # energy = pd.DataFrame(np.transpose([energy, irradiation_crop, irradiation_panel]), 
    #                       columns=["Energy output [kWh]", "Irradiation crop [kWh/m^2]", "Irradiation panel [kWh/m^2]"], 
    #                       index=months)

if __name__ == '__main__':
    database = energy_output()
    print(database)