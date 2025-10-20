import pandas as pd

months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def agricultural(irradiation_panels = 12*[10],
                 irradiation_crop = 12*[20],
                 crop_type = "potatoes"):
    """
    Description
    -----------
    Determine things related to agriculture
    
    Parameters
    ----------
    irradiation_panels : np.array 
        Energy output of the solar array per month [kWh]
    irradiation_crop : np.array
       Irradiation per m^2 [kW/m2] still arriving at crop 
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
    possible_crops = ["potatoes"]
    
    # Define necessary solar irradiation thresholds for each crop (MJ/m²/month)
    crop_requirements = {
        "potatoes": {
            "min": [49.2, 49.2, 49.2, 0, 0, 0, 0, 0, 0, 0, 49.2, 49.2],
            "max": [85.8, 85.8, 85.8, 0, 0, 0, 0, 0, 0, 0, 85.8, 85.8]
        }
    }

    # check if crop is valid
    if crop_type.lower() not in crop_type:
        raise ValueError(f"Crop type is not recognized, select one out of {possible_crops}")

   # Get the crop’s required irradiation range
    crop = crop_requirements[crop_type.lower()]
    min_req = crop["min"]
    max_req = crop["max"]

    # Compare actual irradiation with required range
    impact = []
    for i, month in enumerate(months):
        if irradiation_crop[i] < min_req[i]:
            impact.append("Crop yield reduced (too low irradiation)")
        elif irradiation_crop[i] > max_req[i]:
            impact.append("Crop yield may be stressed (too high irradiation)")
        else:
            impact.append("Yield remains constant")


    # Build the crop impact dataframe
    crop_impact = pd.DataFrame({
        "Month": months,
        "Irradiation [MJ/m²/month]": irradiation_crop,
        "Crop impact [unit]": impact
    })

    return crop_impact

if __name__ == '__main__':
    y = agricultural()
    print(y)
