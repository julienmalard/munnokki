from typing import Optional

import pybtex.database
import xarray as xr
from pybtex.database import Entry

from .பயிர்_பரப்பளவு import பயிர்_பரப்பளவு
from .. import பயிர்_பெயர்கள் as பெயர்கள்
from ..மாறிலிகள் import பயிர்_அச்சு
from ...அச்சுகள் import நெட்டாங்கு_அச்சு, அகலாங்கு_அச்சு
from ...கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


class பயிர்கட்டம்(பயிர்_பரப்பளவு):
    def __init__(
        தன்,
        தரவு_திறன்=0,
        பயிர்கள்: Optional[str | list[str]] = None,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)

        தன்.தரவு_திறன் = தரவு_திறன்
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[str | list[str]] = None) -> xr.DataArray:
        பயிர்கள் = (
            [பயிர்கள்] if isinstance(பயிர்கள், str) else பயிர்கள் or list(பெயர்_சமானம்.values())
        )

        தரவு_பட்டியல் = []
        for பயிர் in பயிர்கள்:
            பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
                உள்_கோப்பு_பாதை=தன்.உள்_கோப்பு_பெயர்(பயிர்),
                பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
                தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
            )
            தரவுகள் = பதிவிறக்கம்.தரவுத்தளத்தைப்_பெறு().rename(
                {"lat": அகலாங்கு_அச்சு, "lon": நெட்டாங்கு_அச்சு}
            )
            தரவுகள் = தன்.வடிக்க(தரவுகள்)

            தரவு_பட்டியல்.append(தரவுகள்["croparea"])

        return xr.concat(தரவு_பட்டியல், dim=பயிர்_அச்சு)

    @staticmethod
    def உள்_கோப்பு_பெயர்(பயிர்_பெயர்: str):
        return f"CROPGRIDSv1.08_{பயிர்க்கட்டம்_பெயர்(பயிர்_பெயர்)}.nc"

    def வடிக்க(தன், தரவுகள்: xr.Dataset) -> xr.Dataset:
        தரவுகள்["croparea"] = xr.where(
            தரவுகள்["quality"] >= தன்.தரவு_திறன், தரவுகள்["croparea"], 0
        )
        தரவுகள்["harvarea"] = xr.where(
            தரவுகள்["quality"] >= தன்.தரவு_திறன், தரவுகள்["harvarea"], 0
        )
        return தரவுகள்

    def மேற்கோள்(தன்) -> list[Entry]:
        return [
            pybtex.database.parse_string("TY  - JOUR\nAU  - Tang, Fiona H. M.\nAU  - Nguyen, Thu Ha\nAU  - Conchedda, Giulia\nAU  - Casse, Leon\nAU  - Tubiello, Francesco N.\nAU  - Maggi, Federico\nPY  - 2024\nDA  - 2024/04/22\nTI  - CROPGRIDS: a global geo-referenced dataset of 173 crops\nJO  - Scientific Data\nSP  - 413\nVL  - 11\nIS  - 1\nAB  - CROPGRIDS is a comprehensive global geo-referenced dataset providing area information for 173 crops for the year 2020, at a resolution of 0.05° (about 5.6 km at the equator). It represents a major update of the Monfreda et al. (2008) dataset (hereafter MRF), the most widely used geospatial dataset previously available, covering 175 crops with reference year 2000 at 10 km spatial resolution. CROPGRIDS builds on information originally provided in MRF and expands it using 27 selected published gridded datasets, subnational data of 52 countries obtained from National Statistical Offices, and the 2020 national-level statistics from FAOSTAT, providing more recent harvested and crop (physical) areas for 173 crops at regional, national, and global levels. The CROPGRIDS data advance the current state of knowledge on the spatial distribution of crops, providing useful inputs for modelling studies and sustainability analyses relevant to national and international processes.\nSN  - 2052-4463\nUR  - https://doi.org/10.1038/s41597-024-03247-7\nDO  - 10.1038/s41597-024-03247-7\nID  - Tang2024\nER  - ", bib_format="ris"),

        ]


