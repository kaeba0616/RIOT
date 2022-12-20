import requests
import time

import pandas as pd

from tqdm import tqdm

api_key = 'RGAPI-7c7d857b-1844-451d-a232-33360953f179'
sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + '고등학생' + '?api_key=' +api_key
r = requests.get(sohwan)

r.json()['id']

