import os.path
import shutil
from typing import Optional
from zipfile import ZipFile

import requests
import xarray as xr
from appdata import AppDataPaths


class பதிவிறக்கம்:
    def __init__(
        தன், பதிவிறக்க_முகவரி: str, பெயர்: Optional[str] = None, செயலி_பெயர்="முன்னோக்கி"
    ):
        தன்.பெயர் = பெயர் or os.path.basename(பதிவிறக்க_முகவரி)
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி
        தன்.செயலி_பெயர் = செயலி_பெயர்

        தன்.செயலி_பாதைகள் = AppDataPaths(தன்.செயலி_பெயர்)
        தன்.செயலி_பாதைகள்.setup()

    @property
    def கோப்பு_பாதை(தன்) -> str:
        return os.path.join(தன்.செயலி_பாதைகள்.app_data_path, தன்.பெயர்)

    def பெறு(தன்) -> xr.Dataset:
        if not os.path.isfile(தன்.கோப்பு_பாதை):
            தன்.பதிவேற்கு()
        return xr.open_dataset(தன்.கோப்பு_பாதை, chunks="auto")

    def பதிவேற்கு(தன்):
        with requests.get(தன்.பதிவிறக்க_முகவரி, stream=True) as கோரிக்கை:
            with open(தன்.கோப்பு_பாதை, "wb") as கோப்பு:
                shutil.copyfileobj(கோரிக்கை.raw, கோப்பு)

    def நீக்கு(தன்):
        if os.path.exists(தன்.கோப்பு_பாதை):
            os.remove(தன்.கோப்பு_பாதை)


class ஜிப்_பதிவிறக்கம்(பதிவிறக்கம்):
    def __init__(தன், பெயர்: str, பதிவிறக்க_முகவரி: str, செயலி_பெயர்="முன்னோக்கி"):
        பெயர், தன்.உள்_கோப்பு_பெயர் = பெயர்.split("/", 1)
        super().__init__(
            பெயர்=பெயர், பதிவிறக்க_முகவரி=பதிவிறக்க_முகவரி, செயலி_பெயர்=செயலி_பெயர்
        )

    def __enter__(தன்):
        தன்.பெறு()
        தன்.ஜிப் = ZipFile(தன்.கோப்பு_பாதை, "r")
        தன்.ஜிப்.__enter__()
        தன்.ஜிப்பில்_கோப்பு = தன்.ஜிப்.open(தன்.உள்_கோப்பு_பெயர்)
        தன்.ஜிப்பில்_கோப்பு.__enter__()

    def __exit__(தன், exc_type, exc_val, exc_tb):
        தன்.ஜிப்பில்_கோப்பு.__exit__(exc_type, exc_val, exc_tb)
        தன்.ஜிப்.__exit__(exc_type, exc_val, exc_tb)
        தன்.ஜிப் = None
        தன்.ஜிப்பில்_கோப்பு = None
