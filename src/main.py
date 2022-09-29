import rumps
import time
from user_info import CaffeineLevels
from dateutil.parser import parse

class CaffeineTracker(rumps.App):
    def __init__(self):
        super().__init__(
            name="CaffeineTracker", 
            title="150", 
            icon="../assets/coffee.png",
            menu=(
                'Drink Celsius',
                'Drink Yerb',
                'Add Caffeine',
                'Refresh Tracker',
                'Reset Tracker'
            )
        )
        self.configure_windows()
        self.tracker = CaffeineLevels()
        self.title = "test"
        self.timer = rumps.Timer(self.update_caffeine_level, 60)
        self.update_caffeine_level()
    
    def run(self):
        super().run()

    def configure_windows(self):
        try:
            self.add_caffeine_window = rumps.Window(
                message="Enter the amount of caffeine consumed. (mg)",
                title="Add Caffeine",
                ok="Add Now",
                cancel=True,
                dimensions=(320, 100)
            )
            self.add_caffeine_window.add_button("Set Time")
            self.add_caffeine_window.icon = "../assets/coffee-dark.png"

            self.set_time_window = rumps.Window(
                message="Enter the time you consumed the caffeine. (hh:mm:ss)",
                title="Add Caffeine",
                ok="Add",
                cancel=True,
                dimensions=(320, 100)
            )
        except Exception as e:
            print(e)

    @rumps.timer(60)
    def update_caffeine_level(self, sender=None):
        self.tracker.update_levels()
        self.title = str(round(self.tracker.caffeine_level)) + " mg"

    @rumps.clicked('Drink Celsius')
    def drink_celcius(self, sender):
        self.tracker.add_caffeine(200)

        self.update_caffeine_level()

    
    @rumps.clicked('Drink Yerb')
    def drink_yerb(self, sender):
        self.tracker.add_caffeine(150)

        self.update_caffeine_level()


    @rumps.clicked('Add Caffeine')
    def add_caffeine(self, sender):
        response = self.add_caffeine_window.run()
        if response.clicked == 1:
            while not response.text.isnumeric():
                response = self.add_caffeine_window.run()
                if response.clicked == 0:
                    return
            self.tracker.add_caffeine(float(response.text))
        elif response.clicked == 2:
            time_response = self.set_time_window.run()
            self.tracker.add_adjusted_caffeine(float(response.text), parse(time_response.text))
        else:
            return

        self.update_caffeine_level()


    @rumps.clicked('Refresh Tracker')
    def refresh_tracker(self, sender):
        self.update_caffeine_level()
        

    @rumps.clicked('Reset Tracker')
    def reset_tracker(self, sender):
        self.tracker.user_info = {}
        self.tracker.last_updated = time.time()
        self.tracker.caffeine_level = 0

        self.update_caffeine_level()

if __name__ == "__main__":
    app = CaffeineTracker()
    app.run()
    app.timer.start()
