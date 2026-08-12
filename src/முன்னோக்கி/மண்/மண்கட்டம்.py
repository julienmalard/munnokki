from owslib.wcs import WebCoverageService
import xarray as xr
from .மண் import மண்
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு


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

    def __init__(தன், மாறிகள்):
        தன்.மாறிகள் = மாறிகள்

        cov_id = 'phh2o_0-5cm_mean'
        subsets = [('X', -1784000, -1140000), ('Y', 1356000, 1863000)]


    def தரவுகளைப்_பெறு(தன்):

        for மாறி in தன்.மாறிகள்:
            மாறி_குறியீடு = தன்.மாறி_குறியீட்டைப்_பெறு(மாறி)
            அடையாளம் = தன்.தரவு_அடையாளத்தைப்_பெறு(மாறி=மாறி)
            சேவை = WebCoverageService(f'http://maps.isric.org/mapserv?map=/map/{மாறி_குறியீடு}.map', version='2.0.1')
            பதில் = சேவை.getCoverage(
                identifier=[அடையாளம்],
                crs="http://www.opengis.net/def/crs/EPSG/0/152160",
                subsets=subsets,
                resx=250, resy=250,
                format=சேவை.supportedFormats[0]
            )
            with open('./data/Senegal_pH_0-5_mean.tif', 'wb') as கோப்பு:
                கோப்பு.write(பதில்.read())

        xr.open_dataarray('./data/Senegal_pH_0-5_mean.tif').rio.write_crs("ESRI:54052").rio.reproject("EPSG:4326").rename({
            "x": நெட்டாங்கு_அச்சு,
            "y": அகலாங்கு_அச்சு,
        }).squeeze("band").drop_vars(["band", "spatial_ref"])


    def தரவு_அடையாளத்தைப்_பெறு(தன், மாறி: str, ஆழம்: int, மதிப்பு):
        மாறி_குறிப்பு = தன்.மாறி_குறியீட்டைப்_பெறு(மாறி)

        return f'{மாறி_குறிப்பு}_{ஆழ_குறிப்பு}_{மதிப்பு_குறிப்பு}'

    def மாறி_குறியீட்டைப்_பெறு(தன், மாறி: str) -> str:
        return மாறி_குறியீடுகள்[மாறி]

மாறி_குறியீடுகள் = {
"bdod": "",
"cec": "",
"cfvo": "",
"clay": "",
"nitrogen": "",
"ocd": "",
"ocs": "",
"soc": "",
"phh2o": "",
"sand": "",
"silt": "",
"wv0010": "",
"wv1500": "",
"wv003": "",
}