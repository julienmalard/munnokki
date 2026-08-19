from abc import abstractmethod, ABC
from numbers import Number
from typing import Optional

import xarray as xr

from .மாறிலிகள் import மண்_மாறி_அச்சு, மண்_ஆழ_அச்சு
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ..கருவிகள்.படிமுறைகள் import யூக்ளிடிய
from ..தாள் import ஒற்றுமைக்_குறிப்பு
from ..தாள் import தாள்


class மண்(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், மறை: Optional[xr.DataArray] = None) -> xr.DataArray:
        pass

    def தொலைவு(தன், குறிப்பு: xr.DataArray, தரவுகள்: xr.DataArray) -> xr.DataArray:
        return யூக்ளிடிய(தரவுகள், குறிப்பு=குறிப்பு, அச்சு=[மண்_மாறி_அச்சு, மண்_ஆழ_அச்சு])

    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமைக்_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு(மறை)
        புள்ளி = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: நிலநேர்க்கோடு, நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        )
        return தன்.தொலைவு(புள்ளி, தரவுகள்)
