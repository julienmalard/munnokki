from typing import Optional, Literal

import xarray as xr

import பண்புகள் as ப
from .மண் import மண்
from .மாறிலிகள் import மண்_மாறி_அச்சு, மண்_ஆழ_அச்சு
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ..கருவிகள்.இணைபசே import இணைபசே


class மண்கட்டம்(மண்):
    """
    https://soilgrids.org/
    https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html
    https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_02.html
    https://git.wur.nl/isric/soilgrids/soilgrids.notebooks/-/blob/master/03-WCS-2.0.ipynb
    https://git.wur.nl/isric/soilgrids/soilgrids.notebooks/-/blob/master/01-WCS-basics.ipynb?ref_type=heads
    https://git.wur.nl/isric/soilgrids/soilgrids.notebooks/-/blob/master/02-WCS-getExtent.ipynb

    https://soilgrids.readthedocs.io/en/latest/index.html
    https://docs.isric.org/globaldata/soilgrids/webdav_from_Python.html

    Poggio, L., de Sousa, L. M., Batjes, N. H., Heuvelink, G. B. M., Kempen, B., Ribeiro, E., and Rossiter, D.: SoilGrids 2.0: producing soil information for the globe with quantified spatial uncertainty, SOIL, 7, 217–240, 2021. DOI
    """

    ஆழங்கள் = [0, 5, 15, 30, 60, 100, 200]

    def __init__(
        தன், ஆழம்: Optional[list[int | float]] = None, மாறிகள்: Optional[str] = None
    ):
        தன்.மாறிகள் = மாறிகள் or [
            ப.அடர்த்தி,
            ப.நேர்மின்_அயனி_பறிமாற்ற_தன்மை,
            ப.பாறைத்_துண்டங்கள்,
            ப.களிமண்,
            ப.தலைச்சத்து,
            ப.மண்_கரிம_சேர்மம்,
            ப.அமில_காரத்தன்மை,
            ப.மணல்,
            ப.கரம்பை,
            ப.கன_நீர்_இருப்பு_பத்து,
            ப.கன_நீர்_இருப்பு_மூப்பத்துமூன்று,
            ப.கன_நீர்_இருப்பு_ஆயிரத்தியைநூறு,
        ]
        தன்.ஆழம் = ஆழம் or [0, 5, 15, 30, 60, 100]

    def தரவுகளைப்_பெறு(தன், மறை=None):
        தரவு_பட்டியல் = []
        for மாறி in தன்.மாறிகள்:
            மாறி_குறியீடு = தன்.மாறி_குறியீட்டைப்_பெறு(மாறி)
            for ஆழம் in தன்.ஆழங்கள்:
                அடையாளம் = தன்.தரவு_அடையாளத்தைப்_பெறு(மாறி=மாறி, ஆழம்=ஆழம், மதிப்பு="mean")

                மாறி_தரவுகள் = (
                    இணைபசே(
                        வரைப்படம்=மாறி_குறியீடு,
                        அடையாளம்=அடையாளம்,
                    )
                    .தரவுகளைப்_பெறு(மறை)
                    .expand_dims({மண்_மாறி_அச்சு: [மாறி], மண்_ஆழ_அச்சு: [ஆழம்]})
                )
                தரவு_பட்டியல்.append(மாறி_தரவுகள்)

        return xr.concat(தரவு_பட்டியல், dim=மண்_மாறி_அச்சு)

    def தரவு_அடையாளத்தைப்_பெறு(
        தன், மாறி: str, ஆழம்: int, மதிப்பு: Literal["mean", "Q05", "Q50", "Q95"]
    ):
        மாறி_குறிப்பு = தன்.மாறி_குறியீட்டைப்_பெறு(மாறி)
        ஆழம்_வரம்புகள் = next(
            (தன்.ஆழங்கள்[i], தன்.ஆழங்கள்[i + 1])
            for i in range(len(தன்.ஆழங்கள்) - 1)
            if தன்.ஆழங்கள்[i] <= ஆழம் < தன்.ஆழங்கள்[i + 1]
        )

        ஆழ_குறிப்பு = f"{ஆழம்_வரம்புகள்[0]}-{ஆழம்_வரம்புகள்[1]}cm"
        மதிப்பு_குறிப்பு = மதிப்பு

        return f"{மாறி_குறிப்பு}_{ஆழ_குறிப்பு}_{மதிப்பு_குறிப்பு}"

    def மாறி_குறியீட்டைப்_பெறு(தன், மாறி: str) -> str:
        return மாறி_குறியீடுகள்[மாறி]


மாறி_குறியீடுகள் = {
    "bdod": ப.அடர்த்தி,
    "cec": ப.நேர்மின்_அயனி_பறிமாற்ற_தன்மை,
    "cfvo": ப.பாறைத்_துண்டங்கள்,
    "clay": ப.களிமண்,
    "nitrogen": ப.தலைச்சத்து,
    "ocd": ப.கரிம_சேர்ம_அடர்த்தி,
    "ocs": ப.கரிம_சேர்ம_இருப்பு,
    "soc": ப.மண்_கரிம_சேர்மம்,
    "phh2o": ப.அமில_காரத்தன்மை,
    "sand": ப.மணல்,
    "silt": ப.கரம்பை,
    "wv0010": ப.கன_நீர்_இருப்பு_பத்து,
    "wv1500": ப.கன_நீர்_இருப்பு_ஆயிரத்தியைநூறு,
    "wv003": ப.கன_நீர்_இருப்பு_மூப்பத்துமூன்று,
}


class ஓஸிஸ்_மண்_வகைகள்(மண்):
    """
    WOSIS
    """

    def தரவுகளைப்_பெறு(தன், மறை=None):
        சேவை = இணைபசே(
            வரைப்படம்="wrb",
            அடையாளம்="MostProbable",
        )
        return சேவை.தரவுகளைப்_பெறு(மறை)

    def ஒற்றுமை(தன், நிலநேர்க்கோடு, நிலநிரைக்கொடு, மறை=None) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு(மறை)
        மண்_வகை = தரவுகள்.sel(
            **{அகலாங்கு_அச்சு: நிலநேர்க்கோடு, நெட்டாங்கு_அச்சு: நிலநிரைக்கொடு},
            method="nearest",
        )

        return xr.where(தரவுகள் == மண்_வகை, 1, 0)
