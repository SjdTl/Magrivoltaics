import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def energy_usage(something : float = 10,
                  ):
    """
    Description
    -----------
    Determines the energy usage of the plant per month due to:
        - Cleaning
        - Etc.
    Varies based on the given parameters that have yet to be determined
    
    Parameters
    ----------
    something : float
        Parameter that influences the energy usage

    Returns
    -------
    energy : pd.Dataframe
        Energy per month in a pandas dataframe according to the following format:
        | Month    | Energy usage [kWh] |
        | -------- | ------------------ |
        | January  | xxx kWh            | 
        | Februari | xxx kWh            | 
    
    Notes
    -----
    xxx
    
    Examples
    --------
    >>> database = energy_usage()
    >>> print(database)
        | Month    | Energy usage  |
        | -------- | ------------- |
        | January  | xxx kWh       | 
        | February | xxx kWh       | 
    """
    





    
    energy = 12*[10]
    energy = pd.DataFrame(energy, columns=["Energy usage [kWh]"], index=months)
    return energy

if __name__ == '__main__':
    database = energy_usage()
    print(database)