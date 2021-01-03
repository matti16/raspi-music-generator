import threading
import time

from raspi_music_generator.adapters.rgb_led import RGBLed

class RGBLedController():
    def __init__(self):
        self.rgb_led = RGBLed()

    def _rgb_loop(self):
        while True:
            self.rgb_led.update_color()
            time.sleep(0.01)

    def start_rgb_led_thread(self):
        self.rgb_led_thread = threading.Thread(target=self._rgb_loop)
        self.rgb_led_thread.start()
    
    def stop(self):
        self.rgb_led.destroy()
