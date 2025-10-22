import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def economics(area=10000,                           # total farm area [m²]
              coverage: float =0.5,                       # fraction of area covered by PV (0–1)
              rows: float =10,                           # number of rows in the farm
              length_rows: float =1000,                    # length of each row [m]
              height_panel: float = 2,                   # height panel
              energy = np.linspace(5,20,12),  # pandas DataFrame: monthly energy production [kWh/month]
              subsidy=0.0,                    # subsidy fraction of CAPEX (0–1)
              lifetime : float = 30):
    """
    Description
    -----------
    Gives the economical parameters
    
    Parameters
    ----------
    subsidy : float
        Amount of subsidy given initially [Eur]
    energy_per_year : np.array
        Amount of energy each month for the system in [kWh]
    lifetime : float
        Lifetime of the system [y]
    
    Returns
    -------
    single_parameters : pd.Dataframe
        Parameters of the plant that hold for the entire lifetime
        |      | Value |
        | LCEO | xxx   |
    montly_parameters : pd.Dataframe
        Parameters that change monthly, but are consistent yearly
        |          | Maintenance cost |
        | January  | xxxx             | 
        | February | xxxx             |                  
    Notes
    -----

    Examples
    --------

    """

    # area calculations
    panel_area_m2 = 2.58
    area_pv = area * coverage
    n_panels = area_pv / panel_area_m2
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
    LCOE= ( (alpha * (CAPEX - subsidy))+ OM ) / annual_energy_kWh 
    #ROI
    energy_price = 0.1301 #€/kWh
    net_profit= (energy_price-LCOE)*annual_energy_kWh
    ROI=(net_profit/CAPEX)*100

    single_parameters = pd.DataFrame({
        "LCOE [EUR/kWh]" : [LCOE],
         "ROI" : [ROI],
         "Operation & Maintenance cost [EUR/y]" : [OM],
         "Energy price [EUR/kWh]" : [energy_price],
         })


    return single_parameters

# ===== Test the function =====
if __name__ == '__main__':
    s = economics(
    )
    print(s)
