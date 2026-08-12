from typing import Literal, Iterable, List, Tuple

import xarray as xr

from .காலநிலை import காலநிலை_குறிப்பு
from ...முன்னோக்கி.காலநிலை.காலநிலை import காலநிலை
from ...முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம், ஜிப்_பதிவிறக்கம்


கிடைக்கும்_துல்லியங்கள் = Literal["30s", "2.5m", "5m", "10m"]


class உயிரிகாலநிலை(காலநிலை):
    """https://www.worldclim.org/data/bioclim.html"""

    def __init__(
        தன்,
        துல்லியம்: கிடைக்கும்_துல்லியங்கள் = "30s",
    ):
        தன்.துல்லியம் = துல்லியம்

    @property
    def மாதிரிகள்(தன்) -> List[str]:
        return [
            "ACCESS-CM2",
            "BCC-CSM2-MR",
            "CMCC-ESM2",
            "EC-Earth3-Veg",
            "FIO-ESM-2-0",
            "GFDL-ESM4",
            "GISS-E2-1-G",
            "HadGEM3-GC31-LL",
            "INM-CM5-0",
            "IPSL-CM6A-LR",
            "MIROC6",
            "MPI-ESM1-2-HR",
            "MRI-ESM2-0	tn",
            "UKESM1-0-LL",
        ]

    @property
    def காட்சிகள்(தன்) -> List[str]:
        return ["ssp126", "ssp245", "ssp370", "ssp585"]

    @property
    def ஆதறிக்கப்பட்ட_ஆண்டுகள்(தன்) -> Tuple[int, int]:
        return 2021, 2100

    @property
    def மாறிகள்(தன்) -> List[str]:
        return [
            "BIO1",
            "BIO2",
            "BIO3",
            "BIO4",
            "BIO5",
            "BIO6",
            "BIO7",
            "BIO8",
            "BIO9",
            "BIO10",
            "BIO11",
            "BIO12",
            "BIO13",
            "BIO14",
            "BIO15",
            "BIO16",
            "BIO17",
            "BIO18",
            "BIO19",
        ]

    def தரவுகளைப்_பெறு(தன், குறிப்பு: காலநிலை_குறிப்பு) -> xr.DataArray:
        return xr.merge(
            பதிவிறக்கம்(பெயர், பதிவிறக்க_முகவரி=முகவரி).பெறு()
            for முகவரி in தன்.பதிவிறக்க_முகவரியைப்_பெறு()
        )

    def வறலாற்று_தகவள்களைப்_பெறு(தன்) -> xr.DataArray:
        முகவரி = f"https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_{தன்.துல்லியம்}_bio.zip"
        ப = ஜிப்_பதிவிறக்கம்(பெயர், பதிவிறக்க_முகவரி=முகவரி)
        return ப.பெறு()

    def பதிவிறக்க_முகவரியைப்_பெறு(தன்) -> Iterable[str]:
        try:
            ஆண்டுகள் = next(
                இடைவெளி
                for இடைவெளி in இடைவெளிகள்
                if இடைவெளி[0] <= தன்.சூழ்நிலை.ஆண்டு <= இடைவெளி[1]
            )
        except StopIteration:
            raise ValueError(
                f"{தன்.சூழ்நிலை.ஆண்டு} என்று ஆண்டு இந்த மாதிரியால் ஆதறவிக்கப்பட்ட தேதிகளுக்கு வெளியே உள்ளது."
            )

        for மாதிரி in தன்.சூழ்நிலை.மாதிரி:
            if (
                மாதிரி == "GFDL-ESM4" and தன்.சூழ்நிலை.காலநிலைக்காட்சி in ["ssp245", "ssp585"]
            ) or (
                மாதிரி in ["FIO-ESM-2-0", "HadGEM3-GC31-LL"]
                and தன்.சூழ்நிலை.காலநிலைக்காட்சி == "ssp370"
            ):
                # இந்த தகவல்கள் கிடைக்காது - https://www.worldclim.org/data/cmip6/cmip6_clim30s.html
                continue

            yield f"https://geodata.ucdavis.edu/cmip6/{தன்.துல்லியம்}/{மாதிரி}/{தன்.சூழ்நிலை.காலநிலைக்காட்சி}/wc2.1_{தன்.துல்லியம்}_bioc_{மாதிரி}_{தன்.சூழ்நிலை.காலநிலைக்காட்சி}_{ஆண்டுகள்[0]}-{ஆண்டுகள்[1]}.tif"
