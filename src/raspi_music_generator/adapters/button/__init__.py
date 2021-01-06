import RPi.GPIO as GPIO

from raspi_music_generator.settings import ButtonSettings

class Button():
    def __init__(self):
        self.button_pin = ButtonSettings.pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_button(self):
        return GPIO.input(self.button_pin)