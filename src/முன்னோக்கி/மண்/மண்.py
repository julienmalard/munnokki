from abc import abstractmethod
from numbers import Number
import xarray as xr

from src.முன்னோக்கி.தாள் import தாள்


class மண்(தாள்):
    @abstractmethod
    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        pass
