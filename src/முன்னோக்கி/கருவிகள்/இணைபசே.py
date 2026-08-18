import os.path
from numbers import Number, Real
from typing import Optional, Iterable

import numpy as np
import xarray as xr
from soilgrids import SoilGrids

from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு


class இணைபசே:
    """இணைய பரவு சேவை"""

    def __init__(தன், வரைப்படம்: str, அடையாளம்: str, தரவு_கோப்புரை: str, கட்ட_அளவு=(20, 20)):
        தன்.வரைப்படம் = வரைப்படம்
        தன்.அடையாளம் = அடையாளம்
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை
        தன்.கட்ட_அளவு = கட்ட_அளவு

        தன்.சேவை = SoilGrids()

    def கட்டங்கள்(தன்) -> Iterable[tuple[Real, Real]]:
        for அக in range(-90, 90 + தன்.கட்ட_அளவு[0], தன்.கட்ட_அளவு[0]):
            for நெ in range(-180, 180 + தன்.கட்ட_அளவு[1], தன்.கட்ட_அளவு[1]):
                yield அக, நெ

    def தரவுகளைப்_பெறு(தன், மறை: Optional[xr.DataArray] = None) -> xr.DataArray:
        தரவுகள் = xr.DataArray(
            np.nan,
            coords={
                அகலாங்கு_அச்சு: np.arange(-90, 90, தன்.கட்ட_அளவு[0]),
                நெட்டாங்கு_அச்சு: np.arange(-180, 180, தன்.கட்ட_அளவு[1]),
            },
            dims=[
                நெட்டாங்கு_அச்சு,
                அகலாங்கு_அச்சு,
            ],
            name=தன்.அடையாளம்,
        )
        for கட்டம் in தன்.கட்டங்கள்():
            # இந்த கட்டத்தில் மறைக்கப்படாத புள்ளிகள் இருந்தால்
            if கட்டம்[மறை]:
                கட்டத்_தரவுகள் = தன்.கட்டத்_தரவுகளைப்_பெறு(கட்டம்)
                தரவுகள்.fillna(கட்டத்_தரவுகள்)

        return தரவுகள்

    def கட்டத்_தரவுகளைப்_பெறு(தன், கட்டம்: tuple[Real, Real]) -> xr.DataArray:
        if os.path.isfile(கோப்பு_பெயர்):
            தரவுகள் = xr.open_dataarray(கோப்பு_பெயர், chunks="auto")
        else:
            data = தன்.சேவை.get_coverage_data(
                service_id=தன்.வரைப்படம்,
                coverage_id=தன்.அடையாளம்,
                west=கட்டம்[0],
                south=கட்டம்[1],
                east=கட்டம்[0] + தன்.கட்ட_அளவு[1],
                north=கட்டம்[1] + தன்.கட்ட_அளவு[0],
                width=500 * தன்.கட்ட_அளவு[1],
                height=500 * தன்.கட்ட_அளவு[0],
                crs="urn:ogc:def:crs:EPSG::4326",
                output="test latlon.tif",
            )
            xr.where(data == 255, np.nan, data).plot(figsize=(9, 5), vmin=0)

            திஃப_கோப்பு_பெயர்
            with open(திஃப_கோப்பு_பெயர், "wb") as கோப்பு:
                கோப்பு.write(பதில்.read())

            தரவுகள் = (
                xr.open_dataarray(திஃப_கோப்பு_பெயர்)
                .rio.write_crs("ESRI:54052")
                .rio.reproject("EPSG:4326")
                .rename(
                    {
                        "x": நெட்டாங்கு_அச்சு,
                        "y": அகலாங்கு_அச்சு,
                    }
                )
                .squeeze("band")
                .drop_vars(["band", "spatial_ref"])
            )
            தரவுகள்.to_netcdf(கோப்பு_பெயர்)

            os.remove(திஃப_கோப்பு_பெயர்)

        return தரவுகள்
