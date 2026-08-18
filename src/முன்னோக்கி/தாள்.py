from abc import abstractmethod, ABC
from numbers import Number
from typing import Iterable, Optional

import xarray as xr

from முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import இயல்பு_தரவு_பாதை


class தாள்(ABC):
    def __init__(தன், தரவு_கோப்புரை: Optional[str] = None):
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை or இயல்பு_தரவு_பாதை("முன்னோக்கி")

    @abstractmethod
    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        pass
