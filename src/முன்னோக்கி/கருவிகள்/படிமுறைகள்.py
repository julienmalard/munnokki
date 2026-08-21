import numpy as np
import xarray as xr
from scipy.spatial import distance

from ..அச்சுகள் import நெட்டாங்கு_அச்சு, அகலாங்கு_அச்சு


def அச்சு_தயாரிப்பு(மதிப்பு: xr.DataArray, குறிப்பு: xr.DataArray, அச்சு: str | list[str]):
    if not isinstance(அச்சு, str):
        மாறி_அச்சு_மாற்றம் = {"மாறி": அச்சு}
        மதிப்பு = மதிப்பு.stack(மாறி_அச்சு_மாற்றம்)
        குறிப்பு = குறிப்பு.stack(மாறி_அச்சு_மாற்றம்)
        அச்சு = "மாறி"
    return மதிப்பு, குறிப்பு, அச்சு

def நெறிமப்படுத்துக்கொ(குறிப்பு, *மற்றது):
    கூட்டுச்சராசரி = குறிப்பு.mean()
    நியமவிலகல் = குறிப்பு.std()
    return (குறிப்பு-கூட்டுச்சராசரி)/நியமவிலகல், *[(ம-கூட்டுச்சராசரி)/நியமவிலகல் for ம in மற்றது]

def யூக்ளிடிய(
    மதிப்பு: xr.DataArray, குறிப்பு: xr.DataArray, மாறி_அச்சு: str | list[str]
) -> xr.DataArray:
    மதிப்பு, குறிப்பு, மாறி_அச்சு = அச்சு_தயாரிப்பு(மதிப்பு, குறிப்பு, மாறி_அச்சு)
    return (மதிப்பு - குறிப்பு.squeeze()).reduce(np.linalg.norm, dim=மாறி_அச்சு)


def மஹனலோபிஸ்(
    மதிப்பு: xr.DataArray, குறிப்பு: xr.DataArray, மாறி_அச்சு: str | list[str]
) -> xr.DataArray:
    மதிப்பு, குறிப்பு, மாறி_அச்சு = அச்சு_தயாரிப்பு(மதிப்பு, குறிப்பு, மாறி_அச்சு)
    # மதிப்பு, குறிப்பு = நெறிமப்படுத்துக்கொ(மதிப்பு, குறிப்பு)

    எதிர்_கூடபரவற்படி = np.linalg.inv(
        xr.apply_ufunc(
            np.cov,
            மதிப்பு.stack({"இடம்": [அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு]}).transpose(
                *[மாறி_அச்சு, "இடம்"]
            ),
            input_core_dims=[["இடம்"]],
            output_core_dims=[["இரண்டாவது மாறி அச்சு"]],
        )
    )

    def செயல்பாட்டு(ஆ, இ):
        return distance.mahalanobis(ஆ, இ, எதிர்_கூடபரவற்படி)

    தொலைவு = xr.apply_ufunc(
        செயல்பாட்டு,
        குறிப்பு.squeeze([அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு]),
        மதிப்பு,
        input_core_dims=[[மாறி_அச்சு], [மாறி_அச்சு]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=["float"],
    )

    return தொலைவு
