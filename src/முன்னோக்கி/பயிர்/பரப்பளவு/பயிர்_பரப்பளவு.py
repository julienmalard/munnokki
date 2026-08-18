from abc import ABC, abstractmethod
from numbers import Number
from typing import Optional

import xarray as xr

from src.முன்னோக்கி.தாள் import தாள், ஒற்றுமை_குறிப்பு
from முன்னோக்கி.அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from முன்னோக்கி.பயிர்.மாறிலிகள் import பயிர்_அச்சு


class பயிர்_பரப்பளவு(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[str | list[str]] = None) -> xr.DataArray:
        pass

    def இருக்கும்_பயிர்கள்(தன், அகலாங்கு: Number, நெட்டாங்கு: Number) -> list[str]:
        தரவுகள் = தன்.தரவுகளைப்_பெறு()
        புள்ளி = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: அகலாங்கு, நெட்டாங்கு_அச்சு: நெட்டாங்கு},
            method="nearest",
        )
        return புள்ளி.coords[பயிர்_அச்சு].where(புள்ளி > 0).values

    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமை_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு(பயிர்கள்=குறிப்பு.பயிர்கள்)
        # https://www.pythontutorials.net/blog/xarray-select-nearest-lat-lon-with-multi-dimension-coordinates/
        புள்ளி = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: நிலநேர்க்கோடு, நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        )

        if புள்ளி < 0:
            return xr.DataArray(0, coords=தரவுகள்.coords, dims=தரவுகள்.dims)
        else:
            return xr.where(தரவுகள் > 0, 1, 0)
