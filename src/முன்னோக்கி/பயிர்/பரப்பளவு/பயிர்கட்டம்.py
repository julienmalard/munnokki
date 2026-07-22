from numbers import Number
from typing import Optional

import xarray as xr

from src.முன்னோக்கி import அச்சுகள்
from src.முன்னோக்கி.கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்
from src.முன்னோக்கி.பயிர்.பரப்பளவு import பயிர்
from .. import பயிர்_பெயர்கள் as பெயர்கள்


class பயிர்கட்டம்(பயிர்):
    def __init__(
        தன்,
        தரவு_திறன்: 0,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
    ):
        super().__init__()

        தன்.தரவு_திறன் = தரவு_திறன்
        தன்.தரவு_கோப்புரை = தரவு_கோப்புரை
        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி

    def ஒற்றுமை(
        தன், நிலநேர்க்கோடு: Number, நிலநிரைக்கொடு: Number, பயிர்_பெயர்: str
    ) -> xr.DataArray:
        பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
            பெயர்=f"{தன்.பதிவிறக்க_முகவரி}/{தன்.உள்_கோப்பு_பெயர்(பயிர்_பெயர்)}",
            பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
        )
        தரவுகள் = xr.open_dataset(பதிவிறக்கம்.பெறு()).rename(
            {"lat": அச்சுகள்.அகலாங்கு, "lon": அச்சுகள்.நெட்டாங்கு}
        )
        தரவுகள் = தன்.வடிக்க(தரவுகள்)
        # https://www.pythontutorials.net/blog/xarray-select-nearest-lat-lon-with-multi-dimension-coordinates/
        புள்ளி = தரவுகள்.sel(
            **{அச்சுகள்.அகலாங்கு: நிலநேர்க்கோடு, அச்சுகள்.நெட்டாங்கு: நிலநிரைக்கொடு},
            method="nearest",
        )
        if புள்ளி["croparea"] < 0:
            return xr.DataArray(
                0, coords=தரவுகள்["croparea"].coords, dims=தரவுகள்["croparea"].dims
            )
        else:
            return xr.where(தரவுகள்["croparea"] > 0, 1, 0)

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


