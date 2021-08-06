import requests
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

IP_STACK_API_KEY = os.environ.get('IP_STACK_API_KEY')


class IpInfoError(Exception):
    def __init__(self):
        self.message = f'Error in Ip Info'

# TODO: REMOVE ME :)
# @lru_cache(maxsize=200)
# def ip_info(ip):
#     # FREE SUBSCRIPTION OF IP_STACK DON'T GIVE HTTPS ACCESS
#     res = requests.get(
#         url=f'http://api.ipstack.com/{ip}?access_key={IP_STACK_API_KEY}'
#     )
#     if res.status_code >= 300:
#         raise IpInfoError()
#     data = res.json()
#     country_code = data.get('country_code', 1)
#     region_code = data.get('')
#     city = data.get('')
#     zip_code = data.get('zip')
#     latitude = data.get('')
#     longitude = data.get('')
