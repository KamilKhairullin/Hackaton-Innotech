import json

from financial_profile.providers.provider import Provider


class TrialsProvider(Provider):
    @staticmethod
    def provide_data(first_name: str, last_name: str):
        first_name = first_name.upper()
        last_name = last_name.upper()
        fi = first_name + '.' + last_name
        res = []
        with open('financial_profile/data/trails.json') as file:
            data = json.load(file)
            for pdata in data:
                name = pdata['defendant']
                if name[0: len(name) - 2] == fi:
                    res.append(pdata)
        return res

    @staticmethod
    def use(**kwargs):
        first_name = kwargs.get('firstname')
        last_name = kwargs.get('lastname')
        res = TrialsProvider.provide_data(first_name, last_name)
        return res
