import requests
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

IP_STACK_API_KEY = os.environ.get('IP_STACK_API_KEY')


class IpInfoError(Exception):
    def __init__(self):
        self.message = f'Error in Ip Info'
