# https://doi.org/10.7910/DVN/XGGJAV
# https://github.com/wsag/GAEZ-_2015_code
# https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/XGGJAV/MZJYV0&version=2.0
from numbers import Number
from typing import Optional

import xarray as xr

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ...அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ...கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம்
from ...தாள் import ஒற்றுமைக்_குறிப்பு


class காயெஸ்கூட்டல்(மகசூல்):
    """
    https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XGGJAV
    """

    def __init__(
        தன்,
        பதிவிறக்கம்_முகவரி="https://rserve.dataverse.harvard.edu/cgi-bin/zipdownload?71c-5bdff1240543",
        தரவு_கோப்புரை: Optional[str] = None,
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்கம்_முகவரி

    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமைக்_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        pass

    def தரவுகளைப்_பெறு(தன், பயிர்) -> xr.DataArray:
        return (
            பதிவிறக்கம்(
                பெயர்=தன்.உள்_கோப்பு_பெயர்(பயிர்),
                பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
                தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
            )
            .தரவு_அணியைப்_பெறு()
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
    "Sorghum": பெயர்கள்.சோளம்,
    "Millet": பெயர்கள்.சிறுதானியம்,
    "Barley": பெயர்கள்.வாற்கோதுமை,
    # "Othercereals": பெயர்கள்.வேறு_தானியங்கள்,
    # "PotatoAndSweetpotato": பெயர்கள்,
    "Cassava": பெயர்கள்.மரவள்ளி,
    # "Yamsandotherroots": பெயர்கள்.சேனைக்கிழங்கு,
    "Sugarbeet": பெயர்கள்.சக்கரைச்_செங்கிழங்கு,
    "Sugarcane": பெயர்கள்.கரும்பு,
    # "Pulses": பெயர்கள்.இருபுற_வெடிக்கனி,
    "Soybean": பெயர்கள்.சோயா,
    "Rapeseed": பெயர்கள்.கனோலா,
    "Sunflower": பெயர்கள்.சூரியகாந்தி,
    "Groundnut": பெயர்கள்.வேர்கடலை,
    "Oilpalmfruit": பெயர்கள்.செம்பனை,
    "Olives": பெயர்கள்.ஐரோப்பிய_இடலை,
    "Cotton": பெயர்கள்.பருத்தி,
    "Tobacco": பெயர்கள்.புகையிலை,
    "Banana": பெயர்கள்.வாழை,
    # "Stimulants": பெயர்கள்,
    # "Vegetables": பெயர்கள்.காய்றிகள்,
    # "CropsNES": பெயர்கள்,
    # "Foddercrops": பெயர்கள்.தீவனம்,
}


def காயெஸ்கூட்டல்_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
