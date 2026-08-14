from abc import abstractmethod, ABC
from numbers import Number
from typing import Optional

import xarray as xr

from src.முன்னோக்கி.தாள் import தாள்
from முன்னோக்கி.அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from முன்னோக்கி.கருவிகள்.படிமுறைகள் import யூக்ளிடிய


class மண்(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், மறை: Optional[xr.DataArray] = None) -> xr.DataArray:
        pass

    def தொலைவு(தன், குறிப்பு: xr.DataArray, தரவுகள்: xr.DataArray) -> xr.DataArray:
        return யூக்ளிடிய(தரவுகள், குறிப்பு=குறிப்பு)

    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு(மறை)
        புள்ளி = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: நிலநேர்க்கோடு, நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        )
        return தன்.தொலைவு(புள்ளி, தரவுகள்)
