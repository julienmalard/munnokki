import xarray as xr

from src.முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்
from src.முன்னோக்கி.நீர்பாசனம்.நீர்பாசனம் import நீர்பாசனம்


# MIRCA-OS
# https://www.nature.com/articles/s41597-024-04313-w
class மிர்கா(நீர்பாசனம்):
    def __init__(
        தன்,
        பதிவிறக்க_முகவரி="https://www.hydroshare.org/resource/60a890eb841c460192c03bb590687145/data/contents/Annual%20Harvested%20Area%20Grids/Annual_Harvested_Area_Grids.rar",
    ):
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்: str) -> xr.DataArray:
        ஜிப்_பதிவிறக்கம்(பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி)
        system = "ir"  # 'rf'
        f"MIRCA-OS_{மிர்கா_பெயர்(பயிர்)}_{2015}_{system}_{version}"


பெயர்_சமானம் = {
    "barley": பெயர்கள்,
    "cassava": பெயர்கள்,
    "cocoa": பெயர்கள்,
    "coffee": பெயர்கள்,
    "cotton": பெயர்கள்,
    "fodder": பெயர்கள்,
    "groundnuts": பெயர்கள்,
    "maize": பெயர்கள்,
    "millet": பெயர்கள்,
    "oil palm": பெயர்கள்,
    "potatoes": பெயர்கள்,
    "pulses": பெயர்கள்,
    "rapeseed": பெயர்கள்,
    "rice": பெயர்கள்,
    "rye": பெயர்கள்,
    "sorghum": பெயர்கள்,
    "soybeans": பெயர்கள்,
    "sugar cane": பெயர்கள்,
    "sugar beet": பெயர்கள்,
    "sunflower": பெயர்கள்,
    "wheat": பெயர்கள்,
}


def மிர்கா_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
