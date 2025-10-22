import pandas as pd
import numpy as np

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def energy_usage():
    """
    Description
    -----------
    Determines the energy usage of the plant per month due to:
        - Cleaning
        - Etc.
    Varies based on the given parameters that have yet to be determined
    
    Parameters
    ----------
    No inputs

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
    THIS MODULE IS MADE ZERO. 
    It still exists in case this model has to be used for a farm that uses quite a lot of electricity
    However, for simplicity, we have made this zero for now
    
    Examples
    --------
    >>> database = energy_usage()
    >>> print(database)
        | Month    | Energy usage  |
        | -------- | ------------- |
        | January  | xxx kWh       | 
        | February | xxx kWh       | 
    """
    
    energy = 12*[0] 
    energy = pd.DataFrame(energy, columns=["Energy usage [kWh]"], index=months)
    return energy

if __name__ == '__main__':
    database = energy_usage()
    print(database)