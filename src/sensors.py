from machine import Pin, ADC, time_pulse_us, SPI
import dht
import math
import time
import mfrc522

class Analog:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

    def voltage(self):
        return (self.read() / 4055) * 3.3

    def read(self):
        return self.adc.read()

class LDR(Analog):
    def calc(self):
        return (1 - (self.voltage() / 3.3)) * 100

class MQ2(Analog):
    def calc(self):
        return (self.voltage() / 3.3) * 100

class DHT22:
    def __init__(self, pin):
        self.dht = dht.DHT22(Pin(pin))

    def measure(self):
        self.dht.measure()

    def temperature(self):
        return self.dht.temperature()

    def humidity(self):
        return self.dht.humidity()

    def calc(self):
        self.measure()
        return (self.temperature(), self.humidity())

class Thermostat(Analog):
    def calc(self):
        BETA = 3950
        analogValue = self.adc.read()

        # Calculo baseado na documentação do sensor de temperatura 
        # https://docs.wokwi.com/parts/wokwi-ntc-temperature-sensor
        celsius = (1 / (math.log(1 / (4095 / analogValue - 1)) / BETA + 1.0 / 298.15) - 273.15)
        return celsius

class Ultrassonic:
    def __init__(self, echo, trig):
        self.echo = Pin(echo, Pin.IN)
        self.trig = Pin(trig, Pin.OUT)
    
    def measure(self):
        self.trig.value(0)

        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        duration = time_pulse_us(self.echo, 1)
        return duration / 58

class PIR:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)

    def hasMovement(self):
        return self.pin.value()

class MFRC522:
    def __init__(self):
        self.spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
        self.spi.init()
        self.rfid = mfrc522.MFRC522(spi=self.spi, gpioRst=4, gpioCs=5)

    def read(self): 
        stat, _ = self.rfid.request(self.rfid.REQIDL)

        if stat == self.rfid.OK:
            stat, raw_uid = self.rfid.anticoll()
            if stat == 2:      
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                return card_id
        return ""

class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)

    def read(self):
        return self.pin.value()

    def setIrq(self, function):
        self.pin.irq(
            trigger = Pin.IRQ_RISING,
            handler = lambda pin: function()
        )