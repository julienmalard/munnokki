from abc import abstractmethod, ABC
from numbers import Number

import xarray as xr

from .. import அச்சுகள்
from ..தாள் import தாள்


class நீர்பாசனம்(தாள், ABC):

    def __init__(தன்):
        pass

    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு()
        புள்ளி = தரவுகள்.sel(
            **{அச்சுகள்.அகலாங்கு: நிலநேர்க்கோடு, அச்சுகள்.நெட்டாங்கு: நிலநிரைக்கொடு},
            method="nearest",
        )
        if புள்ளி["நீர்பாசனம்"] == 0:
            return xr.where(தரவுகள்["நீர்பாசனம்"] == 0, 1, 0)
        else:
            return xr.DataArray(
                1, coords=தரவுகள்["நீர்பாசனம்"].coords, dims=தரவுகள்["நீர்பாசனம்"].dims
            )

    @abstractmethod
    def தரவுகளைப்_பெறு(தன்) -> xr.DataArray:
        pass