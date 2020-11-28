import json
import os

from financial_profile.providers.provider import Provider


class TerroristProvider(Provider):
    @staticmethod
    def provide_data(first_name: str, last_name: str, birthdate: str):
        first_name = first_name.upper()
        last_name = last_name.upper()
        with open('financial_profile/data/terrorist.json') as file:
            data = json.load(file)
            for pdata in data:
                if pdata['firstname'] == first_name and pdata['lastname'] == last_name \
                        and pdata['birthdate'] == birthdate:
                    return True
            return False

    @staticmethod
    def use(**kwargs) -> str:
        first_name = kwargs.get('firstname')
        last_name = kwargs.get('lastname')
        birthdate = kwargs.get('birthdate')
        if TerroristProvider.provide_data(first_name, last_name, birthdate):
            return 'is terrorist'
