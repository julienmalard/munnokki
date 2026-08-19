import os
from logging import warning
from typing import Literal, Optional

import numpy as np
import xarray as xr
from pybtex.database import Entry

from .காலநிலை import காலநிலை, காலநிலை_குறிப்பு, சரிபார்த்த_காலநிலை_குறிப்பு
from .மாறிலிகள் import வறலாற்று_காட்சி, காலநிலை_மாறி_அச்சு
from ..கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்

கிடைக்கும்_துல்லியங்கள் = Literal["0.00833333", "0.1", "0.5", "1.0"]


class கப்பென்_ஜைகர்(காலநிலை):
    """
    https://www.nature.com/articles/s41597-023-02549-6
    https://koppen.earth/

    """

    def __init__(
        தன்,
        தரவு_திறன்=0,
        துல்லியம்: கிடைக்கும்_துல்லியங்கள் = "0.1",
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/21789074/versions/2",
        தரவு_கோப்புரை: Optional[str] = None,
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)
        தன்.தரவு_திறன் = தரவு_திறன்
        தன்.துல்லியம் = துல்லியம்
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    @property
    def மாதிரிகள்(தன்) -> set[str]:
        return {
            "ACCESS-CM2",
            "ACCESS-ESM1-5",
            "AWI-CM-1-1-MR",
            "AWI-ESM-1-1-LR",
            "BCC-CSM2-MR",
            "BCC-ESM1",
            "CAMS-CSM1-0",
            "CESM2-FV2",
            "CESM2-WACCM",
            "CESM2-WACCM-FV2",
            "CMCC-CM2-HR4",
            "CMCC-CM2-SR5",
            "CMCC-ESM2",
            "CNRM-CM6-1",
            "CNRM-CM6-1-HR",
            "CNRM-ESM2-1",
            "EC-Earth3-AerChem",
            "FGOALS-f3-L",
            "FGOALS-g3",
            "GFDL-CM4",
            "GFDL-ESM4",
            "GISS-E2-1-G",
            "GISS-E2-1-G-CC",
            "GISS-E2-1-H",
            "GISS-E2-2-G",
            "GISS-E2-2-H",
            "IITM-ESM",
            "INM-CM4-8",
            "INM-CM5-0",
            "IPSL-CM5A2-INCA",
            "MCM-UA-1-0",
            "MIROC-ES2H",
            "MIROC-ES2L",
            "MIROC6",
            "MPI-ESM-1-2-HAM",
            "MPI-ESM1-2-HR",
            "MPI-ESM1-2-LR",
            "MRI-ESM2-0",
            "NorCPM1",
            "NorESM2-LM",
            "NorESM2-MM",
            "SAM0-UNICON",
        }

    @property
    def காட்சிகள்(தன்) -> set[str]:
        return {"ssp119", "ssp126", "ssp245", "ssp370", "ssp434", "ssp460", "ssp585"}

    @property
    def ஆதறிக்கப்பட்ட_ஆண்டுகள்(தன்) -> tuple[int, int]:
        return 2041, 2099

    @property
    def மாறிகள்(தன்) -> set[str]:
        return {"kg_class"}

    def தரவுகளைப்_பெறு(தன், குறிப்பு: காலநிலை_குறிப்பு) -> xr.DataArray:
        சரிபார்த்த_குறிப்பு = தன்.காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)
        காட்சி = சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி
        ஆண்டு = சரிபார்த்த_குறிப்பு.ஆண்டு

        தரவுகள் = ஜிப்_பதிவிறக்கம்(
            உள்_கோப்பு_பாதை=தன்.உள்_கோப்பு_பாதை(ஆண்டு, காட்சி=காட்சி),
            பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
            தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
        ).தரவுத்தளத்தைப்_பெறு()

        if காட்சி != வறலாற்று_காட்சி:
            தரவுகள் = தன்.வடிக்க(தரவுகள்)

        return தரவுகள்["kg_class"].expand_dims({காலநிலை_மாறி_அச்சு: ["காலநிலை வகை"]})

    def காலநிலை_குறிப்பு_சரிபார்த்தல்(தன், குறிப்பு: காலநிலை_குறிப்பு) -> சரிபார்த்த_காலநிலை_குறிப்பு:
        சரிபார்த்த_குறிப்பு = super().காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)

        if சரிபார்த்த_குறிப்பு.மாதிரிகள் != தன்.மாதிரிகள்:
            warning(
                "இந்த காலநிலை தாளில் தனி மாதிரிகளைக் குறிப்பிட முடியாது. அனைத்த மாதிரிகள் பயன்படுத்தபடும்."
            )
            சரிபார்த்த_குறிப்பு = சரிபார்த்த_காலநிலை_குறிப்பு(
                ஆண்டு=சரிபார்த்த_குறிப்பு.ஆண்டு,
                காலநிலைக்காட்சி=சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி,
                மாதிரிகள்=set(தன்.மாதிரிகள்),
            )

        return சரிபார்த்த_குறிப்பு

    def தொலைவு(
        தன், இலக்கு_மாறிகள்: xr.DataArray, மூல்_காலநிலை_குறிப்பு: xr.DataArray
    ) -> xr.DataArray:
        return xr.where(இலக்கு_மாறிகள் == மூல்_காலநிலை_குறிப்பு, 1, 0)

    def உள்_கோப்பு_பாதை(தன், ஆண்டு: int, காட்சி: str) -> str:
        துல்லிய_குறிப்பு = தன்.துல்லியம்.replace(".", "p")
        if காட்சி == வறலாற்று_காட்சி:
            return os.path.join("1991_2020", f"koppen_geiger_{துல்லிய_குறிப்பு}.nc")

        ஆண்டு_இடைவெளிகள் = [(2041, 2070), (2071, 2099)]
        ஆண்டு_குறிப்பு = "_".join(
            next(str(ஆ) for ஆ in ஆண்டு_இடைவெளிகள் if ஆ[0] <= ஆண்டு <= ஆ[1])
        )

        return os.path.join(ஆண்டு_குறிப்பு, காட்சி, f"koppen_geiger_{துல்லிய_குறிப்பு}.nc")

    def வடிக்க(தன், தரவுகள்: xr.Dataset) -> xr.Dataset:
        தரவுகள்["kg_class"] = xr.where(
            தரவுகள்["kg_confidence"] >= தன்.தரவு_திறன், தரவுகள்["kg_class"], np.nan
        )
        return தரவுகள்

    def மேற்கோள்(தன்) -> list[Entry]:

