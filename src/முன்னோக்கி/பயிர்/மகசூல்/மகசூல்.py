from abc import ABC, abstractmethod

import xarray as xr


class மகசூல்(ABC):
    @abstractmethod
    def தரவுகளைப்_பெறு(தன், பயிர்: str) -> xr.DataArray:
        pass
