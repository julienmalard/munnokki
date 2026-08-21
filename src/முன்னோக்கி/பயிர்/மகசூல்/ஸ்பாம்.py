from typing import Optional

import xarray as xr
from pybtex.database import Entry

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ...கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


class ஸ்பாம்(மகசூல்):
    """
    https://www.mapspam.info/data/
    https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SWPENT
    """

    பெயர்_சமானம் = {
        "whea": பெயர்கள்.கோதுமை,
        "rice": பெயர்கள்.நெல்,
        "maiz": பெயர்கள்.மக்காச்சோளம்,
        "barl": பெயர்கள்.வாற்கோதுமை,
        "mill": "Small Millet",
        "pmil": "Pearl Millet",
        "sorg": பெயர்கள்.சோளம்,
        # "ocer": "Other Cereals",
        "pota": பெயர்கள்.உருளைக்கிழங்கு,
        "swpo": பெயர்கள்.வற்றாளைக்கிழங்கு,
        "yams": பெயர்கள்.சேனைக்கிழங்கு,
        "cass": பெயர்கள்.மரவள்ளி,
        # "orts": "Other Roots",
        "bean": பெயர்கள்.அவரையினம்,
        "chic": பெயர்கள்.கொண்டைக்_கடலை,
        "cowp": பெயர்கள்.காராமணி,
        "pige": பெயர்கள்.துவரை,
        "lent": பெயர்கள்.மைசூர்ப்_பருப்பு,
        # "opul": "Other Pulses",
        "soyb": பெயர்கள்.சோயா,
        "grou": பெயர்கள்.வேர்கடலை,
        "cnut": பெயர்கள்.தென்னை,
        "oilp": பெயர்கள்.செம்பனை,
        "sunf": பெயர்கள்.சூரியகாந்தி,
        "rape": பெயர்கள்.கனோலா,
        "sesa": பெயர்கள்.எள்,
        # "ooil": "Other Oil Crops",
        "sugc": பெயர்கள்.கரும்பு,
        "sugb": பெயர்கள்.சக்கரைச்_செங்கிழங்கு,
        "cott": பெயர்கள்.பருத்தி,
        # "ofib": "Other Fibre Crops",
        "coff": "Arabic Coffee",
        "rcof": "Robust Coffee",
        "coco": பெயர்கள்.கொக்கோ,
        "teas": பெயர்கள்.தேயிலை,
        "toba": பெயர்கள்.புகையிலை,
        "bana": பெயர்கள்.வாழை,
        "plnt": பெயர்கள்.வாழைக்காய்,
        "citr": "Citrus",
        # "trof": "Other Tropical Fruit",
        # "temf": "Temperate Fruit",
        "toma": பெயர்கள்.தக்காளி,
        "onio": பெயர்கள்.வெங்காயம்,
        # "vege": "Other Vegetables",
        "rubb": பெயர்கள்.மீள்மம்,
        # "rest": "Rest Of Crops",
    }

    def __init__(தன், தரவு_கோப்புரை: Optional[str] = None):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)
        தன்.இணைய_முகவரி = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SWPENT"

    def தரவுகளைப்_பெறு(தன், பயிர்கள்=None) -> xr.DataArray:
        பயிர்கள் = பயிர்கள் or தன்.பெயர்_சமானம்.values()

        தரவுகள் = []
        for பயிர் in பயிர்கள்:
            பயிர்_தரவுகள் = ஜிப்_பதிவிறக்கம்(
                உள்_கோப்பு_பாதை=தன்.உள்_கோப்பு_பெயரைப்_பெறு(பயிர்=பயிர்),
                பெயர்="SPAM2020",
                பதிவிறக்க_முகவரி="https://uc7d84332914b1a50e4464c7cb27.dl.dropboxusercontent.com/cd/0/get/DF97igdacshN0pMo4sHRy0mNZIS1otumbYJfqQA9QZ0syefbN4u0ty8QO4gIGI8YJ6GbDD3h3Fd-WyG-tMBsaK3_lGKXOkXBIB_MMAzLIPdCvMRtghVNaCVeAnxgu2MskKEhaBVtQ5fB4Jt3d7oxi8XsGNlqYKeNe9dr1CJ9bA0WHA/file?_download_id=61288417551464298075394442349195462245351782123568741928849543311&_log_download_success=1&_notify_domain=www.dropbox.com&dl=1",
                தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
            ).தரவு_அணியைப்_பெறு()

            தரவுகள்.append(பயிர்_தரவுகள்)

        return xr.combine_by_coords(தரவுகள்)

    def உள்_கோப்பு_பெயரைப்_பெறு(தன், பயிர்: str, நீர்பாசனம்: bool) -> str:
        நீர்பாசன_குறியீடு = "I" if நீர்பாசனம் else "R"  # I, R, A
        return f"spam2020_V2r2_global_Y_{தன்.ஸ்பாம்_பயிர்_பெயர்(பயிர்).upper()}_{நீர்பாசன_குறியீடு}.tif"

    def ஸ்பாம்_பயிர்_பெயர்(தன், பெயர்: str) -> str:
        return தன்.பெயர்_சமானம்[பெயர்]

    def மேற்கோள்(தன்) -> list[Entry]:
        return """International Food Policy Research Institute (IFPRI), 2026, "Global Spatially-Disaggregated Crop Production Statistics Data for 2020 Version 2.0 Release 2", https://doi.org/10.7910/DVN/SWPENT, Harvard Dataverse, V5"""

    def உரிமம்(தன்) -> Optional[உரிமம்]:
        return "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SWPENT&version=6.0&selectTab=termsTab"
