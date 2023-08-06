import requests
from importlib import reload
from base64 import b64encode
import uuid
import json
import re
import random
import codecs
import datetime as dt
import csv
from dateutil.tz import gettz
from dateutil import parser
from .colors import color

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class IsoDateTime(object):

    def __init__(self, zone='America/Los_Angeles', iso=dt.datetime.now(gettz('America/Los_Angeles')).isoformat()):
        super(IsoDateTime, self).__init__()
        self.zone = zone
        self.iso = iso
    def tzone(self):
        return dt.datetime.now(gettz(self.zone))

    def retrieve_iso(self):
        return parser.parse(self.iso)

def get_uuid(stop, first3=''):
    num = uuid.uuid4().int
    num = str(num)[:stop]
    return f'{first3}{num}'

def get_hex_uuid(stop):
    num = uuid.uuid4().hex
    num = str(num)[:stop]
    return f'{num}'

def currency_formater(amount):
    amount = round(float(amount), 1)
    amount = '{:,}'.format(amount)
    return amount

def calculate_percent(percent, amount):
    return percent*amount/100

def save_image_from_url(model, image_url, proxies=None, verify=None):
    r = req.requests.get(
        url=image_url,
         proxies=proxies,
         verify=verify
         )
    req.urllibinsecure
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()
    model.image.save("image.jpg", File(img_temp), save=True)
    print('Image successfully saved')

def check_even_numbers(num, list):
    for num in list:
        if num % 2 == 0:
            print(num, end=" ")
