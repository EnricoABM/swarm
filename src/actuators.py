from machine import Pin
from time import sleep_us

class Motor:
    def __init__(self, direc, step):
        self.direc = Pin(direc, Pin.OUT)
        self.step = Pin(step, Pin.OUT)

    def move(self, direc, steps, delay):
        self.direc.value(direc)
        steps = abs(steps)
    
        for i in range(steps):
            self.step.value(1)
            sleep_us(delay)
            self.step.value(0)
            sleep_us(delay)

class Actuator:
    def __init__(self, pin, name):
        self.pin = Pin(pin, Pin.OUT)
        self.name = name

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def toggle(self):
        self.pin.value(
            not self.pin.value()
        )

    def value(self):
        return self.pin.value()
