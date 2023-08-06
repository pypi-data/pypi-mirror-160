from datetime import datetime

class Time:

    def display_count(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time is :", current_time)

Time().display_count()





