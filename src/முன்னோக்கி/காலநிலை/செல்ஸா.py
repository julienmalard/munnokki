from typing import Optional

import xarray as xr

from முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம்
from முன்னோக்கி.காலநிலை.காலநிலை import காலநிலை, காலநிலை_குறிப்பு
from முன்னோக்கி.காலநிலை.மாறிலிகள் import காலநிலை_மாறி_அச்சு, காலநிலை_மாதிரி_அச்சு


class செல்ஸா_உயிரிகாலநிலை(காலநிலை):
    """
    CHELSA-Bioclim+
    file:///Users/julienmalard/Downloads/chelsa_file_specification_bioclim_plus-1.pdf
    https://www.chelsa-climate.org/datasets/chelsa_bioclim
    https://opendata.swiss/en/dataset/chelsa-bioclim-a-novel-set-of-global-climate-related-predictors-at-kilometre-resolution
    https://envicloud.wsl.ch/#/?bucket=https%3A%2F%2Fos.zhdk.cloud.switch.ch%2Fchelsav2%2F&prefix=%2F
    """

    def __init__(தன், மாறிகள்: Optional[list[str]] = None):
        தன்._மாறிகள் = மாறிகள் or [
            "bio1",
            "bio2",
            "bio3",
            "bio4",
            "bio5",
            "bio6",
            "bio7",
            "bio8",
            "bio9",
            "bio10",
            "bio11",
            "bio12",
            "bio13",
            "bio14",
            "bio15",
            "bio16",
            "bio17",
            "bio18",
            "bio19",
            "fcf",
            "fgd",
            "gdd0",
            "gdd5",
            "gdd10",
            "gddlgd0",
            "gddlgd5",
            "gddlgd10",
            "gddfgd0",
            "gddfgd5",
            "gddfgd10",
            "gsl",
            "gsp",
            "gst",
            "lgd",
            "ngd0",
            "ngd5",
            "ngd10",
            "npp",
            "scd",
            "swe",
        ]

    @property
    def மாதிரிகள்(தன்) -> list[str]:
        return [
            "GFDL-ESM4",
            "IPSL-CM6A-LR",
            "MPI-ESM1-2-HR",
            "MRI-ESM2-0",
            "UKESM1-0-LL",
        ]

    @property
    def காட்சிகள்(தன்) -> list[str]:
        return ["ssp126", "ssp370", "ssp585"]

    @property
    def ஆதறிக்கப்பட்ட_ஆண்டுகள்(தன்) -> tuple[int, int]:
        return 2011, 2100

    @property
    def மாறிகள்(தன்) -> list[str]:
        return தன்._மாறிகள்

    def தரவுகளைப்_பெறு(தன், குறிப்பு: காலநிலை_குறிப்பு) -> xr.DataArray:
        சரிபார்த்த_குறிப்பு = தன்.காலநிலை_குறிப்பு_சரிபார்த்தல்(குறிப்பு)
        காட்சி = சரிபார்த்த_குறிப்பு.காலநிலைக்காட்சி
        மாதிரிகள் = சரிபார்த்த_குறிப்பு.மாதிரி

        தரவுகள்: None | xr.DataArray = None
        for மாறி in தன்.மாறிகள்:
            for மாதிரி in மாதிரிகள்:
                முகவரி = தன்.பதிவிறக்கம்_முகவரி(
                    ஆண்டு=சரிபார்த்த_குறிப்பு.ஆண்டு, மாதிரி=மாதிரி, மாறி=மாறி, காட்சி=காட்சி
                )
                பெற்ற_தரவுகள் = (
                    பதிவிறக்கம்(முகவரி)
                    .பெறு()
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
        if தரவுகள் is None:
            raise ValueError

        return தரவுகள்

    @staticmethod
    def பதிவிறக்கம்_முகவரி(ஆண்டு: int, மாதிரி: str, மாறி: str, காட்சி: str) -> str:
        ஆண்டு_இடைவெளிகள் = [(2011, 2040), (2041, 2070), (2071, 2100)]
        ஆண்டுகள் = "-".join(next(str(ஆ) for ஆ in ஆண்டு_இடைவெளிகள் if ஆ[0] <= ஆண்டு <= ஆ[1]))
        return (
            f"https://os.zhdk.cloud.switch.ch/chelsav2/GLOBAL/climatologies/"
            f"{ஆண்டுகள்}/{மாதிரி}/{காட்சி}/bio/CHELSA_{மாறி}_{ஆண்டுகள்}_{மாதிரி.lower()}_{காட்சி}_V.2.1.tif"
        )


class செல்ஸா_காலநிலை_வகைகள்(செல்ஸா_உயிரிகாலநிலை):
    def __init__(தன், மாறிகள்: Optional[list[str]] = None):
        super().__init__(மாறிகள்=மாறிகள் or [
            "kg0",
            "kg1",
            "kg2",
            "kg3",
            "kg4",
            "kg5",
        ])

    def தொலைவு(
        தன், இலக்கு_மாறிகள்: xr.DataArray, மூல்_காலநிலை_குறிப்பு: xr.DataArray
    ) -> xr.DataArray:
        return (மூல்_காலநிலை_குறிப்பு == இலக்கு_மாறிகள்).all(dim=காலநிலை_மாறி_அச்சு)
