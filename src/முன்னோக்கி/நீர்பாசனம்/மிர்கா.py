import os.path
from typing import Optional, Literal

import xarray as xr

from ..கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்
from ..நீர்பாசனம்.நீர்பாசனம் import நீர்பாசனம்
from ..பயிர் import பயிர்_பெயர்கள் as பெயர்கள்
from ..பயிர்.மாறிலிகள் import பயிர்_அச்சு


class மிர்கா(நீர்பாசனம்):
    """
    MIRCA-OS
    https://www.nature.com/articles/s41597-024-04313-w
    https://www.hydroshare.org/resource/60a890eb841c460192c03bb590687145
    Kebede, E., Oluoch, K. O., Siebert, S., Mehta, P., Hartman, S., Jägermeyr, J., Ray, D., Ali, T., Brauman, K. A., Deng, Q., Xie, W., Davis, K. F. (2026). A global open-source dataset of monthly irrigated and rainfed cropped areas (MIRCA-OS) for the 21st century, HydroShare, https://doi.org/10.4211/hs.60a890eb841c460192c03bb590687145
    """

    பெயர்_சமானம் = {
        "Barley": பெயர்கள்.வாற்கோதுமை,
        "Cassava": பெயர்கள்.மரவள்ளி,
        "Cocoa": பெயர்கள்.கொக்கோ,
        "Coffee": பெயர்கள்.குளம்பி,
        "Cotton": பெயர்கள்.பருத்தி,
        # "Fodder": பெயர்கள்.தீவனம்,
        "Groundnuts": பெயர்கள்.வேர்கடலை,
        "Maize": பெயர்கள்.மக்காச்சோளம்,
        "Millet": பெயர்கள்.சிறுதானியம்,
        "Oil_palm": பெயர்கள்.செம்பனை,
        "Potatoes": பெயர்கள்.உருளைக்கிழங்கு,
        # "Pulses": பெயர்கள்.இருபுற_வெடிக்கனி,
        "Rapeseed": பெயர்கள்.கனோலா,
        "Rice": பெயர்கள்.நெல்,
        "Rye": பெயர்கள்.புல்லரிசி,
        "Sorghum": பெயர்கள்.சோளம்,
        "Soybeans": பெயர்கள்.சோயா,
        "Sugar_cane": பெயர்கள்.கரும்பு,
        "Sugar_beet": பெயர்கள்.சக்கரைச்_செங்கிழங்கு,
        "Sunflower": பெயர்கள்.சூரியகாந்தி,
        "Wheat": பெயர்கள்.கோதுமை,
    }

    def __init__(
        தன்,
        ஆண்டு=2015,
        துல்லியம்: Literal["5-arcminute", "30-arcminute"] = "5-arcminute",
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://www.hydroshare.org/resource/60a890eb841c460192c03bb590687145/data/contents/Annual%20Harvested%20Area%20Grids/Annual_Harvested_Area_Grids.rar",
    ):
        super().__init__(தரவு_கோப்புரை)

        தன்.ஆண்டு = ஆண்டு
        தன்.துல்லியம் = துல்லியம்
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[list[str]]) -> xr.DataArray:

        பயிர்கள் = பயிர்கள் or தன்.பெயர்_சமானம்.values()

        தரவுகள் = []
        for பயிர் in பயிர்கள்:
            பயிர்_தரவுகள் = (
                ஜிப்_பதிவிறக்கம்(
                    உள்_கோப்பு_பாதை=தன்.உள்_கோப்பு_பாதை(பயிர்),
                    பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
                    தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
                )
                .தரவு_அணியைப்_பெறு()
                .expand_dims({பயிர்_அச்சு: [பயிர்]})
            )
            தரவுகள்.append(பயிர்_தரவுகள்)

        return xr.concat(தரவுகள், dim=[பயிர்_அச்சு])

    def உள்_கோப்பு_பாதை(தன், பயிர்: str):
        குறுந்துல்லியம் = {"30-arcminute": "30arcmin", "5-arcminute": ""}[தன்.துல்லியம்]
        நீர்பாசனம்_குறியீடு = "ir"  # அல்லது 'rf'

        பெயர் = f"MIRCA-OS_{தன்.மிர்கா_பெயர்(பயிர்)}_{தன்.ஆண்டு}_{நீர்பாசனம்_குறியீடு}"
        if குறுந்துல்லியம்:
            பெயர் += f"_{குறுந்துல்லியம்}"
        பெயர் += ".tif"

        return os.path.join(
            "Annual Harvested Area Grids", str(தன்.ஆண்டு), தன்.துல்லியம், பெயர்
        )

    def மிர்கா_பெயர்(தன், பயிர்: str) -> str:
        try:
            return next(பெ for பெ in தன்.பெயர்_சமானம்.keys() if தன்.பெயர்_சமானம்[பெ] == பயிர்)
        except StopIteration:
            return பயிர்
