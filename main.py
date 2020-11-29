import json
import os
from financial_profile.providers.fsspProvider import FsspProvider
from financial_profile.providers.terroristProvider import TerroristProvider
from social_parsers.vk_parser import VkParser

if __name__ == '__main__':
    os.environ['fssp_token'] = 'W9kswdsrfD2J'
    # need service token for vk api
    token = '4ab0cb4a4ab0cb4a4ab0cb4ac94ac5fb6044ab04ab0cb4a1572d740b850b9712aee47bb'
    token_photos = '4f7364932210ac1e6a8c636f7efaa378e9d7c90c9455a8d62e401ff6b0fedd4ead4903493722ee88ee3d7'
    # pass token to social_parsers, find info accepts id of vk user

    user_id = 'id486226681'
    vk_parser = VkParser(token)
    # parse user account
    data = vk_parser.find_main_info(user_id)
    print(data)
    providers: list = [FsspProvider, TerroristProvider]
    for provider in providers:
        print(provider.use(**data))
