#  https://doi.org/10.7910/DVN/G1HBNK
from .மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்


class GGCP10(மகசூல்):
    def __init__(தன், ஆண்டு=2020):
        தன்.ஆண்டு = ஆண்டு

    def கோப்பு_முகவரி(தன், பயிர்_பெயர்: str):
        return f"GGCP10_Production_{தன்.ஆண்டு}_{GGCP10_பெயர்(பயிர்_பெயர்)}.tif"


பெயர்_சமானம் = {
    "Maize": பெயர்கள்.மக்காச்சோளம்,
    "Rice": பெயர்கள்.நெல்,
    "Soybean": பெயர்கள்.சோயா,
    "Wheat": பெயர்கள்.கோதுமை,
}


def GGCP10_பெயர்(பெயர்: str):
    try:
        return next(பெ for பெ in பெயர்_சமானம்.keys() if பெயர்_சமானம்[பெ] == பெயர்)
    except StopIteration:
        return பெயர்
