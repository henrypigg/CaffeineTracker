import rumps
import time
from user_info import CaffeineLevels

class CaffeineTracker(rumps.App):
    def __init__(self):
        super().__init__(
            name="CaffeineTracker", 
            title="150", 
            icon="../assets/coffee.png",
            menu=(
                'Add Caffeine',
                'Reset Tracker'
            )
        )
        self.add_caffeine_window = rumps.Window(
            message="Enter the amount of caffeine consumed. (mg)",
            title="Add Caffeine",
            ok="Add",
            cancel=True,
            dimensions=(320, 260)
        )
        self.add_caffeine_window.icon = "../assets/coffee-dark.png"
        self.tracker = CaffeineLevels()
        self.title = "test"
        self.timer = rumps.Timer(self.update_caffeine_level, 60)
        self.update_caffeine_level()
    
    def run(self):
        super().run()

    @rumps.timer(60)
    def update_caffeine_level(self, sender=None):
        self.tracker.update_levels()
        self.title = str(round(self.tracker.caffeine_level)) + " mg"

    @rumps.clicked('Add Caffeine')
    def add_caffeine(self, sender):
        response = self.add_caffeine_window.run()
        if response.clicked == 1:
            while not response.text.isnumeric():
                response = self.add_caffeine_window.run()
                if response.clicked == 0:
                    return
        else:
            return

        print(response.text)

        self.tracker.add_caffeine(float(response.text))

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
