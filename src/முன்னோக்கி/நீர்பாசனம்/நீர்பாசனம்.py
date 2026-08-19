from abc import abstractmethod, ABC
from numbers import Number
from typing import Optional

import xarray as xr

from .. import அச்சுகள்
from ..தாள் import தாள், ஒற்றுமைக்_குறிப்பு


class நீர்பாசனம்(தாள், ABC):
    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமைக்_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு(பயிர்கள்=குறிப்பு.பயிர்கள்)
        புள்ளி = தரவுகள்.sel(
            **{அச்சுகள்.அகலாங்கு_அச்சு: நிலநேர்க்கோடு, அச்சுகள்.நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        )
        if புள்ளி["நீர்பாசனம்"] == 0:
            return xr.where(தரவுகள்["நீர்பாசனம்"] == 0, 1, 0)
        else:
            return xr.DataArray(
                1, coords=தரவுகள்["நீர்பாசனம்"].coords, dims=தரவுகள்["நீர்பாசனம்"].dims
            )

    @abstractmethod
    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[list[str]]) -> xr.DataArray:
        pass
