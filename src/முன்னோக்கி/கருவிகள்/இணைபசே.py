import os.path
from numbers import Real
from tempfile import NamedTemporaryFile
from typing import Optional, Iterable

import numpy as np
import xarray as xr
from soilgrids import SoilGrids

from .பதிவிறக்கம் import வேர்_கோப்புரை_உருவாக்கு
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு


class இணைபசே:
    """இணைய பரவு சேவை"""

    def __init__(தன், வரைப்படம்: str, அடையாளம்: str, தரவு_கோப்புரை: str, கட்ட_அளவு=(20, 20)):
        தன்.வரைப்படம் = வரைப்படம்
        தன்.அடையாளம் = அடையாளம்
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை
        தன்.கட்ட_அளவு = கட்ட_அளவு

        தன்.சேவை = SoilGrids()

        wcs, coverage_list = தன்.சேவை._get_service_and_coverage_list(தன்.வரைப்படம்)
        தன்.ஆதறவு = தன்.சேவை._get_coverage_obj(wcs, coverage_list, தன்.அடையாளம்)

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

    def கட்டத்_தரவுகளைப்_பெறு(தன், கட்டம்: tuple[Real, Real]) -> str | None:
        கட்ட_கோப்பு_பெயர் = os.path.join(
            str(தன்.தரவு_கோப்புரை),
            "SOILGRIDS",
            தன்.வரைப்படம்,
            தன்.அடையாளம்,
            "_".join([str(இ) for இ in கட்டம்]) + ".nc",
        )
        if os.path.isfile(கட்ட_கோப்பு_பெயர்):
            return கட்ட_கோப்பு_பெயர்
        else:
            தேற்கு, மேற்கு = கட்டம்
            கிழக்கு = மேற்கு+ தன்.கட்ட_அளவு[1]
            வடக்கு = தேற்கு + தன்.கட்ட_அளவு[0]

            வரும்பு = தன்.ஆதறவு.boundingBoxWGS84
            மேற்கு = max(வரும்பு[0], மேற்கு)
            தேற்கு = max(வரும்பு[1], தேற்கு)
            கிழக்கு = min(வரும்பு[2], கிழக்கு)
            வடக்கு = min(வரும்பு[3], வடக்கு)
            if மேற்கு >= கிழக்கு or வடக்கு <= தேற்கு:
                return None

            with NamedTemporaryFile(suffix=".tif") as தற்காலிகமானது:
                பதில் = தன்.சேவை.get_coverage_data(
                    service_id=தன்.வரைப்படம்,
                    coverage_id=தன்.அடையாளம்,
                    west=மேற்கு,
                    south=தேற்கு,
                    east=கிழக்கு,
                    north=வடக்கு,
                    width=500 * (கிழக்கு - மேற்கு),
                    height=500 * (வடக்கு - தேற்கு),
                    crs="urn:ogc:def:crs:EPSG::4326",
                    output=தற்காலிகமானது.name,
                )

                பதில் = xr.where(பதில் == பதில்.attrs["_FillValue"], np.nan, பதில்)
                if பதில்.count().values:

                    தரவுகள் = (பதில்.rename(
                        {
                            "x": நெட்டாங்கு_அச்சு,
                            "y": அகலாங்கு_அச்சு,
                        }
                    ).squeeze("band").drop_vars(["band", "spatial_ref"]))
                else:
                    # காலியான தரவுகளுக்காக நினைவகத்தில் இடம் எடுக்க கூடாது
                    தரவுகள் = xr.DataArray(coords={நெட்டாங்கு_அச்சு: மேற்கு, அகலாங்கு_அச்சு: தேற்கு})

                தரவுகள்.name = தன்.அடையாளம்

                வேர்_கோப்புரை_உருவாக்கு(கட்ட_கோப்பு_பெயர்)

                தரவுகள்.to_netcdf(கட்ட_கோப்பு_பெயர்)

            return கட்ட_கோப்பு_பெயர்
