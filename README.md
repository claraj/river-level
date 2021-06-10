# River info API

Simplified data originally from https://waterservices.usgs.gov/ and APIs generated and tested with https://waterservices.usgs.gov/rest/IV-Test-Tool.html

An example API route, fetching flow (00060), gauge height (00065) and temperature (00011) at the Mississippi River in Saint Paul, site 05331000,  https://waterservices.usgs.gov/nwis/iv?format=json&sites=05331000&parameterCd=00060,00065,00011&siteStatus=all

Finding site numbers: https://maps.waterdata.usgs.gov/mapper/

For example,
Mississippi River in St Paul 05331000
Mississippi River in Fridley 05288670
Mississippi River in Brooklyn Park, 05288500
Minnehaha Creek at Hiawatha Avenue in south Minneapolis 05289800
Shingle Creek, north Minneapolis 05288705

To use this API, you can only set the site number and number of days of data leading up to today. The API returns the gauge height for the river. 

Examples: 

http://127.0.0.1:5000/api/river/05331000/3   Three days of data for the Mississippi in St. Paul. 
http://127.0.0.1:5000/api/river/05288705/365    365 days of data for Shingle Creen in Minneapolis.

The number of days must be between 1 and 365.

The original API is slower when requesting larger amounts of data. If you want a year of data, it will take a few seconds. 