பெயர்_சமானம் = {
    "abaca": பெயர்கள்.அபாக்கா,
    "agave": பெயர்கள்.அகவே,
    "alfalfa": பெயர்கள்.குதிரை_மசால்,
    "almond": பெயர்கள்.பாதாம்,
    "aniseetc": பெயர்கள்.சோம்பு,
    "apricot": பெயர்கள்.சர்க்கரை_பாதாமி,
    "areca": பெயர்கள்.பாக்கு,
    "artichoke": பெயர்கள்.முள்_முட்டைக்கோசு,
    "asparagus": பெயர்கள்.சாத்தாவாரியினம்,
    "avocado": பெயர்கள்.வெண்ணெய்_பழம்,
    "bambara": பெயர்கள்.பம்பரா_பருப்பு,
    "banana": பெயர்கள்.வாழை,
    "barley": பெயர்கள்.வாற்கோதுமை,
    "bean": பெயர்கள்.அவரையினம்,
    "beetfor": பெயர்கள்.தீவன_செங்கிழங்கு,
    # "berrynes": பெயர்கள்.வேறு_சின்ன_பழங்கள்,
    "blueberry": பெயர்கள்.அவுரிநெல்லி,
    "brazil": பெயர்கள்.பிரேசில்_கோட்டை,
    "broadbean": பெயர்கள்.தட்டை_மோச்சை,
    "buckwheat": பெயர்கள்.நெளிகோதுமை,
    "cabbage": பெயர்கள்.முட்டைக்கோசு,
    "cabbagefor": பெயர்கள்.தீவன_முட்டைக்கோசு,
    "canaryseed": பெயர்கள்.ஃபலாரிஸ்_கனாரியென்ஸிஸ்,
    "carob": பெயர்கள்.கரோபு,
    "carrot": பெயர்கள்.குறுங்கிழங்கு,
    "carrotfor": பெயர்கள்.தீவன_குறுங்கிழங்கு,
    "cashew": பெயர்கள்.முந்திரி,
    "cashewapple": பெயர்கள்.போலிப்பழம்,
    "cassava": பெயர்கள்.மரவள்ளி,
    "castor": பெயர்கள்.ஆமணக்கு,
    "cauliflower": பெயர்கள்.பூக்கோசு,
    # "cerealnes": பெயர்கள்.வேறு_தானியங்கள்,
    "cherry": பெயர்கள்.சேலாப்பழம்,
    "chestnut": பெயர்கள்.கசுக்கோட்டை,
    "chickpea": பெயர்கள்.கொண்டைக்_கடலை,
    "chicory": பெயர்கள்.காசினிக்கீரை,
    "chilleetc": பெயர்கள்.பச்சை_மிளகாய்,
    "cinnamon": பெயர்கள்.இலவங்கப்பட்டை,
    "citrusnes": பெயர்கள்.கிச்சிலி,
    "clove": பெயர்கள்.கிராம்பு,
    "clover": பெயர்கள்.சீமைமசால்,
    "cocoa": பெயர்கள்.கொக்கோ,
    "coconut": பெயர்கள்.தெங்காய்,
    "coffee": பெயர்கள்.குளம்பி,
    "coir": பெயர்கள்.தென்னை_நார்,
    "cotton": பெயர்கள்.பருத்தி,
    "cowpea": பெயர்கள்.காராமணி,
    "cranberry": பெயர்கள்.குருதிநெல்லி,
    "cucumberetc": பெயர்கள்.வெள்ளரிக்காய்,
    "currant": பெயர்கள்.சிவப்பு_நெல்லிக்காய்,
    "date": பெயர்கள்.பேரிச்சம்பழம்,
    "eggplant": பெயர்கள்.கத்தரிக்காய்,
    # "fibrenes": பெயர்கள்.வேறு_நார்பொருட்கள்,
    "fig": பெயர்கள்.அத்திப்பழம்,
    "flax": பெயர்கள்.ஆளிச்செடி_நார்,
    "fonio": பெயர்கள்.ஃபோனியோ,
    # "fornes": பெயர்கள்.வேறு_தீவனங்கள்,
    # "fruitnes": பெயர்கள்.வேறு_பழங்கள்,
    "garlic": பெயர்கள்.பூண்டு,
    "ginger": பெயர்கள்.இஞ்சி,
    "gooseberry": பெயர்கள்.நெல்லிக்காய்,
    "grape": பெயர்கள்.திராட்சை,
    "grapefruitetc": பெயர்கள்.பப்ளிமாஸ்,
    # "grassnes": பெயர்கள்.வேறு_புல்கள்,
    "greenbean": பெயர்கள்.பச்சை_அவரை,
    "greenbroadbean": பெயர்கள்.பச்சை_தட்டை_மோச்சை,
    "greencorn": பெயர்கள்.பச்சை_மக்காச்சோளம்,
    "greenonion": பெயர்கள்.வெங்காயத்தாள்,
    "greenpea": பெயர்கள்.பச்சை_பட்டாணி,
    "groundnut": பெயர்கள்.வேர்கடலை,
    "gums": பெயர்கள்.பிசின்,
    "hazelnut": பெயர்கள்.நோவாஸெத்_கொட்டை,
    "hemp": பெயர்கள்.சணல்நார்,
    "hempseed": பெயர்கள்.சணல்_விதை,
    "hop": பெயர்கள்.ஹுமுலுஸ்_லூபுலுஸ்,
    "jute": பெயர்கள்.கோர்கோரஸ்,
    # "jutelikefiber": பெயர்கள்.சணல்_போன்ற_நார்,
    "kapokfiber": பெயர்கள்.கபுக்நார்,
    "kapokseed": பெயர்கள்.கபுக்விதை,
    "karite": பெயர்கள்.வித்தெலாரியா,
    "kiwi": பெயர்கள்.பசலிப்பழம்,
    "kolanut": பெயர்கள்.கோலா_கோட்டை,
    # "legumenes": பெயர்கள்.வேறு_பச்சை_இருபுற_வெடிக்கனி,
    "lemonlime": பெயர்கள்.எலுமிச்சை,
    "lentil": பெயர்கள்.மைசூர்ப்_பருப்பு,
    "lettuce": பெயர்கள்.இலைக்கோசு,
    "linseed": பெயர்கள்.ஆளிச்செடி_விதை,
    "lupin": பெயர்கள்.லூபின்,
    "maize": பெயர்கள்.மக்காச்சோளம்,
    "maizefor": பெயர்கள்.தீவன_மக்காச்சோளம்,
    "mango": பெயர்கள்.மாம்பழம்,
    "mate": பெயர்கள்.மாத்தே,
    "melonetc": பெயர்கள்.மூலாம்பழம்,
    "melonseed": பெயர்கள்.மூலாம்பழம்_விதை,
    "millet": பெயர்கள்.சிறுதானியம்,
    # "mixedgrain": பெயர்கள்.கலந்த_தானியங்கள்,
    # "mixedgrass": பெயர்கள்.கலந்த_புல்கள்,
    "mushroom": பெயர்கள்.காலான்,
    "mustard": பெயர்கள்.கடுகு,
    # "nutmeg": பெயர்கள்.சாதிக்காய்,
    # "nutnes": பெயர்கள்.வேறு_கோட்டை,
    "oats": பெயர்கள்.காடைக்கண்ணி,
    "oilpalm": பெயர்கள்.செம்பனை,
    "oilseedfor": பெயர்கள்.தீவன_எண்ணெய்_விதைகள்,
    "oilseednes": பெயர்கள்.எண்ணெய்_விதைகள்,
    "okra": பெயர்கள்.வெண்டக்காய்,
    "olive": பெயர்கள்.ஐரோப்பிய_இடலை,
    "onion": பெயர்கள்.வெங்காயம்,
    "orange": பெயர்கள்.தோடம்பழம்,
    "papaya": பெயர்கள்.பப்பாளி,
    "pea": பெயர்கள்.பட்டாணி,
    "peachetc": பெயர்கள்.குழிப்பேரி,
    "pear": பெயர்கள்.பேரி,
    "pepper": பெயர்கள்.மிளகு,
    "peppermint": பெயர்கள்.மிளகுக்கீரை,
    "persimmon": பெயர்கள்.சீமைப்பனிச்சை,
    "pigeonpea": பெயர்கள்.துவரை,
    "pimento": பெயர்கள்.மிளகாய்,
    "pineapple": பெயர்கள்.அன்னாசி,
    "pistachio": பெயர்கள்.பசுங்கொட்டை,
    "plantain": பெயர்கள்.வாழைக்காய்,
    "plum": பெயர்கள்.கொத்துப்பேரி,
    "popcorn": பெயர்கள்.சொளப்பொரி,
    "poppy": பெயர்கள்.கசகசா,
    "potato": பெயர்கள்.உருளைக்கிழங்கு,
    # "pulsenes": பெயர்கள்.வேறு_இருபுற_வெடிக்கனி,
    "pumpkinetc": பெயர்கள்.பூசணி,
    "pyrethrum": பெயர்கள்.செந்தூரகம்,
    "quince": பெயர்கள்.சீமைமாதுளை,
    "quinoa": பெயர்கள்.கினோவா,
    "ramie": பெயர்கள்.ரமி,
    "rapeseed": பெயர்கள்.கனோலா,
    "rasberry": பெயர்கள்.புற்றுப்பழம்,
    "rice": பெயர்கள்.நெல்,
    # "rootnes": பெயர்கள்.வேறு_வேர்கள்,
    "rubber": பெயர்கள்.மீள்மம்,
    "rye": பெயர்கள்.புல்லரிசி,
    "ryefor": பெயர்கள்.தீவனப்_புல்லரிசி,
    "safflower": பெயர்கள்.குசம்பப்பூ,
    "sesame": பெயர்கள்.எள்,
    "sisal": பெயர்கள்.கதலை,
    "sorghum": பெயர்கள்.சோளம்,
    "sorghumfor": பெயர்கள்.தீவனச்_சோளம்,
    "sourcherry": பெயர்கள்.புலிக்கும்_சேலாப்பழம்,
    "soybean": பெயர்கள்.சோயா,
    # "spicenes": பெயர்கள்.வேறு_மசாலா_பொருட்கள்,
    "spinach": பெயர்கள்.பசளி,
    "stonefruitnes": பெயர்கள்.வேறு_உள்_ஒட்டு_சதைக்கனி,
    "strawberry": பெயர்கள்.செம்புற்று,
    "stringbean": பெயர்கள்.அவரைக்காய்,
    "sugarbeet": பெயர்கள்.சக்கரைச்_செங்கிழங்கு,
    "sugarcane": பெயர்கள்.கம்பு,
    # "sugarnes": பெயர்கள்.வேறு_சக்கரை,
    "sunflower": பெயர்கள்.சூரியகாந்தி,
    "swedefor": பெயர்கள்.தீவன_வெண்_நூல்கோல்,
    "sweetpotato": பெயர்கள்.வற்றாளைக்கிழங்கு,
    "tangetc": பெயர்கள்.மெண்டரின்_தோடம்பழம்,
    "taro": பெயர்கள்.சேம்பு,
    "tea": பெயர்கள்.தேயிலை,
    "tobacco": பெயர்கள்.புகையிலை,
    "tomato": பெயர்கள்.தக்காளி,
    "triticale": பெயர்கள்.திரிதிகால்,
    # "tropicalnes": பெயர்கள்.வேறு_வெமண்டல_பழங்கள்,
    "tung": பெயர்கள்.தூங்_மரம்,
    "turnipfor": பெயர்கள்.தீவன_கோசுக்கிழங்கு,
    "vanilla": பெயர்கள்.வெனிலா,
    # "vegetablenes": பெயர்கள்.வேறு_காய்கறிகள்,
    "vegfor": பெயர்கள்.தீவன_காய்கறிகள்,
    "vetch": பெயர்கள்.விசியா,
    "walnut": பெயர்கள்.வாதுமைக்_கோட்டை,
    "watermelon": பெயர்கள்.தர்ப்பூசணி,
    "wheat": பெயர்கள்.கோதுமை,
    "yam": பெயர்கள்.சேனைக்கிழங்கு,
    "yautia": பெயர்கள்.யௌத்தீயா,
}


def பயிர்க்கட்டம்_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
