import time

import requests
import json
import os

from financial_profile.providers.provider import Provider


class FsspProvider(Provider):
    @staticmethod
    def provide_data(first_name: str, last_name: str, region: int, birthdate: str):
        first_name = first_name.upper()
        last_name = last_name.upper()
        req = f'?token={os.environ["fssp_token"]}&' \
              f'region={region}&' \
              f'firstname={first_name}&' \
              f'lastname={last_name}&' \
              f'birthdate={birthdate}'
        response = requests.get(f'http://api-ip.fssprus.ru/api/v1.0/search/physical{req}')
        resp_data: dict = json.loads(response.content)
        task = resp_data['response']['task']
        req = f'?token={"W9kswdsrfD2J"}&' \
              f'task={task}'
        response = requests.get(f'http://api-ip.fssprus.ru/api/v1.0/result{req}')
        resp_data = json.loads(response.content)
        debts = resp_data['response']['result']
        res = []
        for d in debts:
            if d["result"]:
                res.append(d["result"])
        return res

    @staticmethod
    def use(**kwargs) -> str:
        first_name = kwargs.get('firstname')
        last_name = kwargs.get('lastname')
        city = kwargs.get('city')
        birthdate = kwargs.get('birthdate')
        try:
            with open('financial_profile/data/city_number.json', 'r') as f:
                cr = json.load(f)
                region = int(cr[city])
        except KeyError:
            region = 50
        cnt = 0
        res = []
        while not res and cnt < 10:
            res = FsspProvider.provide_data(first_name, last_name, region, birthdate)
            cnt += 1
            time.sleep(0.5)
        if len(res):
            return json.dumps(res)
