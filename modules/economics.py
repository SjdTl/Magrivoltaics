import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def economics(subsidy : float = 10,
              energy = np.linspace(5,20,12),
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
    total_cost = 1e6
    LCOE = (total_cost - subsidy) / (lifetime * np.sum(energy))
    single_parameters = pd.DataFrame({
        "LCOE" : [LCOE],
         "ROI" : [4],
         })

    maintenance_cost = 12*[10]
    energy_price = 12*[10]
    monthly_parameters = pd.DataFrame(np.transpose([maintenance_cost, energy_price]), 
                                      columns=["Maintenance cost [eur]", "Energy price [eur]"], 
                                      index=months)
    return single_parameters, monthly_parameters

if __name__ == '__main__':
    s, m = economics()
    print(s)
    print(m)