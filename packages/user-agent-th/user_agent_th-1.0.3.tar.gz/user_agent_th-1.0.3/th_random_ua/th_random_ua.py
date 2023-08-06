import json
import random

with open('data/random_ua.json', 'r', encoding='utf-8') as p:
    list_user_agent = json.loads(p.read())


class RandomUA:

    def __init__(self):
        self.list_user_agent = list_user_agent
        self.uc_index = 0
        self.index_dict = {
            "Chrome": 0,
            "UC": 0,
            'Android': 0,
            'iPhone': 0,
            'XiaoMi': 0

        }

    def random_chrome(self):
        return random.choice(self.list_user_agent['Chrome'])

    def random_uc(self):
        return random.choice(self.list_user_agent['UC'])

    def random_android(self):
        return random.choice(self.list_user_agent['Android'])

    def random_iphone(self):
        return random.choice(self.list_user_agent['iPhone'])

    def random_xiaomi(self):
        return random.choice(self.list_user_agent['XiaoMi'])

    def order_chrome(self):
        return self.order_index_ua('Chrome')

    def order_uc(self):
        return self.order_index_ua('UC')

    def order_android(self):
        return self.order_index_ua('Android')

    def order_iphone(self):
        return self.order_index_ua('iPhone')

    def order_xiaomi(self):
        return self.order_index_ua('XiaoMi')

    def order_index_ua(self, index_name):
        if self.index_dict[index_name] < len(self.list_user_agent[index_name]) - 1:
            self.index_dict[index_name] += 1
        else:
            self.index_dict[index_name] = 0

        return self.list_user_agent[index_name][self.index_dict[index_name]]
