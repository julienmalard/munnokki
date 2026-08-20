from abc import ABC, abstractmethod
from numbers import Real
from typing import Optional

import xarray as xr

from ..கருவிகள்.பதிவிறக்கம் import இயல்பு_தரவு_பாதை


class பரப்பிடம்(ABC):
    def __init__(தன், தரவு_கோப்புரை: Optional[str] = None):
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை or இயல்பு_தரவு_பாதை("முன்னோக்கி")

    @abstractmethod
    def பெட்டி(
        தன்,
    ) -> tuple[Real, Real]:
        pass

    @abstractmethod
    def மறை(
        தன்,
    ) -> xr.DataArray:
        pass
