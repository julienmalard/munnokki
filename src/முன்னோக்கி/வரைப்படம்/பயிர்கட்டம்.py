import re
from functools import lru_cache
from numbers import Real
from typing import Optional

import xarray as xr

from .பரப்பிடம் import பரப்பிடம்
from ..அச்சுகள் import அகலாங்கு_அச்சு, நெட்டாங்கு_அச்சு
from ..கருவிகள்.பதிவிறக்கம் import ஜிப்_பதிவிறக்கம்


class பயிர்க்கட்டம்_பரப்பிடம்(பரப்பிடம்):
    நாடு_பெயர்கள் = {
        "கனடா": "Canada",
        "பாரதம்": "India"
    }
    def __init__(
        தன்,
        தரவு_கோப்புரை: Optional[str] = None,
        பதிவிறக்க_முகவரி="https://figshare.com/ndownloader/articles/22491997/versions/9",
    ):
        super().__init__(தரவு_கோப்புரை=தரவு_கோப்புரை)

        தன்.பதிவிறக்க_முகவரி = பதிவிறக்க_முகவரி
        தன்.நாட்டு_எண்கள் = தன்.நாட்டு_எண்களைத்_தொடங்கு()

    def நாட்டு_எண்களைத்_தொடங்கு(தன்) -> dict[str, int]:
        தரவுகள் = தன்.தரவுகளைப்_பெறு()

        எண்கள் = {}
        for பொருத்தம் in re.finditer(
                r"([0-9]+)\W+-\W+[A-Z]{2},\W+[A-Z]{3};\W+[0-9]+:([^>]+)>",
                தரவுகள்.attrs["List of countries"],
        ):
            எண்கள்[பொருத்தம்.group(2)] = int(பொருத்தம்.group(1))

        return எண்கள்

    def மறை(தன், இடம்) -> xr.DataArray:
        தரவுகள் = தன்.தரவுகளைப்_பெறு()

        நாட்டு_எண்கள் = [தன்.நாட்டு_எண்(நாடு) for நாடு in இடம்.நாடுகள்()]
        return தரவுகள்.isin(நாட்டு_எண்கள்)

    def பெட்டி(தன், இடம்) -> tuple[tuple[Real, Real], tuple[Real, Real]]:
        மறைக்கப்பட்டது = தன்.மறை(இடம்)
        ஆயக்கூறுகள் = மறைக்கப்பட்டது.where(மறைக்கப்பட்டது, drop=True).coords
        அகலாங்கு = ஆயக்கூறுகள்[அகலாங்கு_அச்சு]
        நெட்டாங்கு = ஆயக்கூறுகள்[நெட்டாங்கு_அச்சு]
        return (அகலாங்கு.min(), அகலாங்கு.max()), (நெட்டாங்கு.min(), நெட்டாங்கு.max())

    def தரவுகளைப்_பெறு(தன்) -> xr.DataArray:
        பதிவிறக்கம் = ஜிப்_பதிவிறக்கம்(
            உள்_கோப்பு_பாதை="Countries_2018.nc",
            பதிவிறக்க_முகவரி=தன்.பதிவிறக்க_முகவரி,
            தரவு_கோப்புரை=தன்.தரவு_கோப்புரை,
        )
        தரவுகள் = பதிவிறக்கம்.தரவுத்தளத்தைப்_பெறு().rename(
            {"lat": அகலாங்கு_அச்சு, "lon": நெட்டாங்கு_அச்சு}
        )

        return தரவுகள்["country"]

    def நாட்டு_எண்(தன், நாடு) -> int:
        return தன்.நாட்டு_எண்கள்[தன்.நாடு_பெயர்கள்[str(நாடு)]]


