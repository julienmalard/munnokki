from abc import abstractmethod, ABC
from numbers import Number
from typing import Iterable

import xarray as xr


class தாள்(ABC):
    @abstractmethod
    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        pass


class கூட்டுத்தாள்(தாள்):
    def __init__(தன், தாள்கள்: Iterable[தாள்]):
        தன்.தாள்கள் = தாள்கள்

    @abstractmethod
    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        ஒற்றுமை = None
        for தாள் in தன்.தாள்கள்:
            if ஒற்றுமை is None:
                ஒற்றுமை = தாள்.ஒற்றுமை()
            else:
                ஒற்றுமை.fillna(தாள்.ஒற்றுமை())

            if ஒற்றுமை.count() == ஒற்றுமை.size:
                break

        return ஒற்றுமை

    def __add__(தன், மற்ற: தாள்):
        return கூட்டுத்தாள்([*தன்.தாள்கள், மற்ற])
