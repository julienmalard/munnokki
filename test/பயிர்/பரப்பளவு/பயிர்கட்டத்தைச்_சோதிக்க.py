import io
import math
import os
import zipfile
from tempfile import TemporaryDirectory

import numpy as np
import pytest
import xarray as xr
import xarray.testing as xrt
from pytest_urllib3 import Urllib3Mock

from முன்னோக்கி.அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from முன்னோக்கி.பயிர்.பயிர்_பெயர்கள் import வாழை, சிறுதானியம், பாதாம், குதிரை_மசால், அகவே, அபாக்கா
from முன்னோக்கி.பயிர்.பரப்பளவு.பயிர்கட்டம் import பயிர்கட்டம்
from முன்னோக்கி.பயிர்.மாறிலிகள் import பயிர்_அச்சு

படி = 10
அகலாங்கு = np.arange(-90, 90 + படி, படி)
நெட்டாங்கு = np.arange(-180, 180 + படி, படி)


@pytest.fixture
def சுமா_பயிர்க்ட்டம்(urllib3_mock: Urllib3Mock):
    # எல்லா பயிர்கள் வேண்டாம், இதுவே போதும்...
    பெயர்_சமானம் = பயிர்கட்டம்.பெயர்_சமானம்
    பயிர்கட்டம்.பெயர்_சமானம் = {
        "abaca": அபாக்கா,
        "agave": அகவே,
        "alfalfa": குதிரை_மசால்,
        "almond": பாதாம்,
        "வாழை": வாழை,
        "சிறுதானியம்": சிறுதானியம்,
    }
    நினைவகத்தில்_ஜிப் = io.BytesIO()

    ஆயக்கூறுகள் = {
        "lat": அகலாங்கு,
        "lon": நெட்டாங்கு,
    }
    வடிவம் = [ஆய.size for ஆய in ஆயக்கூறுகள்.values()]
    திறன் = np.random.random(math.prod(வடிவம்)).reshape(வடிவம்)

    with zipfile.ZipFile(நினைவகத்தில்_ஜிப், "w") as ஜிப்கோப்பு:
        for பயிர் in பயிர்கட்டம்.பெயர்_சமானம்:
            கோப்பு_பெயர் = os.path.join(
                "CROPGRIDSv1.08_NC_maps", f"CROPGRIDSv1.08_{பயிர்}.nc"
            )

            def மாறி_தரவுகள்(மாறி: str):
                if மாறி == "qual":
                    return திறன்
                elif மாறி == "set":
                    return np.random.randint(1, 6, size=math.prod(வடிவம்)).reshape(வடிவம்)
                else:
                    return (
                        (np.random.random(math.prod(வடிவம்)) * 1000)
                        .round()
                        .reshape(வடிவம்)
                    )

            தரவுகள் = xr.Dataset(
                {
                    மாறி: xr.DataArray(
                        மாறி_தரவுகள்(மாறி),
                        coords=ஆயக்கூறுகள்,
                        dims=ஆயக்கூறுகள்.keys(),
                        name=மாறி,
                    )
                    for மாறி in ["harvarea", "croparea", "qual", "set"]
                },
                coords=ஆயக்கூறுகள்,
                attrs={
                    "Creation date": "10-Mar-2024 09:19:38",
                    "Authors": "F. Maggi, F.H.M. Tang, T.H. Nguyen",
                    "Version": "v1.08",
                },
            )
            ஜிப்கோப்பு.writestr(கோப்பு_பெயர், தரவுகள்.to_netcdf())

    urllib3_mock.add_response(
        url="https://api.figshare.com/v2/file/download/44950942",
        content=நினைவகத்தில்_ஜிப்.getvalue(),
    )
    yield {"திறன்": திறன்}

    பயிர்கட்டம்.பெயர்_சமானம் = பெயர்_சமானம்


def தரவுகளைப்_பெறு_சோதிக்க(சுமா_பயிர்க்ட்டம்):
    with TemporaryDirectory() as தற்காலிகமானது:
        தரவுகள் = பயிர்கட்டம்(தரவு_கோப்புரை=தற்காலிகமானது).தரவுகளைப்_பெறு()

    xrt.assert_equal(
        தரவுகள்.coords,
        xr.DataArray(
            coords={
                அகலாங்கு_அச்சு: அகலாங்கு,
                நெட்டாங்கு_அச்சு: நெட்டாங்கு,
                பயிர்_அச்சு: sorted([*பயிர்கட்டம்.பெயர்_சமானம்.values()]),
            },
            dims=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு, பயிர்_அச்சு],
        ).coords,
    )


def குறிப்பிட்ட_பயிர்களுடன்_தரவுகளைப்_பெறு_சோதிக்க(சுமா_பயிர்க்ட்டம்):
    with TemporaryDirectory() as தற்காலிகமானது:
        தரவுகள் = பயிர்கட்டம்(தரவு_கோப்புரை=தற்காலிகமானது).தரவுகளைப்_பெறு(
            பயிர்கள்=[வாழை, சிறுதானியம்]
        )

    xrt.assert_equal(
        தரவுகள்.coords,
        xr.DataArray(
            coords={
                அகலாங்கு_அச்சு: அகலாங்கு,
                நெட்டாங்கு_அச்சு: நெட்டாங்கு,
                பயிர்_அச்சு: sorted([வாழை, சிறுதானியம்]),
            },
            dims=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு, பயிர்_அச்சு],
        ).coords,
    )


def தரவு_திறன்_வடிக்கட்டியுடன்_தரவுகளைப்_பெறு_சோதிக்க(சுமா_பயிர்க்ட்டம்):
    with TemporaryDirectory() as தற்காலிகமானது:
        தரவுகள் = பயிர்கட்டம்(தரவு_கோப்புரை=தற்காலிகமானது, தரவு_திறன்=0.5).தரவுகளைப்_பெறு(
            பயிர்கள்=[வாழை, சிறுதானியம்]
        )
    assert (
        xr.where(சுமா_பயிர்க்ட்டம்["திறன்"] < 0.5, தரவுகள், np.nan)
        .isnull()
        .all()
        .compute()
        .values
        == True
    )
    assert (
        xr.where(சுமா_பயிர்க்ட்டம்["திறன்"] >= 0.5, தரவுகள், 1)
        .notnull()
        .all()
        .compute()
        .values
        == True
    )


def மேற்கோள்களைச்_சோதிக்க():
    மேற்கோள்கள் = பயிர்கட்டம்().மேற்கோள்()
    assert len(மேற்கோள்கள்) > 0