பெயர்_சமானம் = {
    "abaca": பெயர்கள்.அபாக்கா,
    "agave": பெயர்கள்.அகவே,
    "alfalfa": பெயர்கள்.குதிரை_மசால்,
    "almond": பெயர்கள்.பாதாம்,
    "aniseetc": பெயர்கள்.சோம்பு,
    "apricot": பெயர்கள்.சர்க்கரை_பாதாமி,
    "areca": பெயர்கள்.பாக்கு,
    "artichoke": பெயர்கள்,
    "asparagus": பெயர்கள்,
    "avocado": பெயர்கள்,
    "bambara": பெயர்கள்,
    "banana": பெயர்கள்.வாழை,
    "barley": பெயர்கள்,
    "bean": பெயர்கள்,
    "beetfor": பெயர்கள்,
    "berrynes": பெயர்கள்,
    "blueberry": பெயர்கள்,
    "brazil": பெயர்கள்,
    "broadbean": பெயர்கள்,
    "buckwheat": பெயர்கள்,
    "cabbage": பெயர்கள்,
    "cabbagefor": பெயர்கள்,
    "canaryseed": பெயர்கள்,
    "carob": பெயர்கள்,
    "carrot": பெயர்கள்,
    "carrotfor": பெயர்கள்,
    "cashew": பெயர்கள்,
    "cashewapple": பெயர்கள்,
    "cassava": பெயர்கள்,
    "castor": பெயர்கள்,
    "cauliflower": பெயர்கள்,
    "cerealnes": பெயர்கள்,
    "cherry": பெயர்கள்,
    "chestnut": பெயர்கள்,
    "chickpea": பெயர்கள்,
    "chicory": பெயர்கள்,
    "chilleetc": பெயர்கள்,
    "cinnamon": பெயர்கள்,
    "citrusnes": பெயர்கள்,
    "clove": பெயர்கள்,
    "clover": பெயர்கள்,
    "cocoa": பெயர்கள்,
    "coconut": பெயர்கள்,
    "coffee": பெயர்கள்,
    "coir": பெயர்கள்,
    "cotton": பெயர்கள்,
    "cowpea": பெயர்கள்,
    "cranberry": பெயர்கள்,
    "cucumberetc": பெயர்கள்,
    "currant": பெயர்கள்,
    "date": பெயர்கள்,
    "eggplant": பெயர்கள்,
    "fibrenes": பெயர்கள்,
    "fig": பெயர்கள்,
    "flax": பெயர்கள்,
    "fonio": பெயர்கள்,
    "fornes": பெயர்கள்,
    "fruitnes": பெயர்கள்,
    "garlic": பெயர்கள்,
    "ginger": பெயர்கள்,
    "gooseberry": பெயர்கள்,
    "grape": பெயர்கள்,
    "grapefruitetc": பெயர்கள்,
    "grassnes": பெயர்கள்,
    "greenbean": பெயர்கள்,
    "greenbroadbean": பெயர்கள்,
    "greencorn": பெயர்கள்,
    "greenonion": பெயர்கள்,
    "greenpea": பெயர்கள்,
    "groundnut": பெயர்கள்,
    "gums": பெயர்கள்,
    "hazelnut": பெயர்கள்,
    "hemp": பெயர்கள்,
    "hempseed": பெயர்கள்,
    "hop": பெயர்கள்,
    "jute": பெயர்கள்,
    "jutelikefiber": பெயர்கள்,
    "kapokfiber": பெயர்கள்,
    "kapokseed": பெயர்கள்,
    "karite": பெயர்கள்,
    "kiwi": பெயர்கள்,
    "kolanut": பெயர்கள்,
    "legumenes": பெயர்கள்,
    "lemonlime": பெயர்கள்,
    "lentil": பெயர்கள்,
    "lettuce": பெயர்கள்,
    "linseed": பெயர்கள்,
    "lupin": பெயர்கள்,
    "maize": பெயர்கள்,
    "maizefor": பெயர்கள்,
    "mango": பெயர்கள்,
    "mate": பெயர்கள்,
    "melonetc": பெயர்கள்,
    "melonseed": பெயர்கள்,
    "millet": பெயர்கள்,
    "mixedgrain": பெயர்கள்,
    "mixedgrass": பெயர்கள்,
    "mushroom": பெயர்கள்,
    "mustard": பெயர்கள்,
    "nutmeg": பெயர்கள்,
    "nutnes": பெயர்கள்,
    "oats": பெயர்கள்,
    "oilpalm": பெயர்கள்,
    "oilseedfor": பெயர்கள்,
    "oilseednes": பெயர்கள்,
    "okra": பெயர்கள்,
    "olive": பெயர்கள்,
    "onion": பெயர்கள்,
    "orange": பெயர்கள்,
    "papaya": பெயர்கள்,
    "pea": பெயர்கள்,
    "peachetc": பெயர்கள்,
    "pear": பெயர்கள்,
    "pepper": பெயர்கள்,
    "peppermint": பெயர்கள்,
    "persimmon": பெயர்கள்,
    "pigeonpea": பெயர்கள்,
    "pimento": பெயர்கள்,
    "pineapple": பெயர்கள்,
    "pistachio": பெயர்கள்,
    "plantain": பெயர்கள்,
    "plum": பெயர்கள்,
    "popcorn": பெயர்கள்,
    "poppy": பெயர்கள்,
    "potato": பெயர்கள்,
    "pulsenes": பெயர்கள்,
    "pumpkinetc": பெயர்கள்,
    "pyrethrum": பெயர்கள்,
    "quince": பெயர்கள்,
    "quinoa": பெயர்கள்,
    "ramie": பெயர்கள்,
    "rapeseed": பெயர்கள்,
    "rasberry": பெயர்கள்,
    "rice": பெயர்கள்,
    "rootnes": பெயர்கள்,
    "rubber": பெயர்கள்,
    "rye": பெயர்கள்,
    "ryefor": பெயர்கள்,
    "safflower": பெயர்கள்,
    "sesame": பெயர்கள்,
    "sisal": பெயர்கள்,
    "sorghum": பெயர்கள்,
    "sorghumfor": பெயர்கள்,
    "sourcherry": பெயர்கள்,
    "soybean": பெயர்கள்,
    "spicenes": பெயர்கள்,
    "spinach": பெயர்கள்,
    "stonefruitnes": பெயர்கள்,
    "strawberry": பெயர்கள்,
    "stringbean": பெயர்கள்,
    "sugarbeet": பெயர்கள்,
    "sugarcane": பெயர்கள்,
    "sugarnes": பெயர்கள்,
    "sunflower": பெயர்கள்,
    "swedefor": பெயர்கள்,
    "sweetpotato": பெயர்கள்,
    "tangetc": பெயர்கள்,
    "taro": பெயர்கள்,
    "tea": பெயர்கள்,
    "tobacco": பெயர்கள்,
    "tomato": பெயர்கள்,
    "triticale": பெயர்கள்,
    "tropicalnes": பெயர்கள்,
    "tung": பெயர்கள்,
    "turnipfor": பெயர்கள்,
    "vanilla": பெயர்கள்,
    "vegetablenes": பெயர்கள்,
    "vegfor": பெயர்கள்,
    "vetch": பெயர்கள்,
    "walnut": பெயர்கள்,
    "watermelon": பெயர்கள்,
    "wheat": பெயர்கள்,
    "yam": பெயர்கள்,
    "yautia": பெயர்கள்,
}


def பயிர்க்கட்டம்_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
