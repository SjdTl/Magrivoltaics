import pandas as pd

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def agricultural(energy_output = 12*[10],
                 irradiation = 12*[20],
                 crop_type = "mais"):
    """
    Description
    -----------
    Determine things related to agriculture
    
    Parameters
    ----------
    energy_out : np.array 
        Energy output of the solar array per month [kWh]
    irrediation : np.array
       Irradiation per m^2 [kW/m2]
    crop_type : str
        Crop type

    Returns
    -------
    crop_impact : pd.Dataframe
        I DON'T KNOW HOW THIS IS GOING TO BE DEFINED
        | Month    | Crop impact [unit]  | 
        | -------- | ------------------- |
        | January  | xxx                 | 
        | February | xxx                 | 
    
    Raises
    ------
    ValueError
        Crop_type not recognized
    
    Examples
    --------
    >>> y = agricultural()
    >>> print(y)
        | Month    | Crop impact [unit]  | 
        | -------- | ------------------- |
        | January  | xxx                 | 
        | February | xxx                 | 
    """
    possible_crops = ["mais"]
    if crop_type.lower() not in crop_type:
        raise ValueError(f"Crop type is not recognized, select one out of {possible_crops}")
    

    crop_impact = 12*[12]
    crop_impact = pd.DataFrame(crop_impact, columns=["Crop impact [unit]"], index=months)
    return crop_impact

if __name__ == '__main__':
    y = agricultural()
    print(y)