"""
2  Afghanistan 
4  Albania 
5  Algeria 
6  Andorra 
7  Angola 
8  Antigua 
9  Argentina 
10  Armenia 
12  Australia 
13  Austria 
14  Azerbaijan 
15  Bahamas 
16  Bahrain 
17  Bangladesh 
18  Barbados 
19  Belarus 
20  Belgium 
21  Belize 
22  Benin 
23  Bhutan 
24  Bolivia 
25  Bosnia Herzeg. 
26  Botswana 
27  Brazil 
28  Brunei 
29  Bulgaria 
30  Burkina Faso 
31  Burundi 
32  Cambodia 
33  Cameroon 
34  Canada 
35  Cape Verde 
36  Cayman Islands 
37  Central Africa 
38  Chad 
39  Chile 
40  China 
42  Colombia 
43  Comoros 
44  Congo 
45  Costa Rica 
46  Croatia 
47  Cuba 
48  Cyprus 
49  Czech Republic 
50 
51  D.R. Congo 
52  Denmark 
53  Djibouti 
54  Dominica 
55  Dominican R. 
56  Ecuador 
57  Egypt 
58  El Salvador 
59  Equat. Guinea 
60  Eritrea 
61  Estonia 
62  Ethiopia 
63  FYR Macedonia 
64  Falkland 
65  Faroe Islands 
66  Fiji 
67  Finland 
68  France 
69  French Guiana 
70  French Polynesia 
71  French S.A.T. 
72  Gabon 
73  Gambia 
75  Georgia 
76  Germany 
77  Ghana 
78  Greece 
79  Greenland 
80  Grenada 
81  Guadeloupe 
82  Guam 
83  Guatemala 
84  Guinea 
85  Guinea-Bissau 
86  Guyana 
87  Haiti 
89  Heard Island 
90  Honduras 
91  Hong Kong 
92  Hungary 
93  Iceland 
95  India 
96  Indonesia 
97  Iran 
98  Iraq 
99  Ireland 
100  Isle of Man 
101  Israel 
102  Italy 
103  Jamaica 
105  Japan 
106  Jordan 
107  Kazakhstan 
108  Kenya 
110  Kiribati 
112  Kuwait 
113  Kyrgyzstan 
114  Laos 
115  Latvia 
116  Lebanon 
117  Lesotho 
118  Liberia 
119  Libya 
120  Lithuania 
121  Luxembourg 
123  Madagascar 
124  Malawi 
125  Malaysia 
126  Mali 
127  Malta 
128  Martinique 
129  Mauritania 
130  Mauritius 
131  Mayotte 
132  Mexico 
133  Micronesia 
134  Moldova 
135  Mongolia 
136  Montenegro 
137  Morocco 
138  Mozambique 
139  Myanmar 
140  Namibia 
141  Nepal 
143  Netherlands 
144  New Caledonia 
145  New Zealand 
146  Nicaragua 
147  Niger 
148  Nigeria 
149  Niue 
150  North Korea 
151  Norway 
152  Oman 
153  Pakistan 
154  Palau 
155  Panama 
156  Papua New Guinea 
157  Paraguay 
158  Peru 
159  Philippines 
160  Poland 
161  Portugal 
162  Puerto Rico 
163  Qatar 
164  Romania 
165  Russian Fed. 
166  Rwanda 
168  Saint Lucia 
171  Samoa 
172  Sao Tome and P. 
173  Saudi Arabia 
174  Senegal 
175  Serbia 
176  Sierra Leone 
177  Singapore 
178  Slovakia 
179  Slovenia 
180  Solomon Islands 
181  Somalia 
182  South Africa 
183  South Georgia 
184  South Korea 
185  South Sudan 
186  Spain 
187  Sri Lanka 
188  Sudan 
189  Suriname 
190  Svalbard 
191  Swaziland 
192  Sweden 
193  Switzerland 
194  Syria 
195  Taiwan 
196  Tajikistan 
197  Tanzania 
198  Thailand 
199  Timor-Leste 
200  Togo 
201  Tonga 
202  Trinidad Tobago 
203  Tunisia 
204  Turkey 
205  Turkmenistan 
206  U.A.E. 
207  U.K. 
208  USA 
209  Uganda 
210  Ukraine 
211  Uruguay 
212  Uzbekistan 
213  Vanuatu 
214  Venezuela 
215  Viet Nam 
216  Virgin Islands 
218  Western Sahara 
219  Yemen 
220  Zambia 
221  Zimbabwe 
"""
