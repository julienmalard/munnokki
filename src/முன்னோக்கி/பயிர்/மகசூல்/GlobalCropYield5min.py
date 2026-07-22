from ..மகசூல் import மகசூல்
from .. import பயிர்_பெயர்கள் as பெயர்கள்

# https://data.mendeley.com/datasets/hg8wzgx4yp/4
# https://www.nature.com/articles/s41597-024-04248-2#Sec5
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/G1HBNK


class GlobalCropYield5min(மகசூல்):
    def __init__(தன், பதிவிறக்கம்_முகவரி="https://data.mendeley.com/public-files/datasets/hg8wzgx4yp/files/75ae8d3f-85d1-484f-bd82-5f6c35c2e252/file_downloaded"):
        தன்.பதிவிறக்கம்_முகவரி = பதிவிறக்கம்_முகவரி

பெயர்_சமானம் = {
    "Maize": பெயர்கள்.மக்காச்சோளம்,
    "Rice": பெயர்கள்.நெல்,
    "Soybean": பெயர்கள்.சோயா,
    "Wheat": பெயர்கள்.கோதுமை,
}
