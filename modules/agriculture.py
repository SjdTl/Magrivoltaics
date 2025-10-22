import pandas as pd

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def agricultural(
    irradiation_panels=None,
    irradiation_crop=None,
    crop_type="potatoes"
):
    """
    Description
    -----------
    Determine crop impact based on monthly solar irradiation.

    Parameters
    ----------
    irradiation_panels : np.array 
        Energy output of the solar array per month [kWh]
    irradiation_crop : np.array
       Irradiation per m^2 [kW/m2] still arriving at crop 
    crop_type : str
        Crop type (currently supports only 'potatoes')

    Returns
    -------
    crop_impact : pd.DataFrame
        DataFrame showing the crop impact by month:
            | Month    | Irradiation [kW/m²] | Crop impact |
    
    Raises
    ------
    ValueError
        If crop_type not recognized.
    """

    # Default values
    if irradiation_panels is None:
        irradiation_panels = [10] * 12
    if irradiation_crop is None:
        irradiation_crop = [20] * 12

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

    """
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

    # Check if crop is valid
    if crop_type.lower() not in possible_crops:
        raise ValueError(f"Crop type not recognized. Choose one of: {possible_crops}")

    # Conversion factor: 1 μmol/m²/s = 0.000217 kW/m²
    conversion_factor = 0.000217

    crop = crop_requirements[crop_type.lower()]
    stages = crop["stages"]

    # Calculate min and max PPFD lists in kW/m²
    min_req_kWm2 = [crop["stage_ppfd_min"][stage] * conversion_factor for stage in stages]
    max_req_kWm2 = [crop["stage_ppfd_max"][stage] * conversion_factor for stage in stages]

    # Compare actual irradiation with required range
    impact = []
    for i, month in enumerate(months):
        if stages[i] == "dormant":
            impact.append("Dormant period - No impact")
        else:
            if irradiation_crop[i] < min_req_kWm2[i]:
                impact.append("Crop yield reduced (too low irradiation)")
            elif irradiation_crop[i] > max_req_kWm2[i]:
                impact.append("Crop yield may be stressed (too high irradiation)")
            else:
                impact.append("Yield remains optimal")

    # Build DataFrame
    crop_impact = pd.DataFrame({
        "Month": months,
        "Irradiation [kW/m²]": irradiation_crop,
        "Crop impact": impact
    })

    return crop_impact


if __name__ == '__main__':
    y = agricultural()
    print(y)
