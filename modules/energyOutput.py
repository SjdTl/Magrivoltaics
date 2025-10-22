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
                  height : float = 2.5,
                  azimuth : float = 10,
                  tilt : float = 10,
                  row_width : float = 2*2.384,
                  pitch : float = 12,
                  area : float = 100,
                  panel_area : float = 1.7,
                  rated_power : float = 440,
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
    efficiency : float
        Efficiency of the panels in fractions [ ]

    Returns
    -------
    energy : pd.Dataframe
        Energy per month in a pandas dataframe AND the solar irradiation according to the following format:
        | Month    | Energy output [kWh] | Irradiation crop [kWh/m^2/month] | Irradiation panel [kWh/m^2/month]    |
        | -------- | ------------------- | ---------------------            | ------------------------------       |
        | January  | xxx                 | xxx                              | xxx                                  |
        | February | xxx                 | xxx                              | xxx                                  |
    
    Raises
    ------
    ValueError
        Value error for efficiency if they are not given in fractions
    
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

     # --- 1. Location and time setup (yearly hourly timeseries)
    location = pvlib.location.Location(latitude, longitude, altitude=elevation)
    times = pd.date_range('2024-01-01', '2024-12-31 23:00', freq='1h', tz='UTC')

    solpos = location.get_solarposition(times)
    clearsky = location.get_clearsky(times, model='ineichen')
    dni_extra = pvlib.irradiance.get_extra_radiation(times)

    # --- 2. Ground coverage ratio from coverage input
    gcr = row_width / pitch

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

    panel_irradiance_Wm2 = poa['poa_global']
    panel_irradiance_kWhm2 = panel_irradiance_Wm2 / 1000.0
    monthly_panel_irradiance = panel_irradiance_kWhm2.resample('ME').sum()
    monthly_panel_irradiance.index = months

    # --- 4. PVWatts power model
    temp_air = 20  # °C, assumed
    temp_cell = pvlib.temperature.faiman(
        poa_global=poa['poa_global'], temp_air=temp_air
    )
    gamma_pdc = -0.004  # power temp coefficient

    N_modules = int((area * gcr) / panel_area)
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
    monthly_avg_power.index = months

    tracking_orientations = pvlib.tracking.singleaxis(
        apparent_zenith=solpos['apparent_zenith'],
        solar_azimuth=solpos['azimuth'],
        axis_azimuth=azimuth,
        max_angle=tilt,
        backtrack=True,
        gcr=gcr,
    )
    vf_ground_sky = pvlib.bifacial.utils.vf_ground_sky_2d_integ(
    surface_tilt=tracking_orientations['surface_tilt'],
    gcr=gcr,
    height=height,
    pitch=pitch,
    )

    unshaded_ground_fraction = pvlib.bifacial.utils._unshaded_ground_fraction(
        surface_tilt=tracking_orientations['surface_tilt'],
        surface_azimuth=tracking_orientations['surface_azimuth'],
        solar_zenith=solpos['apparent_zenith'],
        solar_azimuth=solpos['azimuth'],
        gcr=gcr,
    )

    crop_avg_irradiance = (unshaded_ground_fraction * clearsky['dni']
                           * cosd(solpos['apparent_zenith'])
                            + vf_ground_sky * clearsky['dhi'])
    
    crop_irradiance_kWhm2 = crop_avg_irradiance / 1000.0
    monthly_crop_irradiance = crop_irradiance_kWhm2.resample('ME').sum()
    monthly_crop_irradiance.index = months
    irradiance_df = pd.DataFrame({
        'Month': monthly_crop_irradiance.index,
        'Crop Irradiance (kWh/m²/month)': monthly_crop_irradiance.values
    })

    result = pd.DataFrame({
    'Average Power (kW)': monthly_avg_power.values,
    'Irradiance panel level (kWh/m²/month)': monthly_panel_irradiance.values,
    'Irradiance crop level (kWh/m²/month)': monthly_crop_irradiance.values
    }, index=months)
    return result

if __name__ == '__main__':
    database = energy_output()
    print(database)