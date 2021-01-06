import time
import threading

from raspi_music_generator.controllers import RGBLedController
from raspi_music_generator.controllers.music_generator import MusicGenerator

class Main():

    def __init__(self):
        self.rgb_led = RGBLedController()
        self.music_generator = MusicGenerator(self.rgb_led)
    
    def start(self):
        self.rgb_led.start_rgb_led_thread()
        self.music_generator.start_button_listener()
    
    def stop(self):
        self.rgb_led.stop()


if __name__ == "__main__":
    main = Main()
    main.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")
        main.stop()