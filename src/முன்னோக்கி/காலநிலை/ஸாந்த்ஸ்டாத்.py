import json
import os.path
from datetime import datetime
from hashlib import md5
from typing import Optional
from zipfile import ZipFile

import cdsapi
import numpy as np
import xarray as xr
from caseutil.cases import to_snake
from xarray_regrid import Grid

from .காலநிலை import காலநிலை, காலநிலை_குறிப்பு, சரிபார்த்த_காலநிலை_குறிப்பு
from .மாறிலிகள் import வறலாற்று_காட்சி, காலநிலை_மாதிரி_அச்சு, காலநிலை_மாறி_அச்சு
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு


class ஸாந்த்ஸ்டாத்(காலநிலை):
    """
    Copernicus Climate Change Service (2022): Climate extreme indices and heat stress indicators derived from CMIP6 global climate projections. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.776e08bd
    https://cds.climate.copernicus.eu/datasets/sis-extreme-indices-cmip6?tab=overview
    http://dast.data.compute.cci2.ecmwf.int/documents/sis-extreme-indicators/C3S_COP69_ETCCDI-HSI_product-user-guide_v3-1.pdf

    """

    def __init__(
        தன்,
        மாறிகள்: Optional[set[str]] = None,
        துல்லியம்=(0.5, 0.5),
        கால_இடைவெளி=10,
        தரவு_கோப்புரை: Optional[str] = None,
        வாடிக்கையாளர்: Optional[cdsapi.Client] = None,
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)

        தன்._மாறிகள் = மாறிகள் or {
            "TX10p",
            "CWD",
            "GSL",
            "Rx5day",
            "TNn",
            "PRCPTOT",
            "TX90p",
            "TN10p",
            "DTR",
            "R10mm",
            "TXx",
            "R1mm",
            "TR",
            "TN90p",
            "CSDI",
            "R99p",
            "ID",
            "TXn",
            "SDII",
            "R20mm",
            "WSDI",
            "CDD",
            "FD",
            "Rx1day",
            "TNx",
            "SU",
            "R95p",
        }
        தன்.துல்லியம் = துல்லியம்
        தன்.கால_இடைவெளி = கால_இடைவெளி
        தன்.வாடிக்கையாளர் = வாடிக்கையாளர் or cdsapi.Client()

    @property
    def மாதிரிகள்(தன்):
        return {
            "ACCESS-CM2",
            "ACCESS-ESM1-5",
            "BCC-CSM2-MR",
            "CNRM-CM6-1",
            "CNRM-CM6-1-HR",
            "CNRM-ESM2-1",
            "CanESM5",
            "EC-Earth3",
            "EC-Earth3-Veg",
            "FGOALS-g3",
            "GFDL-CM4",
            "GFDL-ESM4",
            "HadGEM3-GC31-LL",
            "HadGEM3-GC31-MM",
            "INM-CM4-8",
            "INM-CM5-0",
            "KACE-1-0-G",
            "KIOST-ESM",
            "MIROC-ES2L",
            "MIROC6",
            "MPI-ESM1-2-HR",
            "MPI-ESM1-2-LR",
            "MRI-ESM2-0",
            "NESM3",
            "NorESM2-LM",
            "NorESM2-MM",
            "UKESM1-0-LL",
        }

    @property
    def காட்சிகள்(தன்):
        return {"ssp126", "ssp245", "ssp370", "ssp585"}

    @property
    def ஆதறிக்கப்பட்ட_ஆண்டுகள்(தன்):
        return 2015, 2100

    @property
    def மாறிகள்(தன்):
        return தன்._மாறிகள்

    def காலநிலை_குறிப்பு_சரிபார்த்தல்(தன், குறிப்பு: காலநிலை_குறிப்பு):
        சரிபார்த்த_குறிப்பு = super().காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)
        காலநிலைக்காட்சி = சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி

        மாதிரிகள் = {
            மாதிரி
            for மாதிரி in சரிபார்த்த_குறிப்பு.மாதிரிகள்
            if not (
                (
                    மாதிரி in ["CNRM-CM6-1-HR", "HadGEM3-GC31-MM"]
                    and காலநிலைக்காட்சி in ["ssp245", "ssp370"]
                )
                or (
                    மாதிரி == "GFDL-CM4"
                    and காலநிலைக்காட்சி in ["ssp126", "ssp370"]
                ) or (
                    மாதிரி in ["HadGEM3-GC31-LL", "KIOST-ESM", "NESM3"] and காலநிலைக்காட்சி == "ssp370"
                )
            )
        }

        சரிபார்த்த_குறிப்பு = சரிபார்த்த_காலநிலை_குறிப்பு(
            ஆண்டு=சரிபார்த்த_குறிப்பு.ஆண்டு,
            காலநிலைக்காட்சி=சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி,
            மாதிரிகள்=மாதிரிகள்,
        )

        return சரிபார்த்த_குறிப்பு

    def தரவுகளைப்_பெறு(தன், குறிப்பு: காலநிலை_குறிப்பு) -> xr.DataArray:

        சரிபார்த்த_குறிப்பு = தன்.காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)
        காட்சி = சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி
        மாதிரிகள் = சரிபார்த்த_குறிப்பு.மாதிரிகள்
        ஆண்டு = சரிபார்த்த_குறிப்பு.ஆண்டு

        தரவுகள் = xr.DataArray(
            np.nan,
            coords={
                காலநிலை_மாறி_அச்சு: தன்.மாறிகள்,
                காலநிலை_மாதிரி_அச்சு: மாதிரிகள்,
                அகலாங்கு_அச்சு: np.arange(-90, 90, தன்.துல்லியம்[0]),
                நெட்டாங்கு_அச்சு: np.arange(-180, 180, தன்.துல்லியம்[1]),
            },
            dims=[
                காலநிலை_மாறி_அச்சு,
                காலநிலை_மாதிரி_அச்சு,
                அகலாங்கு_அச்சு,
                நெட்டாங்கு_அச்சு,
            ],
        )

        for மாதிரி in மாதிரிகள்:
            கோரிக்கை = தன்.கோரிக்கையைப்_பெறு(மாதிரி=மாதிரி, காட்சி=காட்சி)
            கோப்பு_பாதை = os.path.join(
                தன்.தரவு_கோப்புரை,
                f"{md5(json.dumps(கோரிக்கை, sort_keys=True, ensure_ascii=False).encode()).hexdigest()}.zip",
            )
            if not os.path.isfile(கோப்பு_பாதை):
                தன்.வாடிக்கையாளர்.retrieve(
                    "sis-extreme-indices-cmip6", கோரிக்கை, target=கோப்பு_பாதை
                )

            ஆரம்ப_ஆண்டு = max(தன்.ஆதறிக்கப்பட்ட_ஆண்டுகள்[0], ஆண்டு - தன்.கால_இடைவெளி // 2)
            இறுதியான_ஆண்டு = min(தன்.ஆதறிக்கப்பட்ட_ஆண்டுகள்[1], ஆரம்ப_ஆண்டு + தன்.கால_இடைவெளி)
            நேர_இடைவெளி = slice(
                datetime(year=ஆரம்ப_ஆண்டு, month=1, day=1),
                datetime(year=இறுதியான_ஆண்டு, month=1, day=1),
            )
            மூல்_பாதை = str(os.path.splitext(கோப்பு_பாதை)[0])
            for மாறி in தன்.மாறிகள்:
                மாறி_கோப்பு_பாதை = next((os.path.join(மூல்_பாதை, கோப்பு) for கோப்பு in os.listdir(மூல்_பாதை) if கோப்பு.startswith(f"{மாறி.lower()}ETCCDI")), None)
                if not மாறி_கோப்பு_பாதை:
                    with ZipFile(கோப்பு_பாதை, "r") as ஜிப்:
                        பெயர் = next(பெயர் for பெயர் in ஜிப்.namelist() if பெயர்.startswith(f"{மாறி.lower()}ETCCDI"))
                        மாறி_கோப்பு_பாதை = os.path.join(மூல்_பாதை, பெயர்)
                        ஜிப்.extract(பெயர், மாறி_கோப்பு_பாதை)

                மாறி_தரவுகள் = (
                    xr.open_dataset(மாறி_கோப்பு_பாதை)[f"{மாறி.lower()}ETCCDI"]
                    .sel({"time": நேர_இடைவெளி})
                    .mean(dim=["time"])
                )

                வடிவமைத்த_மாறி_தரவுகள் = மாறி_தரவுகள்.regrid.linear(
                    Grid(
                        **{
                            "north": 90,
                            "east": 180,
                            "south": -90,
                            "west": -180,
                            "resolution_lat": தன்.துல்லியம்[0],
                            "resolution_lon": தன்.துல்லியம்[1],
                        }
                    ).create_regridding_dataset()
                ).rename(
                    {
                        "lat": அகலாங்கு_அச்சு,
                        "lon": நெட்டாங்கு_அச்சு,
                    }
                )
                தரவுகள்.fillna(வடிவமைத்த_மாறி_தரவுகள்)

        return தரவுகள்

    def கோரிக்கையைப்_பெறு(தன், மாதிரி: str, காட்சி: str):
        காட்சி_குறிப்பு = (
            "historical" if காட்சி == வறலாற்று_காட்சி else காட்சி[:-3] + "_".join(காட்சி[-3:])
        )

        return {
            "variable": [மாறி_தகவல்கள்[மாறி]["பெயர்"] for மாறி in தன்.மாறிகள்],
            "product_type": [
                "base_period_1961_1990",
                "base_period_1981_2010",
                "base_independent",
            ],
            "model": [to_snake(மாதிரி)],
            "ensemble_member": ["r1i1p1f1"],
            "experiment": [காட்சி_குறிப்பு],
            "temporal_aggregation": ["yearly"],
            "period": ["2015_2100"],
            "version": ["2_0"],
        }


மாறி_தகவல்கள் = {
    "TX10p": {"பெயர்": "cold_days"},
    "CWD": {"பெயர்": "consecutive_wet_days"},
    "GSL": {"பெயர்": "growing_season_length"},
    "Rx5day": {"பெயர்": "maximum_5_day_precipitation"},
    "TNn": {"பெயர்": "minimum_value_of_daily_minimum_temperature"},
    "PRCPTOT": {"பெயர்": "total_wet_day_precipitation"},
    "TX90p": {"பெயர்": "warm_days"},
    "TN10p": {"பெயர்": "cold_nights"},
    "DTR": {"பெயர்": "diurnal_temperature_range"},
    "R10mm": {"பெயர்": "heavy_precipitation_days"},
    "TXx": {"பெயர்": "maximum_value_of_daily_maximum_temperature"},
    "R1mm": {"பெயர்": "number_of_wet_days"},
    "TR": {"பெயர்": "tropical_nights"},
    "TN90p": {"பெயர்": "warm_nights"},
    "CSDI": {"பெயர்": "cold_spell_duration_index"},
    "R99p": {"பெயர்": "extremely_wet_day_precipitation"},
    "ID": {"பெயர்": "ice_days"},
    "TXn": {"பெயர்": "minimum_value_of_daily_maximum_temperature"},
    "SDII": {"பெயர்": "simple_daily_intensity_index"},
    "R20mm": {"பெயர்": "very_heavy_precipitation_days"},
    "WSDI": {"பெயர்": "warm_spell_duration_index"},
    "CDD": {"பெயர்": "consecutive_dry_days"},
    "FD": {"பெயர்": "frost_days"},
    "Rx1day": {"பெயர்": "maximum_1_day_precipitation"},
    "TNx": {"பெயர்": "maximum_value_of_daily_minimum_temperature"},
    "SU": {"பெயர்": "summer_days"},
    "R95p": {"பெயர்": "very_wet_day_precipitation"},
}
