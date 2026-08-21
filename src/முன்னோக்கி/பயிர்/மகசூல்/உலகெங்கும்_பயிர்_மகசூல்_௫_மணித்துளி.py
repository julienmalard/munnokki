import os
from typing import Optional

import xarray as xr

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ..மாறிலிகள் import பயிர்_அச்சு
from ...அச்சுகள் import நெட்டாங்கு_அச்சு, அகலாங்கு_அச்சு
from ...கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


class உலகெங்கும்_பயிர்_மகசூல்_௫_மணித்துளி(மகசூல்):
    """
    உலகெங்கும் பயிர் மகசூல் ஐந்து மணித்துளி
    GlobalCropYield5min


    https://data.mendeley.com/datasets/hg8wzgx4yp/4
    https://www.nature.com/articles/s41597-024-04248-2#Sec5
    https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/G1HBNK
    """

    பெயர்_சமானம் = {
        பெயர்கள்.மக்காச்சோளம்: "Maize",
        பெயர்கள்.நெல்: "Rice",
        பெயர்கள்.சோயா: "Soybean",
        பெயர்கள்.கோதுமை: "Wheat",
    }

    def __init__(
        தன்,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்கம்_முகவரி="https://data.mendeley.com/public-files/datasets/hg8wzgx4yp/files/75ae8d3f-85d1-484f-bd82-5f6c35c2e252/file_downloaded",
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்கம்_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்கள்=None) -> xr.DataArray:
        பயிர்கள் = [ப for ப in பயிர்கள் or தன்.பெயர்_சமானம்.values() if பயிர்கள் in தன்.பெயர்_சமானம்]

        தரவுகள் = []
        for பயிர் in பயிர்கள்:
            பயிர்_தரவுகள் = (
                ஜிப்_பதிவிறக்கம்(
                    உள்_கோப்பு_பாதை=தன்.உள்_கோப்பு_பெயர்(பயிர்),
                    பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
                    பெயர்="GlobalCropYield5min",
                    தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
                )
                .தரவுத்தளத்தைப்_பெறு()["band_data"]
                .squeeze("band")
                .drop_vars(["band", "spatial_ref"])
                .rename({"x": நெட்டாங்கு_அச்சு, "y": அகலாங்கு_அச்சு})
                .expand_dims({பயிர்_அச்சு: பயிர்கள்})
            )
            தரவுகள்.append(பயிர்_தரவுகள்)

        return xr.combine_by_coords(தரவுகள்)

    def உள்_கோப்பு_பெயர்(தன், பயிர்: str) -> str:
        ஆவணத்தில்_பயிர்_பெயர் = தன்.பெயர்_சமானம்[பயிர்]
        return os.path.join(
            "GlobalCropYield5min", ஆவணத்தில்_பயிர்_பெயர், f"{ஆவணத்தில்_பயிர்_பெயர்}2015.tif"
        )
