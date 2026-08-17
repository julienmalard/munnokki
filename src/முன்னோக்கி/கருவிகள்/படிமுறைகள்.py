import xarray as xr
import numpy as np
from scipy.spatial import distance
from முன்னோக்கி.காலநிலை.மாறிலிகள் import காலநிலை_மாறி_அச்சு
from முன்னோக்கி.அச்சுகள் import நெட்டாங்கு_அச்சு, அகலாங்கு_அச்சு


def யூக்ளிடிய(மதிப்பு: xr.DataArray, குறிப்பு: xr.DataArray) -> xr.DataArray:
    return (மதிப்பு - குறிப்பு).reduce(np.linalg.norm, காலநிலை_மாறி_அச்சு)


def மஹனலோபிஸ்(மதிப்பு: xr.DataArray, குறிப்பு: xr.DataArray) -> xr.DataArray:
    எதிர்_கூடபரவற்படி = np.linalg.inv(
        np.cov(
            குறிப்பு.stack({"இடம்": [அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு]}).transpose(
                *[காலநிலை_மாறி_அச்சு, "இடம்"]
            ),
        )
    )

    def செயல்பாட்டு(ஆ, இ):
        return distance.mahalanobis(ஆ, இ, எதிர்_கூடபரவற்படி)

    தொலைவு = xr.apply_ufunc(
        செயல்பாட்டு,
        குறிப்பு,
        input_core_dims=[["time"]],
        output_core_dims=[["mid_date"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=["float"],
        dask_gufunc_kwargs={
            "output_sizes": {"mid_date": int(np.ceil(len(dataset.time) / 5))}
        },
    )

    # https://www.nature.com/articles/s41467-019-08540-3#Sec8
    return xr.where(தொலைவு > 2, 0, (2 - தொலைவு) / 2)
