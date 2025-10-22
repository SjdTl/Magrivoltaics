import pandas as pd

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def agricultural(
    crop_type="potatoes",
    irradiation_crop=[20] * 12,
):
    """
    Description
    -----------
    Determine crop impact based on monthly solar irradiation.

    Parameters
    ----------
    irradiation_crop : np.array
       Irradiation per m^2 [kW/m2] still arriving at crop 
    crop_type : str
        Crop type (currently supports only 'potatoes')

    Returns
    -------
    crop_impact : pd.DataFrame
        DataFrame showing the crop impact by month:
            | Month    | Crop impact [kW/m^2] |
            | -------- | -------------------- |
            | January  | xxx                  |
        A positive value +y indicates that there is y kW/m^2 too much radiance
        A negative value -y indicates that there is y kW/m^2 too little radiance
        A zero value 0 indicates that the radiation is within the range required for the crop
    
    Raises
    ------
    ValueError
        If crop_type not recognized.

    Note 
    ----
    Assume that the average photon wavelength of sunlight is 550nm as this is the main peak
    E_ph=hc/λ --> E_ph= 3.61x10^-19 J
    1 μmol photons = 6.022x10^17 photons
    E_per_μmol = 3.61x10^-19 J * 6.022x10^17 photons = 0.217 J--> 0.000217 kJ
    --> 1 μmol/m²/s = 0.000217 kW/m²

    Reference POTATO:
    @article{KELLER2019104293,
    title = {Historical increase in agricultural machinery weights enhanced soil stress levels and adversely affected soil functioning},
    journal = {Soil and Tillage Research},
    volume = {194},
    pages = {104293},
    year = {2019},
    issn = {0167-1987},
    doi = {https://doi.org/10.1016/j.still.2019.104293},
    url = {https://www.sciencedirect.com/science/article/pii/S016719871930131X},
    author = {Thomas Keller and Maria Sandin and Tino Colombi and Rainer Horn and Dani Or}
    }
    """

    # Define possible crops and their requirements
    possible_crops = ["potatoes"]
    crop_requirements = {
        "potatoes": {
            "stages": [
                "flowering","fruiting", "dormant","dormant", "dormant", "dormant","dormant", "dormant", "dormant", 
                "seedling", "vegetative", "vegetative",  
            ],
            "stage_ppfd_min": {
                "dormant": 0,
                "seedling": 100,
                "vegetative": 200,
                "flowering": 500,
                "fruiting": 500
            },
            "stage_ppfd_max": {
                "dormant": 0,  # Dormant period - no irradiation requirements
                "seedling": 200,
                "vegetative": 600,
                "flowering": 600,
                "fruiting": 600
            }
        }
    }

    # Check if crop is valid
    if crop_type.lower() not in possible_crops:
        raise ValueError(f"Crop type {crop_type.lower()} not recognized. Choose one of: {possible_crops}")

    # Conversion factor: 1 μmol/m²/s = 0.000217 kW/m²
    conversion_factor = 0.000217

    crop = crop_requirements[crop_type.lower()]
    stages = crop["stages"]

    # Calculate min and max PPFD lists in kW/m²
    min_req_kWm2 = [crop["stage_ppfd_min"][stage] * conversion_factor for stage in stages]
    max_req_kWm2 = [crop["stage_ppfd_max"][stage] * conversion_factor for stage in stages]

    # Compare actual irradiation with required range
    impact=[]
    for i, month in enumerate(months):
        if stages[i] == "dormant":
            impact.append(0)
        else:
            if irradiation_crop[i] < min_req_kWm2[i]:
                impact.append(irradiation_crop[i] - min_req_kWm2[i])
            elif irradiation_crop[i] > max_req_kWm2[i]:     
                impact.append(irradiation_crop[i] - max_req_kWm2[i])
            else:
                impact.append(0)

    # Build DataFrame
    crop_impact = pd.DataFrame(impact, columns=["Crop impact [kW/m^2]"], index=months)

    return crop_impact


if __name__ == '__main__':
    y = agricultural()
    print(y)
