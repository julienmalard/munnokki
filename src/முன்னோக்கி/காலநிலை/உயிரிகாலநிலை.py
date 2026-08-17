from typing import Literal, Iterable, List, Tuple, Optional

import xarray as xr

from .காலநிலை import காலநிலை_குறிப்பு
from .மாறிலிகள் import வறலாற்று_காட்சி, காலநிலை_மாதிரி_அச்சு, காலநிலை_மாறி_அச்சு
from ...முன்னோக்கி.காலநிலை.காலநிலை import காலநிலை
from ...முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம், ஜிப்_பதிவிறக்கம்


கிடைக்கும்_துல்லியங்கள் = Literal["30s", "2.5m", "5m", "10m"]


class உயிரிகாலநிலை(காலநிலை):
    """https://www.worldclim.org/data/bioclim.html"""

    def __init__(
        தன், துல்லியம்: கிடைக்கும்_துல்லியங்கள் = "30s", தரவு_கோப்புரை: Optional[str] = None
    ):
        super().__init__(தரவு_கோப்புரை)
        தன்.துல்லியம் = துல்லியம்

    @property
    def மாதிரிகள்(தன்):
        return {
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
        }

    @property
    def காட்சிகள்(தன்):
        return {"ssp126", "ssp245", "ssp370", "ssp585"}

    @property
    def ஆதறிக்கப்பட்ட_ஆண்டுகள்(தன்) -> Tuple[int, int]:
        return 2021, 2100

    @property
    def மாறிகள்(தன்):
        return {
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
        }

    def தரவுகளைப்_பெறு(தன், குறிப்பு: காலநிலை_குறிப்பு) -> xr.DataArray:
        சரிபார்த்த_குறிப்பு = தன்.காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)
        காட்சி = சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி
        மாதிரிகள் = சரிபார்த்த_குறிப்பு.மாதிரிகள்

        தரவுகள்: None | xr.DataArray = None
        for மாதிரி in மாதிரிகள்:
            for மாறி in தன்.மாறிகள்:
                if (மாதிரி == "GFDL-ESM4" and காட்சி in ["ssp245", "ssp585"]) or (
                    மாதிரி in ["FIO-ESM-2-0", "HadGEM3-GC31-LL"] and காட்சி == "ssp370"
                ):
                    # இந்த தகவல்கள் கிடைக்காது - https://www.worldclim.org/data/cmip6/cmip6_clim30s.html
                    continue

                முகவரி = தன்.பதிவிறக்க_முகவரியைப்_பெறு(
                    ஆண்டு=சரிபார்த்த_குறிப்பு.ஆண்டு, மாதிரி=மாதிரி, மாறி=மாறி, காட்சி=காட்சி
                )
                பெற்ற_தரவுகள் = (
                    பதிவிறக்கம்(முகவரி, தரவு_கோப்புரை=தன்.தரவு_கோப்புரை)
                    .தரவுத்தளத்தைப்_பெறு()
                    .expand_dims(
                        {
                            காலநிலை_மாறி_அச்சு: [மாறி],
                            காலநிலை_மாதிரி_அச்சு: [மாதிரி],
                        }
                    )
                )["variable"]
                if தரவுகள் is None:
                    தரவுகள் = பெற்ற_தரவுகள்
                else:
                    தரவுகள் = தரவுகள்.merge(பெற்ற_தரவுகள்)

            if காட்சி == வறலாற்று_காட்சி:
                if தரவுகள் is None:
                    raise ValueError

                தரவுகள்.squeeze(காலநிலை_மாதிரி_அச்சு)
                break

        if தரவுகள் is None:
            raise ValueError

        return தரவுகள்

    def பதிவிறக்க_முகவரியைப்_பெறு(தன், ஆண்டு: int, மாதிரி: str, மாறி: str, காட்சி: str) -> str:
        if காட்சி == வறலாற்று_காட்சி:
            return f"https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_{தன்.துல்லியம்}_bio.zip"

        ஆண்டு_இடைவெளிகள் = [(2021, 2040), (2041, 2060), (2061, 2080), (2081, 2100)]
        ஆண்டுகள் = "-".join(next(str(ஆ) for ஆ in ஆண்டு_இடைவெளிகள் if ஆ[0] <= ஆண்டு <= ஆ[1]))
        return f"https://geodata.ucdavis.edu/cmip6/{தன்.துல்லியம்}/{மாதிரி}/{காட்சி}/wc2.1_{தன்.துல்லியம்}_bioc_{மாதிரி}_{காட்சி}_{ஆண்டுகள்[0]}-{ஆண்டுகள்[1]}.tif"
