from typing import Optional

from src.கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்
from src.பயிர்.பயிர் import பயிர்
import xarray as xr

class உள்_பெயர்:
    def __init__(தன், பயிர்_பெயர்):
        தன்.பயிர்_பெயர் = பயிர்_பெயர்

    def __str__(தன்):
        return f"CROPGRIDSv1.08_{தன்.பயிர்_பெயர்}.nc"


class பயிர்கட்டம்(பயிர்):
    def __init__(
        தன்,
        பயிர்: str,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
        உள்_கோப்பு_பெயர் = உள்_பெயர்
    ):
        super().__init__(பயிர்)

        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை

        தன்.பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
            பெயர்=f"{பதிவிறக்க_முகவரி}/{உள்_கோப்பு_பெயர்(தன்.பெயர்)}.nc", பதிவிறக்க_முகவரி=பதிவிறக்க_முகவரி
        )

    def ஒற்றுமை(தன்):
        x = xr.open_dataset(தன்.பதிவிறக்கம்.பெறு())

