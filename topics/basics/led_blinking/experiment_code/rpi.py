import time


class Experiment:
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        counter = 0
        while self.is_running:
            counter+=1
            self.value_for_ui.emit(f"counter={counter}")
            time.sleep(.2)

    def stop(self):
        self.is_running = False