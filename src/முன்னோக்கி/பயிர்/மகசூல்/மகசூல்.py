from abc import ABC, abstractmethod

import xarray as xr

from ...தாள் import தாள்


class மகசூல்(தாள், ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், பயிர்: str) -> xr.DataArray:
        pass
