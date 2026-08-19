import os.path
from numbers import Real
from tempfile import NamedTemporaryFile
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
        தரவுகள் = []
        for கட்டம் in தன்.கட்டங்கள்():
            # இந்த கட்டத்தில் மறைக்கப்படாத புள்ளிகள் இருந்தால்
            if (
                not மறை
                or மறை.sel(
                    {
                        அகலாங்கு_அச்சு: slice(கட்டம்[0], கட்டம்[0] + தன்.கட்ட_அளவு[0]),
                        நெட்டாங்கு_அச்சு: slice(கட்டம்[1], கட்டம்[1] + தன்.கட்ட_அளவு[1]),
                    }
                ).sum()
            ):
                தரவுகள்.append(தன்.கட்டத்_தரவுகளைப்_பெறு(கட்டம்))

        return xr.open_mfdataset(தரவுகள்)[தன்.அடையாளம்]

    def கட்டத்_தரவுகளைப்_பெறு(தன், கட்டம்: tuple[Real, Real]) -> str:
        கட்ட_கோப்பு_பெயர் = os.path.join(
            தன்.தரவு_கோப்புரை,
            "SOILGRIDS",
            தன்.வரைப்படம்,
            தன்.அடையாளம்,
            "_".join([str(இ) for இ in கட்டம்]) + ".nc",
        )
        if os.path.isfile(கட்ட_கோப்பு_பெயர்):
            return கட்ட_கோப்பு_பெயர்
        else:
            பதில் = தன்.சேவை.get_coverage_data(
                service_id=தன்.வரைப்படம்,
                coverage_id=தன்.அடையாளம்,
                west=கட்டம்[1],
                south=கட்டம்[0],
                east=கட்டம்[1] + தன்.கட்ட_அளவு[1],
                north=கட்டம்[0] + தன்.கட்ட_அளவு[0],
                width=500 * தன்.கட்ட_அளவு[1],
                height=500 * தன்.கட்ட_அளவு[0],
                crs="urn:ogc:def:crs:EPSG::4326",
                output="test latlon.tif",
            )
            பதில் = xr.where(பதில் == 255, np.nan, பதில்)

            with NamedTemporaryFile() as திஃப_கோப்பு:
                திஃப_கோப்பு.write(பதில்.read())

                தரவுகள் = (
                    xr.open_dataarray(திஃப_கோப்பு.name, chunks="auto")
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
                தரவுகள்.name = தன்.அடையாளம்
                தரவுகள்.to_netcdf(கட்ட_கோப்பு_பெயர்)

            return கட்ட_கோப்பு_பெயர்
