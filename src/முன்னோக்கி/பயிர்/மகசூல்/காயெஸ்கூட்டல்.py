# https://doi.org/10.7910/DVN/XGGJAV
# https://github.com/wsag/GAEZ-_2015_code
# https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/XGGJAV/MZJYV0&version=2.0
import xarray as xr

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ...அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ...கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம்


class காயெஸ்கூட்டல்(மகசூல்):
    """
    https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XGGJAV
    """

    def __init__(
        தன்,
        பதிவிறக்கம்_முகவரி="https://rserve.dataverse.harvard.edu/cgi-bin/zipdownload?71c-5bdff1240543",
    ):
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்கம்_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்) -> xr.DataArray:
        return (
            பதிவிறக்கம்(பெயர்=தன்.உள்_கோப்பு_பெயர்(பயிர்), பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி)
            .பெறு()
            .rename(
                {
                    "x": நெட்டாங்கு_அச்சு,
                    "y": அகலாங்கு_அச்சு,
                }
            )
            .squeeze("band")
        )

    @staticmethod
    def உள்_கோப்பு_பெயர்(பயிர்_பெயர்: str, நீர்பாசனம்: bool):
        # மேலாண்மை = Irrigated, Rainfed, Total அல்லது Mean
        return f"GAEZAct2015_Yield_{காயெஸ்கூட்டல்_பெயர்(பயிர்_பெயர்)}_{'Irrigated' if நீர்பாசனம் else 'Rainfed'}.tif"


பெயர்_சமானம் = {
    "Wheat": பெயர்கள்.கோதுமை,
    "Rice": பெயர்கள்.நெல்,
    "Maize": பெயர்கள்.மக்காச்சோளம்,
    "Sorghum": பெயர்கள்,
    "Millet": பெயர்கள்,
    "Barley": பெயர்கள்,
    "Othercereals": பெயர்கள்,
    "PotatoAndSweetpotato": பெயர்கள்,
    "Cassava": பெயர்கள்,
    "Yamsandotherroots": பெயர்கள்,
    "Sugarbeet": பெயர்கள்,
    "Sugarcane": பெயர்கள்,
    "Pulses": பெயர்கள்,
    "Soybean": பெயர்கள்.சோயா,
    "Rapeseed": பெயர்கள்,
    "Sunflower": பெயர்கள்,
    "Groundnut": பெயர்கள்,
    "Oilpalmfruit": பெயர்கள்,
    "Olives": பெயர்கள்,
    "Cotton": பெயர்கள்.பருத்தி,
    "Tobacco": பெயர்கள்,
    "Banana": பெயர்கள்.வாழை,
    "Stimulants": பெயர்கள்,
    "Vegetables": பெயர்கள்,
    "CropsNES": பெயர்கள்,
    "Foddercrops": பெயர்கள்,
}


def காயெஸ்கூட்டல்_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
