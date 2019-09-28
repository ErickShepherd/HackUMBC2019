# Third party imports.
import requests

# Constant definitions.
API_ENDPOINT_BASE_URL = "http://catalog.data.gov/api/3/"

"""

https://api.census.gov/data/

    <year>/
    timeseries/

"""


response = requests.get(url = API_ENDPOINT_BASE_URL)
data     = response.json()
