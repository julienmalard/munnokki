import numpy as np
import xarray as xr

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ...அச்சுகள் import நெட்டாங்கு_அச்சு, அகலாங்கு_அச்சு
from ...கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


# https://data.mendeley.com/datasets/hg8wzgx4yp/4
# https://www.nature.com/articles/s41597-024-04248-2#Sec5
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/G1HBNK


class உலகெங்கும்_பயிர்_மகசூல்_௫_மணித்துளி(மகசூல்):
    """
    உலகெங்கும் பயிர் மகசூல் ஐந்து மணித்துளி
    GlobalCropYield5min
    """

    def __init__(
        தன்,
        பதிவிறக்கம்_முகவரி="https://data.mendeley.com/public-files/datasets/hg8wzgx4yp/files/75ae8d3f-85d1-484f-bd82-5f6c35c2e252/file_downloaded",
    ):
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்கம்_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்: str) -> xr.DataArray:
        if பயிர் in பெயர்_சமானம்:
            return (
                ஜிப்_பதிவிறக்கம்(
                    பெயர்=தன்.உள்_கோப்பு_பெயர்(பயிர்), பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி
                )
                .பெறு()["band_data"]
                .squeeze("band")
                .drop_vars(["band", "spatial_ref"])
                .rename({"x": நெட்டாங்கு_அச்சு, "y": அகலாங்கு_அச்சு})
            )
        else:
            return xr.DataArray(np.nan)

    @staticmethod
    def உள்_கோப்பு_பெயர்(பயிர்: str) -> str:
        ஆவணத்தில்_பயிர்_பெயர் = பெயர்_சமானம்[பயிர்]
        return f"GlobalCropYield5min/{ஆவணத்தில்_பயிர்_பெயர்}/{ஆவணத்தில்_பயிர்_பெயர்}2015.tif"


பெயர்_சமானம் = {
    பெயர்கள்.மக்காச்சோளம்: "Maize",
    பெயர்கள்.நெல்: "Rice",
    பெயர்கள்.சோயா: "Soybean",
    பெயர்கள்.கோதுமை: "Wheat",
}
