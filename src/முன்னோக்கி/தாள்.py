from abc import abstractmethod, ABC
from numbers import Number

import xarray as xr


class தாள்(ABC):
    @abstractmethod
    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        pass
