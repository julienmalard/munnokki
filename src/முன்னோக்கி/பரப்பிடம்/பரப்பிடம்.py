from abc import ABC, abstractmethod
from numbers import Real
from typing import Optional

import xarray as xr

from முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import இயல்பு_தரவு_பாதை


class பரப்பிடம்:
    def நாடுகள்(தன்) -> list[str]:
        pass


class பரப்பிடப்_பகுப்பி(ABC):
    def __init__(தன், தரவு_கோப்புரை: Optional[str] = None):
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை or இயல்பு_தரவு_பாதை("முன்னோக்கி")

    @abstractmethod
    def பெட்டி(
        தன்,
        பரப்பிடம்_குறிப்பு: பரப்பிடம்,
    ) -> tuple[Real, Real]:
        pass

    @abstractmethod
    def மறை(
        தன்,
        பரப்பிடம்_குறிப்பு: பரப்பிடம்,
    ) -> xr.DataArray:
        pass
