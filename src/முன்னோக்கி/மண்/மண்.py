from abc import abstractmethod, ABC
from numbers import Number
import xarray as xr

from src.முன்னோக்கி.தாள் import தாள்


class மண்(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன்):
        pass