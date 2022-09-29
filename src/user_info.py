import json
import time
import datetime
import rumps

CAFFEINE_HALF_LIFE = 18000

class CaffeineLevels:
    user_info: dict
    last_updated: float
    caffeine_level: float

    def __init__(self):
        try:
            with open("/Users/henrypigg/Documents/Coding/CaffeineTracker/build_tools/user_info.json", "r") as file:
                self.user_info = json.loads(file.read())
                self.load_user_info(self.user_info)
        except OSError:
            self.user_info = {}
            self.last_updated = time.time()
            self.caffeine_level = 0

    def load_user_info(self, user_info):
        self.last_updated = float(user_info['LastUpdated'])
        self.caffeine_level = float(user_info['CaffeineLevels'])

    def update_user_info(self):
        self.user_info['LastUpdated'] = '{:.6f}'.format(round(self.last_updated, 6))
        self.user_info['CaffeineLevels'] = '{:.2f}'.format(round(self.caffeine_level, 2))

        try:
            with open("/Users/henrypigg/Documents/Coding/CaffeineTracker/build_tools/user_info.json", "w") as file:
                json.dump(self.user_info, file)
        except Exception as e:
            print(e)

    def update_levels(self):
        cur_time = time.time()
        new_caffeine_level = self.caffeine_level * (1 / 2) ** ((cur_time - self.last_updated) / CAFFEINE_HALF_LIFE)
        self.last_updated = cur_time
        self.caffeine_level = new_caffeine_level

        self.update_user_info()
            
    def add_caffeine(self, amount):
        self.caffeine_level += amount

    def add_adjusted_caffeine(self, amount, time_response):
        cur_time = datetime.datetime.now().timestamp()
        time_consumed = datetime.datetime(
            time_response.year,
            time_response.month,
            time_response.day,
            time_response.hour,
            time_response.minute,
            time_response.second
        ).timestamp()
        print(time_response)

        print(time_consumed, cur_time)
        adjusted_amount = amount * (1 / 2) ** ((cur_time - time_consumed) / CAFFEINE_HALF_LIFE)
        self.caffeine_level += adjusted_amount