import http
import http.client
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs

import numpy as np
import pytest
import requests as rq
import xarray as xr
import xarray.testing as xrt
from rasterio import MemoryFile
from requests_mock.response import _IOReader
from urllib3 import HTTPResponse
from urllib3.util import parse_url

from முன்னோக்கி.அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from முன்னோக்கி.காலநிலை.காலநிலை import காலநிலை_குறிப்பு
from முன்னோக்கி.தாள் import ஒற்றுமைக்_குறிப்பு
from முன்னோக்கி.மண்.பண்புகள் import பண்புகள் as ப
from முன்னோக்கி.மண்.மண்கட்டம்.மண்கட்டம் import மண்கட்டம், ஓஸிஸ்_மண்_வகைகள்
from முன்னோக்கி.மண்.மாறிலிகள் import மண்_ஆழ_அச்சு, மண்_மாறி_அச்சு


@pytest.fixture
def சுமா_மண்க்கட்டம்(requests_mock):
    def சோதனைத்_தரவுகள்(கோரிக்கை: rq.Request, சூழல்):
        மாறிகள் = parse_qs(parse_url(கோரிக்கை.url).query)
        assert "WCS" in மாறிகள்["service"]
        மாறி = மாறிகள்["map"][0].replace(r"/map/", "").replace(r".map", "")
        if "GetCapabilities" == மாறிகள்["request"][0]:
            return HTTPResponse(
                status=200,
                reason=http.client.responses.get(200),
                body=_IOReader(
                    f'<?xml version=\'1.0\' encoding="UTF-8" standalone="no" ?>\n<WCS_Capabilities\n   version="1.0.0" \n   updateSequence="0" \n   xmlns="http://www.opengis.net/wcs" \n   xmlns:xlink="http://www.w3.org/1999/xlink" \n   xmlns:gml="http://www.opengis.net/gml" \n   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n   xsi:schemaLocation="http://www.opengis.net/wcs http://schemas.opengis.net/wcs/1.0.0/wcsCapabilities.xsd">\n<Service>\n  <description>Soilgrids layers provided by ISRIC - World Soil Information</description>\n  <name>MapServer WCS</name>\n<!-- WARNING: Mandatory metadata "wcs_label" or "ows_label" was missing in this context. -->\n  <keywords>\n    <keyword>bulk density</keyword>\n    <keyword>digital soil mapping</keyword>\n    <keyword>Soil science</keyword>\n    <keyword>Global</keyword>\n    <keyword>geoscientificInformation</keyword>\n  </keywords>\n<responsibleParty>\n    <individualName>Luis Calisto</individualName>\n    <organisationName>ISRIC - World Soil Reference</organisationName>\n    <positionName>SDI manager</positionName>\n  <contactInfo>\n    <phone>\n    <voice>+31 317 483 735</voice>\n    <facsimile>+31 317 483 735</facsimile>\n    </phone>\n    <address>\n    <deliveryPoint>Droevendaalsesteeg 3, 6708 PB</deliveryPoint>\n    <city>Wageningen</city>\n    <administrativeArea>Gelderland</administrativeArea>\n    <postalCode>6708PB</postalCode>\n    <country>The Netherlands</country>\n    <electronicMailAddress>soilgrids@isric.org</electronicMailAddress>\n    </address>\n    <onlineResource xlink:type="simple" xlink:href="https://maps.isric.org/"/>\n  </contactInfo>\n</responsibleParty>\n  <fees>None</fees>\n  <accessConstraints>\n    None\n  </accessConstraints>\n</Service>\n<Capability>\n  <Request>\n    <GetCapabilities>\n      <DCPType>\n        <HTTP>\n          <Get><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Get>\n        </HTTP>\n      </DCPType>\n      <DCPType>\n        <HTTP>\n          <Post><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Post>\n        </HTTP>\n      </DCPType>\n    </GetCapabilities>\n    <DescribeCoverage>\n      <DCPType>\n        <HTTP>\n          <Get><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Get>\n        </HTTP>\n      </DCPType>\n      <DCPType>\n        <HTTP>\n          <Post><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Post>\n        </HTTP>\n      </DCPType>\n    </DescribeCoverage>\n    <GetCoverage>\n      <DCPType>\n        <HTTP>\n          <Get><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Get>\n        </HTTP>\n      </DCPType>\n      <DCPType>\n        <HTTP>\n          <Post><OnlineResource xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;" /></Post>\n        </HTTP>\n      </DCPType>\n    </GetCoverage>\n  </Request>\n  <Exception>\n    <Format>application/vnd.ogc.se_xml</Format>\n  </Exception>\n</Capability>\n<ContentMetadata>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_Q0.5"/>    <name>{மாறி}_0-5cm_Q0.5</name>\n    <label>{மாறி}_0-5cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_Q0.05"/>    <name>{மாறி}_0-5cm_Q0.05</name>\n    <label>{மாறி}_0-5cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_Q0.95"/>    <name>{மாறி}_0-5cm_Q0.95</name>\n    <label>{மாறி}_0-5cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_mean"/>    <name>{மாறி}_0-5cm_mean</name>\n    <label>{மாறி}_0-5cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_uncertainty"/>    <name>{மாறி}_0-5cm_uncertainty</name>\n    <label>{மாறி}_0-5cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_5-15cm_Q0.5"/>    <name>{மாறி}_5-15cm_Q0.5</name>\n    <label>{மாறி}_5-15cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_5-15cm_Q0.05"/>    <name>{மாறி}_5-15cm_Q0.05</name>\n    <label>{மாறி}_5-15cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_5-15cm_Q0.95"/>    <name>{மாறி}_5-15cm_Q0.95</name>\n    <label>{மாறி}_5-15cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_5-15cm_mean"/>    <name>{மாறி}_5-15cm_mean</name>\n    <label>{மாறி}_5-15cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_5-15cm_uncertainty"/>    <name>{மாறி}_5-15cm_uncertainty</name>\n    <label>{மாறி}_5-15cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_15-30cm_Q0.5"/>    <name>{மாறி}_15-30cm_Q0.5</name>\n    <label>{மாறி}_15-30cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_15-30cm_Q0.05"/>    <name>{மாறி}_15-30cm_Q0.05</name>\n    <label>{மாறி}_15-30cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_15-30cm_Q0.95"/>    <name>{மாறி}_15-30cm_Q0.95</name>\n    <label>{மாறி}_15-30cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_15-30cm_mean"/>    <name>{மாறி}_15-30cm_mean</name>\n    <label>{மாறி}_15-30cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_15-30cm_uncertainty"/>    <name>{மாறி}_15-30cm_uncertainty</name>\n    <label>{மாறி}_15-30cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_30-60cm_Q0.05"/>    <name>{மாறி}_30-60cm_Q0.05</name>\n    <label>{மாறி}_30-60cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_30-60cm_Q0.5"/>    <name>{மாறி}_30-60cm_Q0.5</name>\n    <label>{மாறி}_30-60cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_30-60cm_Q0.95"/>    <name>{மாறி}_30-60cm_Q0.95</name>\n    <label>{மாறி}_30-60cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_30-60cm_mean"/>    <name>{மாறி}_30-60cm_mean</name>\n    <label>{மாறி}_30-60cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_30-60cm_uncertainty"/>    <name>{மாறி}_30-60cm_uncertainty</name>\n    <label>{மாறி}_30-60cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_60-100cm_Q0.05"/>    <name>{மாறி}_60-100cm_Q0.05</name>\n    <label>{மாறி}_60-100cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_60-100cm_Q0.5"/>    <name>{மாறி}_60-100cm_Q0.5</name>\n    <label>{மாறி}_60-100cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_60-100cm_Q0.95"/>    <name>{மாறி}_60-100cm_Q0.95</name>\n    <label>{மாறி}_60-100cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_60-100cm_mean"/>    <name>{மாறி}_60-100cm_mean</name>\n    <label>{மாறி}_60-100cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_60-100cm_uncertainty"/>    <name>{மாறி}_60-100cm_uncertainty</name>\n    <label>{மாறி}_60-100cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_100-200cm_Q0.05"/>    <name>{மாறி}_100-200cm_Q0.05</name>\n    <label>{மாறி}_100-200cm_Q0.05</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_100-200cm_Q0.5"/>    <name>{மாறி}_100-200cm_Q0.5</name>\n    <label>{மாறி}_100-200cm_Q0.5</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_100-200cm_Q0.95"/>    <name>{மாறி}_100-200cm_Q0.95</name>\n    <label>{மாறி}_100-200cm_Q0.95</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_100-200cm_mean"/>    <name>{மாறி}_100-200cm_mean</name>\n    <label>{மாறி}_100-200cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n  <CoverageOfferingBrief>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_100-200cm_uncertainty"/>    <name>{மாறி}_100-200cm_uncertainty</name>\n    <label>{மாறி}_100-200cm_uncertainty</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n  </CoverageOfferingBrief>\n</ContentMetadata>\n</WCS_Capabilities>\n'.encode(
                        "utf-8"
                    )
                ),
                decode_content=False,
                enforce_content_length=False,
                preload_content=False,
                original_response=None,
            )
        elif "DescribeCoverage" == மாறிகள்["request"][0]:
            return HTTPResponse(
                status=200,
                reason=http.client.responses.get(200),
                body=_IOReader(
                    '<?xml version=\'1.0\' encoding="UTF-8" ?>\n<CoverageDescription\n   version="1.0.0" \n   updateSequence="0" \n   xmlns="http://www.opengis.net/wcs" \n   xmlns:xlink="http://www.w3.org/1999/xlink" \n   xmlns:gml="http://www.opengis.net/gml" \n   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n   xsi:schemaLocation="http://www.opengis.net/wcs http://schemas.opengis.net/wcs/1.0.0/describeCoverage.xsd">\n  <CoverageOffering>\n  <metadataLink metadataType="TC211" xlink:type="simple" xlink:href="https://maps.isric.org/mapserv?map=/map/{மாறி}.map&amp;request=GetMetadata&amp;layer={மாறி}_0-5cm_mean"/>  <name>{மாறி}_0-5cm_mean</name>\n  <label>{மாறி}_0-5cm_mean</label>\n    <lonLatEnvelope srsName="urn:ogc:def:crs:OGC:1.3:CRS84">\n      <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n      <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n    </lonLatEnvelope>\n  <keywords>\n    <keyword></keyword>\n  </keywords>\n    <domainSet>\n      <spatialDomain>\n        <gml:Envelope srsName="EPSG:4326">\n          <gml:pos>-179.991347553068 -55.9773009202418</gml:pos>\n          <gml:pos>179.994461880094 82.7192840534453</gml:pos>\n        </gml:Envelope>\n        <gml:Envelope srsName="EPSG:152160">\n          <gml:pos>-19949000 -6147500</gml:pos>\n          <gml:pos>19861750 8361000</gml:pos>\n        </gml:Envelope>\n        <gml:RectifiedGrid dimension="2">\n          <gml:limits>\n            <gml:GridEnvelope>\n              <gml:low>0 0</gml:low>\n              <gml:high>159242 58033</gml:high>\n            </gml:GridEnvelope>\n          </gml:limits>\n          <gml:axisName>x</gml:axisName>\n          <gml:axisName>y</gml:axisName>\n          <gml:origin>\n            <gml:pos>-19949000 8361000</gml:pos>\n          </gml:origin>\n          <gml:offsetVector>250 0</gml:offsetVector>\n          <gml:offsetVector>0 -250</gml:offsetVector>\n        </gml:RectifiedGrid>\n      </spatialDomain>\n    </domainSet>\n    <rangeSet>\n      <RangeSet>\n        <name>range1</name>\n        <label>label1</label>\n        <nullValues>\n          <singleValue>-32768</singleValue>\n        </nullValues>\n      </RangeSet>\n    </rangeSet>\n    <supportedCRSs>\n      <requestResponseCRSs>EPSG:152160</requestResponseCRSs>\n      <requestResponseCRSs>EPSG:4326</requestResponseCRSs>\n      <requestResponseCRSs>EPSG:3857</requestResponseCRSs>\n      <requestResponseCRSs>EPSG:54012</requestResponseCRSs>\n      <nativeCRSs>EPSG:152160</nativeCRSs>\n    </supportedCRSs>\n    <supportedFormats>\n      <formats>GEOTIFF_INT16</formats>\n    </supportedFormats>\n    <supportedInterpolations default="nearest neighbor">\n      <interpolationMethod>nearest neighbor</interpolationMethod>\n      <interpolationMethod>bilinear</interpolationMethod>\n    </supportedInterpolations>\n  </CoverageOffering>\n</CoverageDescription>\n'.encode(
                        "utf-8"
                    )
                ),
                decode_content=False,
                enforce_content_length=False,
                preload_content=False,
                original_response=None,
            )
        elif "GetCoverage" == மாறிகள்["request"][0]:
            அளவுகள் = [float(இ) for இ in மாறிகள்["BBox"][0].split(",")]
            அகலம் = float(மாறிகள்["width"][0])
            உயரம் = float(மாறிகள்["height"][0])
            அகல_படி = (அளவுகள்[2] - அளவுகள்[0]) / அகலம்
            உயர_படி = (அளவுகள்[3] - அளவுகள்[1]) / உயரம்
            நெட்டாங்கு = np.arange(அளவுகள்[0], அளவுகள்[2], அகல_படி)
            அகலாங்கு = np.arange(அளவுகள்[1], அளவுகள்[3], உயர_படி)

            தரவுகள் = xr.DataArray(
                np.random.random(நெட்டாங்கு.size * அகலாங்கு.size).reshape(
                    (1, நெட்டாங்கு.size, அகலாங்கு.size, 1)
                ),
                coords={
                    "band": [1],
                    "x": நெட்டாங்கு,
                    "y": அகலாங்கு,
                    "spatial_ref": 0,
                },
                dims=("band", "y", "x", "spatial_ref"),
                attrs={"_FillValue": -32768},
            )
            with MemoryFile() as memfile:
                தரவுகள்.squeeze().rio.to_raster(memfile.name)
                return HTTPResponse(
                    status=200,
                    reason=http.client.responses.get(200),
                    body=_IOReader(memfile.read()),
                    decode_content=False,
                    enforce_content_length=False,
                    preload_content=False,
                    original_response=None,
                    headers={"Content-Type": "tiff"},
                )

        return HTTPResponse(status=404)

    requests_mock.get("https://maps.isric.org/mapserv", raw=சோதனைத்_தரவுகள்)


