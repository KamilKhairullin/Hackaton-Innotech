import json
import os
from financial_profile.providers.fsspProvider import FsspProvider
from financial_profile.providers.terroristProvider import TerroristProvider

if __name__ == '__main__':
    providers: list = [FsspProvider, TerroristProvider]
    data = {"firstname": "Иван", "lastname": "Иванов", "region": 1, "birthdate": "01.09.1962"}
    for provider in providers:
        print(provider.use(**data))

