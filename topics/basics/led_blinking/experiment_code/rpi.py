import time


class Experiment:
    FREQUENCY=2
    def __init__(self, is_running, value_for_ui):
        self.is_running = is_running
        self.value_for_ui = value_for_ui

    def run(self):
        counter = 0
        while self.is_running:
            counter+=1
            self.value_for_ui.emit(f"counter={counter}")
            time.sleep(1/self.FREQUENCY)

    def stop(self):
        self.is_running = False