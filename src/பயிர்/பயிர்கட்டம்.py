from numbers import Number
from typing import Optional, Iterable

import xarray as xr

from src.கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்
from src.பயிர்.பயிர் import பயிர்


class உள்_பெயர்:
    def __init__(தன், பயிர்_பெயர்):
        தன்.பயிர்_பெயர் = பயிர்_பெயர்

    def __str__(தன்):
        return


class பயிர்கட்டம்(பயிர்):
    def __init__(
        தன்,
        பயிர்: str,
        வடிக்கட்டிகள்: Optional[Iterable[வடிக்கட்டி] or வடிக்கட்டி] = None,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
    ):
        super().__init__(பயிர்)

        தன்.வடிக்கட்டிகள் = வடிக்கட்டிகள்
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை

        தன்.பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
            பெயர்=f"{பதிவிறக்க_முகவரி}/{தன்.உள்_கோப்பு_பெயர்()}",
            பதிவிறக்க_முகவரி=பதிவிறக்க_முகவரி,
        )

    def ஒற்றுமை(தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number) -> xr.DataArray:
        x = xr.open_dataset(தன்.பதிவிறக்கம்.பெறு())
        # https://www.pythontutorials.net/blog/xarray-select-nearest-lat-lon-with-multi-dimension-coordinates/
        புள்ளி = x.sel(lat=நிலநேர்க்கோடு, lon=நிலநிரைக்கொடு, method="nearest")
        if புள்ளி["croparea"] < 0:
            return xr.DataArray(0, coords=x["croparea"].coords, dims=x["croparea"].dims)
        else:
            return xr.where(x["croparea"] < 0, 0, 1)

    def உள்_கோப்பு_பெயர்(தன்):
        return f"CROPGRIDSv1.08_{தன்.பெயர்}.nc"
