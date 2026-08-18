import os.path
import shutil
from tempfile import NamedTemporaryFile
from typing import Optional
from zipfile import ZipFile

import requests
import rioxarray as _
import xarray as xr
from appdata import AppDataPaths
from rarfile import RarFile


class இயல்பு_தரவு_பாதை:
    def __init__(தன், செயலி_பெயர்: str):
        தன்.செயலி_பாதைகள் = AppDataPaths(செயலி_பெயர்)
        தன்.செயலி_பாதைகள்.setup()

    def நீக்கு(தன்):
        shutil.rmtree(str(தன்))

    def __str__(தன்):
        பாதை = os.path.join(தன்.செயலி_பாதைகள்.app_data_path, "தரவுகள்")
        if not os.path.isdir(பாதை):
            os.makedirs(பாதை)

        return பாதை


class பதிவிறக்கம்:
    def __init__(
        தன், பதிவிறக்க_முகவரி: str, தரவு_கோப்புரை: str, பெயர்: Optional[str] = None
    ):
        தன்.பெயர் = பெயர் or os.path.basename(பதிவிறக்க_முகவரி)
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை

    @property
    def கோப்பு_பாதை(தன்) -> str:
        return os.path.join(தன்.தரவு_கோப்புரை, தன்.பெயர்)

    def பதிவேற்கு(தன்):
        if not os.path.isfile(தன்.கோப்பு_பாதை):
            with NamedTemporaryFile() as தற்காலிகமானது:
                with requests.get(தன்.பதிவிறக்க_முகவரி, stream=True) as கோரிக்கை:
                    கோரிக்கை.raise_for_status()

                    for chunk in கோரிக்கை.iter_content():
                        if chunk:
                            தற்காலிகமானது.write(chunk)

                shutil.move(தற்காலிகமானது.name, தன்.கோப்பு_பாதை)

        return தன்.கோப்பு_பாதை

    def தரவு_அணியைப்_பெறு(தன்) -> xr.DataArray:
        _
        தன்.பதிவேற்கு()
        நீட்டி = os.path.splitext(தன்.கோப்பு_பாதை)[1]
        return xr.open_dataarray(
            தன்.கோப்பு_பாதை, chunks="auto", engine="rasterio" if நீட்டி == ".tif" else None
        )

    def தரவுத்தளத்தைப்_பெறு(தன்) -> xr.Dataset:
        _
        தன்.பதிவேற்கு()
        நீட்டி = os.path.splitext(தன்.கோப்பு_பாதை)[1]
        return xr.open_dataset(
            தன்.கோப்பு_பாதை, chunks="auto", engine="rasterio" if நீட்டி == ".tif" else None
        )

    def நீக்கு(தன்):
        if os.path.exists(தன்.கோப்பு_பாதை):
            os.remove(தன்.கோப்பு_பாதை)


class ஜிப்_பதிவிறக்கம்(பதிவிறக்கம்):
    def __init__(
        தன்,
        உள்_கோப்பு_பாதை: str,
        பதிவிறக்க_முகவரி: str,
        தரவு_கோப்புரை: str,
        பெயர்: Optional[str] = None,
    ):
        தன்.உள்_கோப்பு_பாதை = உள்_கோப்பு_பாதை

        super().__init__(
            பெயர்=பெயர், பதிவிறக்க_முகவரி=பதிவிறக்க_முகவரி, தரவு_கோப்புரை=தரவு_கோப்புரை
        )

    @property
    def கோப்பு_பாதை(தன்) -> str:
        return os.path.join(தன்.தரவு_கோப்புரை, தன்.பெயர், தன்.உள்_கோப்பு_பாதை)

    @property
    def ஜிப்_பாதை(தன்) -> str:
        return os.path.join(தன்.தரவு_கோப்புரை, தன்.பெயர்)

    @property
    def கோப்புரை_பாதை(தன்) -> str:
        return os.path.join(தன்.தரவு_கோப்புரை, os.path.splitext(தன்.பெயர்)[0])

    def பதிவேற்கு(தன்):
        if not os.path.isfile(தன்.கோப்பு_பாதை):
            if not os.path.isfile(தன்.ஜிப்_பாதை):
                with NamedTemporaryFile() as தற்காலிகமானது:
                    with requests.get(தன்.பதிவிறக்க_முகவரி, stream=True) as கோரிக்கை:
                        கோரிக்கை.raise_for_status()

                        for chunk in கோரிக்கை.iter_content():
                            if chunk:
                                தற்காலிகமானது.write(chunk)

                    shutil.move(தற்காலிகமானது.name, தன்.ஜிப்_பாதை)
            நீட்டி = os.path.splitext(தன்.ஜிப்_பாதை)[1]
            if நீட்டி == ".rar":
                with RarFile(தன்.ஜிப்_பாதை) as ரார்_கோப்பு:
                    ரார்_கோப்பு.extractall(தன்.கோப்புரை_பாதை)
            else:
                with ZipFile(தன்.ஜிப்_பாதை) as ஜிப்:
                    ஜிப்.extractall(தன்.கோப்புரை_பாதை)

        return தன்.கோப்பு_பாதை

    def நீக்கு(தன்):
        if os.path.exists(தன்.கோப்புரை_பாதை):
            shutil.rmtree(தன்.கோப்புரை_பாதை)

        if os.path.exists(தன்.ஜிப்_பாதை):
            os.remove(தன்.ஜிப்_பாதை)
