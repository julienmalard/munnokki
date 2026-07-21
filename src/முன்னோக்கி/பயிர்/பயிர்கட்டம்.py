from numbers import Number
from typing import Optional

import xarray as xr

from .. import அச்சுகள்
from . import பயிர்
from ..கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


class பயிர்கட்டம்(பயிர்):
    def __init__(
        தன்,
        தரவு_திறன்: 0,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
    ):
        super().__init__()

        தன்.தரவு_திறன் = தரவு_திறன்
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number, பயிர்_பெயர்: str) -> xr.DataArray:
        பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
            பெயர்=f"{தன்.பதிவிறக்க_முகவரி}/{தன்.உள்_கோப்பு_பெயர்(பயிர்_பெயர்)}",
            பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
        )
        தரவுகள் = xr.open_dataset(பதிவிறக்கம்.பெறு()).rename(
            {"lat": அச்சுகள்.அகலாங்கு, "lon": அச்சுகள்.நெட்டாங்கு}
        )
        தரவுகள் = தன்.வடிக்க(தரவுகள்)
        # https://www.pythontutorials.net/blog/xarray-select-nearest-lat-lon-with-multi-dimension-coordinates/
        புள்ளி = தரவுகள்.sel(
            **{அச்சுகள்.அகலாங்கு: நிலநேர்க்கோடு, அச்சுகள்.நெட்டாங்கு: நிலநிரைக்கொடு},
            method="nearest",
        )
        if புள்ளி["croparea"] < 0:
            return xr.DataArray(
                0, coords=தரவுகள்["croparea"].coords, dims=தரவுகள்["croparea"].dims
            )
        else:
            return xr.where(தரவுகள்["croparea"] > 0, 1, 0)

    @staticmethod
    def உள்_கோப்பு_பெயர்(பயிர்_பெயர்: str):
        return f"CROPGRIDSv1.08_{பயிர்_பெயர்}.nc"

    def வடிக்க(தன், தரவுகள்: xr.Dataset) -> xr.Dataset:
        தரவுகள்["croparea"] = xr.where(தரவுகள்["quality"] >= தன்.தரவு_திறன், தரவுகள்["croparea"], 0)
        தரவுகள்["harvarea"] = xr.where(தரவுகள்["quality"] >= தன்.தரவு_திறன், தரவுகள்["harvarea"], 0)
        return தரவுகள்
