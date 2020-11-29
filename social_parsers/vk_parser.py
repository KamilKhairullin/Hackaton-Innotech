import vk
from collections import Counter


class VkParser:

    def __init__(self, vk_token):
        self.session = vk.Session(access_token=vk_token)
        self.vk_api = vk.API(self.session, v=5.89)
        self.rel_dict = {1: "не женат/не замужем",
                         3: "помолвлен/помолвлена",
                         4: "женат/замужем",
                         8: "в гражданском браке",
                         2: "есть друг/есть подруга"}
        self.pers = {}

    def find_main_info(self, user_id):
        person = self.vk_api.users.get(user_ids=user_id, fields='city, country, contacts, connections,'
                                                                'universities, career,'
                                                                'relation, photo_200_orig, sex, bdate, counters')

        if 'deactivated' in person[0]:
            if person[0]['deactivated'] == 'deleted' or person[0]['deactivated'] == 'banned':
                return 'Пользователь удален или забанен'

        private = person[0]['is_closed']

        # f = open('person.txt', 'w')
        # f.write(str(person))
        firstname = person[0]['first_name']
        lastname = person[0]['last_name']
        country = 'не указано'
        city = 'не указано'
        jobs = []
        university = []
        relation = 0
        contacts = []
        military = 'не указано'
        mob_phone = 'не указано'
        home_phone = 'не указано'
        bdate = 'не указано'
        sex = 'не указано'
        photo_url = [person[0]['photo_200_orig']]

        if 'country' in person[0]:
            country = person[0]['country']['title']

        if 'city' in person[0]:
            city = person[0]['city']['title']

        if 'career' in person[0]:
            jobs = person[0]['career']

        if 'universities' in person[0]:
            university = person[0]['universities']

        if 'relation' in person[0]:
            relation = person[0]['relation']

        if relation in self.rel_dict.keys():
            relation = self.rel_dict[relation]
            if 'relation_partner' in person[0]:
                part_name = person[0]['relation_partner']['first_name'] + ' ' + person[0]['relation_partner'][
                    'last_name']
                partner = {
                    'relation': relation,
                    'name': part_name
                }
            else:
                partner = {
                    'relation': relation,
                    'name': 'не указано'
                }
        else:
            relation = 'не указано'
            partner = {
                'relation': relation
            }

        if 'bdate' in person[0]:
            bdate = person[0]['bdate']

        sex_id = person[0]['sex']
        if sex_id == 2:
            sex = 'мужской'
        elif sex_id == 1:
            sex = 'женский'

        if 'mobile_phone' in person[0]:
            mob_phone = person[0]['mobile_phone']

        if 'home_phone' in person[0]:
            home_phone = person[0]['home_phone']

        contacts.append({'home_phone': home_phone})
        contacts.append({'mob_phone': mob_phone})

        if 'military' in person[0]:
            military = person[0]['military']

        if 'facebook' in person[0]:
            contacts.append({'facebook': person[0]['facebook']})

        if 'instagram' in person[0]:
            contacts.append({'instagram': person[0]['instagram']})

        if 'skype' in person[0]:
            contacts.append({'skype': person[0]['skype']})

        if 'twitter' in person[0]:
            contacts.append({'twitter': person[0]['twitter']})

        # change id to city title
        # country not working because of authorization error
        for job in jobs:
            job['city_id'] = self.vk_api.database.getCitiesById(city_ids=job['city_id'])[0]['title']

        interests = []

        if not private:
            # find interests of user
            groups = self.vk_api.users.getSubscriptions(user_id=person[0]['id'], extended=True,
                                                        fields='activity, description')

            if groups['count'] > 0:

                groups = groups['items']
                for g in groups:
                    interests.append(g['activity'])
                interests = dict(Counter(interests))

                for i in interests.keys():
                    interests[i] = interests[i] / len(groups) * 100

        filtered_person = {

            'firstname': firstname,
            'lastname': lastname,
            'country': country,
            'birthdate': bdate,
            'sex': sex,
            'city': city,
            'job': jobs,
            'education': university,
            'contacts': contacts,
            'military': military,
            'photo': photo_url,
            'relation': partner,
            'interests': interests
        }
        self.pers = filtered_person
        return filtered_person

    # add photos from profile
    def get_profile_photos(self, vk_token_outh, user_id):
        session = vk.Session(access_token=vk_token_outh)
        vk_api = vk.API(session, v=5.89)
        person = vk_api.users.get(user_ids=user_id)
        print(person)
        if 'deactivated' in person[0]:
            return 'deactivated'

        if person[0]['is_closed']:
            return 'private'

        self.pers['photo'] = []
        photos = vk_api.photos.getProfile(owner_id=person[0]['id'])
        for photo in photos['items']:
            self.pers['photo'].append(photo['sizes'][len(photo['sizes']) - 1]['url'])
        return self.pers
