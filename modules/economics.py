import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def economics(area=10000,
              coverage: float =0.5,
              panel_area : float = 1.7,
              energy = np.linspace(5,20,12),
              subsidy=0.0,
              lifetime : float = 30):
    """
    Description
    -----------
    Gives the economical parameters
    
    Parameters
    ----------
    area : float
        Total farm area [m^2]
    coverage : float 
        Fraction of area covered by PV (0-1)
    rows : float
        Number of rows in the farm
    length_rows : float 
        Length of each row [m]
    height_panel : float 
        Heights of panels 
    energy : np.array
        Monthly energy production [kWh/month]
    subsidy : float 
        Subsidy faction of CAPEX (0-1)
    lifetime : float 
        Lifetime of the system in years
        
    Returns
    -------
    single_parameters : pd.Dataframe
        Parameters of the plant that hold for the entire lifetime
        |   | LCEO [EUR/MWh] | ROI | Operation & Maintenance cost [EUR/y] | Energy price [EUR/kWh] |
        | - | -------------- | --- | ------------------------------------ | ---------------------- |
        | 0 | xxx            | xxx | xxx                                  | xxx                    |
    
    Notes
    -----
    See report for more information
    
    """

    # area calculations
    area_pv = area * coverage
    n_panels = area_pv / panel_area
    p_sys_kW = (n_panels * 580) / 1000  # total system capacity [kW]

    # estimated CAPEX costs 
    panel_costs=499*n_panels*0.8          # installed cost [€]
    #mounting_costs= 19.22*rows*length_rows + 72.89*rows*n_panels*height_panel
    mounting_costs=panel_costs/250
    installation_costs=100*p_sys_kW 
    BOP_costs=1048.5*p_sys_kW 
    CAPEX = panel_costs + mounting_costs + installation_costs + BOP_costs      # [€]

    OM = 35 * p_sys_kW #[€]

    #capital recovery factor
    r=0.0215
    alpha =  (r * (1 + r) ** lifetime) / ((1 + r) ** lifetime - 1)
    #LCOE 
    annual_energy_kWh = np.sum(energy)   # sum of 12 months
    LCOE= ( (alpha * (CAPEX - subsidy))+ OM ) / (annual_energy_kWh)
    #ROI
    energy_price = 0.1301 #€/kWh
    net_profit= (energy_price-LCOE)*(annual_energy_kWh)
    ROI=(net_profit/CAPEX)*100

    single_parameters = pd.DataFrame({
         "LCOE [EUR/MWh]" : [LCOE*1e3],
         "ROI" : [ROI],
         "Operation & Maintenance cost [EUR/y]" : [OM],
         "Energy price [EUR/kWh]" : [energy_price],
         })

    return single_parameters

# ===== Test the function =====
if __name__ == '__main__':
    s = economics()
    print(s)