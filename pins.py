from collections import OrderedDict
from machine import Pin, ADC, I2C, PWM
from mcp9808 import MCP9808

class pin:
    def __init__(self, index: int, type: string, adc: bool = False, pwm: bool = False, pwm_invert: bool = False):
        self.pin = Pin(index)
        self.type = type
        self.adc = adc
        self.pwm = pwm
        self.pwm_invert = pwm_invert
        self.name = f"Pin {index}"
        if adc:
            self.pin = ADC(self.pin, atten = ADC.ATTN_11DB)
            self.pin.width(ADC.WIDTH_12BIT)
        if pwm:
            self.pin = PWM(self.pin, freq=200)
            self.pin.duty(0 if not pwm_invert else 1023)
    def value(self):
        if self.adc:
            return self.pin.read()/4095
        if self.pwm:
            return (self.pin.duty() if not self.pwm_invert else 1023-self.pin.duty())/1023
        return self.pin.value()
    def set(self, value):
        if self.pwm:
            duty = int((value if not self.pwm_invert else 1-value)*1023)
            self.pin.duty(duty)
        elif self.adc:
            raise ValueError("Cannot set value for ADC pin")
        else:
            self.pin.value(value)

pins = OrderedDict([
    ('Button'        , pin(4, 'button')),
    ('Potentiometer' , pin(36, 'input', adc = True)),
    ('LED-Green'     , pin(32, 'led', pwm = True)),
    ('LED-Orange'    , pin(15, 'led', pwm = True)),
    ('LED-Red'       , pin(33, 'led', pwm = True)),
    ('RGB-Red'       , pin(13, 'led', pwm = True, pwm_invert = True)),
    ('RGB-Green'     , pin(12, 'led', pwm = True, pwm_invert = True)),
    ('RGB-Blue'      , pin(22, 'led', pwm = True, pwm_invert = True)),
    ('Thermometer'   , MCP9808(I2C(0, scl=Pin(22), sda=Pin(23))))])
