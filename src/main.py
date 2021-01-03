import time
import threading

from raspi_music_generator.controllers import RGBLedController

class Main():

    def __init__(self):
        self.rgb_led = RGBLedController()
    
    def start(self):
        self.rgb_led.start_rgb_led_thread()
    


if __name__ == "__main__":
    main = Main()
    main.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")