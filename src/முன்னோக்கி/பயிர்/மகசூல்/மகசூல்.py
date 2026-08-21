from abc import ABC, abstractmethod
from numbers import Number
from typing import Optional

import xarray as xr

from ...அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ...தாள் import தாள், ஒற்றுமைக்_குறிப்பு


class மகசூல்(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[str | list[str]] = None) -> xr.DataArray:
        pass

    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமைக்_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு()
        புள்ளி = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: நிலநேர்க்கோடு, நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        ).squeeze(dim=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு])

        return (தரவுகள் - புள்ளி) / புள்ளி
