import requests
import json
import os


def parse(region: int, first_name: str, last_name: str, birthdate: str):
    req = f'?token={os.environ["token"]}&' \
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
        res.append(d["result"])
    return res
