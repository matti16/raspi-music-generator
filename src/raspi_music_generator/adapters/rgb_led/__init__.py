import RPi.GPIO as GPIO

from raspi_music_generator.adapters.drivers.adc_device import ADS7830
from raspi_music_generator.settings import RGBLedSettings


class RGBLed():
    def __init__(self):
        self.adc = ADS7830()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(RGBLedSettings.R_pin, GPIO.OUT)      # set RGBLED pins to OUTPUT mode
        GPIO.setup(RGBLedSettings.G_pin, GPIO.OUT)
        GPIO.setup(RGBLedSettings.B_pin, GPIO.OUT)
    
        self.p_Red = GPIO.PWM(RGBLedSettings.R_pin, 1000)    # configure PMW for RGBLED pins, set PWM Frequence to 1kHz
        self.p_Red.start(0)
        self.p_Green = GPIO.PWM(RGBLedSettings.G_pin, 1000)
        self.p_Green.start(0)
        self.p_Blue = GPIO.PWM(RGBLedSettings.B_pin, 1000)
        self.p_Blue.start(0)
    

    def update_color(self): 
        value_Red = self.adc.analogRead(RGBLedSettings.adc_R)       # read ADC value of 3 potentiometers
        value_Green = self.adc.analogRead(RGBLedSettings.adc_G)
        value_Blue = self.adc.analogRead(RGBLedSettings.adc_B)

        self.p_Red.ChangeDutyCycle(value_Red*100/255)  # map the read value of potentiometers into PWM value and output it 
        self.p_Green.ChangeDutyCycle(value_Green*100/255)
        self.p_Blue.ChangeDutyCycle(value_Blue*100/255)


    def destroy(self):
        self.adc.close()
        self.p_Red.stop()  # stop PWM
        self.p_Green.stop()  # stop PWM
        self.p_Blue.stop()  # stop PWM
        GPIO.cleanup()
    