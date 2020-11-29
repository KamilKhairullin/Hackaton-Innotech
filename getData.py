import os
from financial_profile.providers.fsspProvider import FsspProvider
from financial_profile.providers.terroristProvider import TerroristProvider
from social_parsers.vkParser import VkParser
import urllib.request


def get_data(user_id: str):
    os.environ['fssp_token'] = 'W9kswdsrfD2J'
    # need service token for vk api
    token = ''
    token_photos = ''
    # pass token to social_parsers, find info accepts id of vk user
    user_id = 'id486226681'
    vk_parser = VkParser(token)
    # parse user account
    data = vk_parser.find_main_info(user_id)
    print(data)
    providers: list = [FsspProvider, TerroristProvider]
    for provider in providers:
        print(provider.use(**data))


def get_photos(user_id: str):
    os.environ['fssp_token'] = ''
    # need service token for vk api
    token = ''
    token_photos = ''
    # pass token to social_parsers, find info accepts id of vk user
    user_id = 'id486226681'
    vk_parser = VkParser(token)
    vk_parser.find_main_info(user_id)
    photos = vk_parser.get_profile_photos(token_photos, user_id)
    cnt = 0
    for photo in photos:
        response = urllib.request.urlopen(photo)
        data = response.read()
        with open(f'drive/MyDrive/Server/static/dataset/train/{user_id}_{cnt}.png', 'wb') as f:
            f.write(data)
            cnt += 1


if __name__ == '__main__':
    get_photos('id268922389')