def மறையுடன்_தரவுகளைப்_பெறு_சோதிக்க(சுமா_மண்க்கட்டம்):
    மறை = xr.DataArray(
        1,
        coords={
            அகலாங்கு_அச்சு: np.arange(0, 10, 0.5),
            நெட்டாங்கு_அச்சு: np.arange(0, 7, 0.5),
        },
        dims=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு],
    )
    ஆழம் = [0, 10]
    மாறிகள் = [ப["அமில_காரத்தன்மை"], ப["களிமண்"]]
    with TemporaryDirectory() as தற்காலிகமானது:
        தரவுகள் = மண்கட்டம்(
            ஆழம்=ஆழம், மாறிகள்=மாறிகள், தரவு_கோப்புரை=தற்காலிகமானது, துள்ளியம்=(2, 2)
        ).தரவுகளைப்_பெறு(மறை=மறை)
        xrt.assert_equal(
            தரவுகள்.coords,
            xr.Coordinates(
                {
                    அகலாங்கு_அச்சு: np.arange(-10, 10, 0.5),
                    நெட்டாங்கு_அச்சு: np.arange(-20, 20, 0.5),
                    மண்_ஆழ_அச்சு: ஆழம்,
                    மண்_மாறி_அச்சு: மாறிகள்,
                }
            ),
        )


