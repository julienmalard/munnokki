import xarray as xr

from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ...கருவிகள்.பதிவிறக்கம் import பதிவிறக்கம், ஜிப்_பதிவிறக்கம்


class ஸ்பாம்(மகசூல்):
    """
    https://www.mapspam.info/data/
    https://www.dropbox.com/scl/fi/hj1wbznjv3k4dfgr6to08/spam2020V2r2_global_yield.geotiff.zip?rlkey=p9u91gc61uwp3r7m5bkixh59y&st=7rkeovp9&dl=0
    """

    def தரவுகளைப்_பெறு(தன், பயிர்: str) -> xr.DataArray:
        return ஜிப்_பதிவிறக்கம்(
            பெயர்=தன்.உள்_கோப்பு_பெயரைப்_பெறு(பயிர்),
            பதிவிறக்க_முகவரி="https://uc7d84332914b1a50e4464c7cb27.dl.dropboxusercontent.com/cd/0/get/DF97igdacshN0pMo4sHRy0mNZIS1otumbYJfqQA9QZ0syefbN4u0ty8QO4gIGI8YJ6GbDD3h3Fd-WyG-tMBsaK3_lGKXOkXBIB_MMAzLIPdCvMRtghVNaCVeAnxgu2MskKEhaBVtQ5fB4Jt3d7oxi8XsGNlqYKeNe9dr1CJ9bA0WHA/file?_download_id=61288417551464298075394442349195462245351782123568741928849543311&_log_download_success=1&_notify_domain=www.dropbox.com&dl=1",
        ).பெறு()

    @staticmethod
    def உள்_கோப்பு_பெயரைப்_பெறு(பயிர்: str, நீர்பாசனம்: bool) -> str:
        நீர்பாசன_குறியீடு = "I" if நீர்பாசனம் else "R"  # I, R, A
        return (
            f"spam2020_V2r2_global_Y_{ஸ்பாம்_பயிர்_பெயர்(பயிர்).upper()}_{நீர்பாசன_குறியீடு}.tif"
        )


def ஸ்பாம்_பயிர்_பெயர்(பெயர்: str) -> str:
    return பெயர்_சமானம்[பெயர்]


பெயர்_சமானம் = {
    "whea": பெயர்கள்.கோதுமை,
    "rice": பெயர்கள்.நெல்,
    "maiz": பெயர்கள்.மக்காச்சோளம்,
    "barl": "Barley",
    "mill": "Small Millet",
    "pmil": "Pearl Millet",
    "sorg": "Sorghum",
    "ocer": "Other Cereals",
    "pota": "Potato",
    "swpo": "Sweet Potato",
    "yams": "Yams",
    "cass": "Cassava",
    "orts": "Other Roots",
    "bean": "Bean",
    "chic": "Chickpea",
    "cowp": "Cowpea",
    "pige": "Pigeon Pea",
    "lent": "Lentil",
    "opul": "Other Pulses",
    "soyb": "Soybean",
    "grou": "Groundnut",
    "cnut": "Coconut",
    "oilp": "Oilpalm",
    "sunf": "Sunflower",
    "rape": "Rapeseed",
    "sesa": "Sesame Seed",
    "ooil": "Other Oil Crops",
    "sugc": "Sugarcane",
    "sugb": "Sugarbeet",
    "cott": "Cotton",
    "ofib": "Other Fibre Crops",
    "coff": "Arabic Coffee",
    "rcof": "Robust Coffee",
    "coco": "Cocoa",
    "teas": "Tea",
    "toba": "Tobacco",
    "bana": "Banana",
    "plnt": "Plantain",
    "citr": "Citrus",
    "trof": "Other Tropical Fruit",
    "temf": "Temperate Fruit",
    "toma": "Tomato",
    "onio": "Onion",
    "vege": "Other Vegetables",
    "rubb": "Rubber",
    "rest": "Rest Of Crops",
}
