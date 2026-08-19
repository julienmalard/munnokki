import typing
from abc import abstractmethod, ABC
from numbers import Number
from typing import Optional

import xarray as xr
from pybtex.database import Entry

from .கருவிகள்.பதிவிறக்கம் import இயல்பு_தரவு_பாதை
from .உரிமங்கள் import உரிமம்

if typing.TYPE_CHECKING:
    from .காலநிலை.காலநிலை import காலநிலை_குறிப்பு


class ஒற்றுமைக்_குறிப்பு:
    def __init__(
        தன், காலநிலை: "காலநிலை_குறிப்பு", பயிர்கள்: Optional[str | list[str]] = None
    ):
        தன்.காலநிலை = காலநிலை
        தன்.பயிர்கள் = பயிர்கள்


class தாள்(ABC):
    def __init__(தன், தரவு_கோப்புரை: Optional[str] = None):
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை or இயல்பு_தரவு_பாதை("முன்னோக்கி")

    @abstractmethod
    def ஒற்றுமை(
        தன்,
        நிலநேர்க்கோடு: Number,
        நிலநிரைக்கொடு: Number,
        குறிப்பு: ஒற்றுமைக்_குறிப்பு,
        மறை: Optional[xr.DataArray] = None,
    ) -> xr.DataArray:
        pass

    def மேற்கோள்(தன்) -> list[Entry]:
        return []

    def உரிமம்(தன்) -> Optional[உரிமம்]:
        pass
