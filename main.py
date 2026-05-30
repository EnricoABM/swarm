# ========= OLED =========
# 21 - SDA OLED
# 16 - SCL OLED

# ========= FOGÃO =========
# 34 - Termostato - ADC
# 17 - Valvula Solenoide

# ========= JANELA =========
# 32 - TRIGGER - DIG
# 35 - ECHO - DIG
# 26 - STEP
# 22 - DIR

# ========= FECHADURA =========
# 25 - Botão

# 23 - MOSI
# 19 - MISO
# 18 - SCK
# 5 - SDA
# 4 - RST

# ========= ALARME =========
# 33 - MOTION - DIG
# 12 - BUZZER
# 13 - ALARME LED MODE
# 14 - Fechadura


from sensors import Thermostat, Ultrassonic, PIR, MFRC522, Button
from actuators import Motor, Actuator
from display import Display
from time import sleep

temp_sensor = Thermostat(34)
ultrassonic = Ultrassonic(trig = 32, echo = 35)
pir = PIR(33)
rfid = MFRC522()
btn = Button(25)

motor = Motor(direc = 22, step = 26)

valv = Actuator(pin = 17, name = "Válvula Solenoide")
lock = Actuator(pin = 14, name = "Fechadura")
buzzer = Actuator(pin = 12, name = "Buzzer")
led = Actuator(pin = 13, name = "LED de Alarme")

oled = Display(sda = 21, scl = 16)

print("Iniciando...")
while True:
    print(f"Temperatura: {temp_sensor.calc()}")
    print(f"Distância: {ultrassonic.measure()} cm")
    print(f"Presença: {'Tem movimento.' if pir.hasMovement() else 'Sem movimento'}")
    print("card: " + rfid.read())
    print("botão: " + str(btn.read()))

    motor.move(1, 200, 2000)


    valv.toggle()
    lock.toggle()
    led.toggle()
    buzzer.toggle()
      
    oled.show("")

    sleep(1)
