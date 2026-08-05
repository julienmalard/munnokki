import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import xarray as xr
from matplotlib.figure import Figure


def வரையு(ஒப்புமை: xr.DataArray, அச்சு=None) -> Figure:
    # https://medium.com/@lubomirfranko/climate-data-visualisation-with-python-visualise-climate-data-using-cartopy-and-xarray-cf35a60ca8eehttps://medium.com/@lubomirfranko/climate-data-visualisation-with-python-visualise-climate-data-using-cartopy-and-xarray-cf35a60ca8ee
    # https://xarray.pydata.org/en/v0.9.6/auto_gallery/plot_cartopy_facetgrid.html
    projection = ccrs.Mercator()
    crs = ccrs.PlateCarree()

    if அச்சு is None:
        படம் = plt.figure(figsize=(16, 9), dpi=150)
        அச்சு = plt.axes(projection=projection, frameon=True)

    அச்சு.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5)
    அச்சு.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3)

    cbar_kwargs = {
        "orientation": "horizontal",
        "shrink": 0.6,
        "pad": 0.05,
        "aspect": 40,
        "label": "விவரங்கள்",
    }
    ஒப்புமை.plot(ax=அச்சு, transform=crs, cbar_kwargs=cbar_kwargs)
    return படம்
