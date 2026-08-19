from typing import Optional

import pybtex
import xarray as xr
from pybtex.database import Entry

from .நீர்பாசனம் import நீர்பாசனம்


# https://figshare.com/collections/Global_Irrigation_Water_Sources_Maps/7318916
# https://www.nature.com/articles/s41597-025-05920-x#Sec7
class ஃபங்கவெய்(நீர்பாசனம்):
    def தரவுகளைப்_பெறு(தன், பயிர்கள்: Optional[list[str]]) -> xr.DataArray:
        pass

    def மேற்கோள்(தன்):
        return [
            pybtex.database.parse_string(
                """@misc{hung_chiarelli_famiglietti_muller_2024, title={Global Irrigation Water Sources Maps}, url={https://figshare.com/collections/Global_Irrigation_Water_Sources_Maps/7318916/2}, DOI={10.6084/m9.figshare.c.7318916}, abstractNote={This dataset identifies irrigation water sources, including rainfed, surface water, and groundwater, for the year 2000, 2005, 2010, and 2015, at a global scale with a 60-meter resolution. }, publisher={figshare}, author={Hung, Fengwei and Chiarelli, Davide Danilo and Famiglietti, James S and Muller, Marc F.}, year={2024}, month={Jul} }""",
                bib_format="bibtex",
            ),
            pybtex.database.parse_string(
                """TY  - JOUR\nAU  - Hung, Fengwei\nAU  - Chiarelli, Davide Danilo\nAU  - Famiglietti, James S.\nAU  - Müller, Marc F.\nPY  - 2025\nDA  - 2025/10/09\nTI  - Downscaled global 60-meter resolution estimates of irrigation water sources (2000–2015)\nJO  - Scientific Data\nSP  - 1632\nVL  - 12\nIS  - 1\nAB  - This dataset provides high-resolution (60 m) global irrigation maps to support water resource and agricultural management. It identifies the likely irrigation status (rainfed or irrigated) and water source (groundwater or surface water) of croplands for 2000, 2005, 2010, and 2015. We downscaled a 10-km irrigation dataset derived from national and subnational statistics (GMIA) using (i) spatial patterns between high-resolution (30 m) cropland and nearby surface water, and (ii) irrigation water requirements from a global crop model. Validation used household agriculture surveys in India (N = 8,355) and a U.S. well database (N = 1,505,371). In the U.S., our method achieved 85% accuracy in distinguishing groundwater use within 2 km of wells – substantially higher than GMIA (25%). In India’s groundwater-dominated regions, our estimates performed comparably to GMIA (73% vs. 72%). These results suggest our dataset offers a more accurate and spatially detailed representation of irrigation water sources, enabling improved analysis of agricultural water use.\nSN  - 2052-4463\nUR  - https://doi.org/10.1038/s41597-025-05920-x\nDO  - 10.1038/s41597-025-05920-x\nID  - Hung2025\nER  - """,
                bib_format="ris",
            ),
        ]