def ஓஸிஸ்_ஒற்றுமையைச்_சோதிக்க():
    class சோதனை_ஓஸிஸ்_மண்_வகைகள்(ஓஸிஸ்_மண்_வகைகள்):
        def தரவுகளைப்_பெறு(தன், மறை=None):
            return xr.DataArray(
                np.random.randint(1, 25, size=40 * 80).reshape((40, 80)),
                coords={
                    அகலாங்கு_அச்சு: np.arange(-10, 10, 0.5),
                    நெட்டாங்கு_அச்சு: np.arange(-20, 20, 0.5),
                },
                dims=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு],
            )

    மறை = xr.DataArray(
        1,
        coords={
            அகலாங்கு_அச்சு: np.arange(0, 10, 0.5),
            நெட்டாங்கு_அச்சு: np.arange(0, 7, 0.5),
        },
        dims=[அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு],
    )

    with TemporaryDirectory() as தற்காலிகமானது:
        குறிப்பு = ஒற்றுமைக்_குறிப்பு(காலநிலை=காலநிலை_குறிப்பு(2050))
        ஒற்றுமை = சோதனை_ஓஸிஸ்_மண்_வகைகள்(
            தரவு_கோப்புரை=தற்காலிகமானது, துள்ளியம்=(2, 2)
        ).ஒற்றுமை(0, 0, குறிப்பு, மறை=மறை)

        xrt.assert_equal(
            ஒற்றுமை.coords,
            xr.Coordinates(
                {
                    அகலாங்கு_அச்சு: np.arange(-10, 10, 0.5),
                    நெட்டாங்கு_அச்சு: np.arange(-20, 20, 0.5),
                }
            ),
        )

        assert ஒற்றுமை.min() == 0
        assert ஒற்றுமை.max() == 1

        assert bool(ஒற்றுமை.sel({அகலாங்கு_அச்சு: [0], நெட்டாங்கு_அச்சு: [0]}) == 1) is True

