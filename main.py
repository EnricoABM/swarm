# ========= OLED =========
#  - SDA OLED
#  - SCL OLED

# ========= FOGÃO =========
# 34 - Termostato - ADC
#  - Valvula Solenoide

# ========= JANELA =========
# 32 - TRIGGER - DIG
# 35 - ECHO - DIG
#  - STEP
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
from time import sleep

temp_sensor = Thermostat(34)
ultrassonic = Ultrassonic(trig = 32, echo = 35)
pir = PIR(33)
rfid = MFRC522()
btn = Button(25)

print("Iniciado...")
while True:
    # print(f"Temperatura: {temp_sensor.calc()}")
    # print(f"Distância: {ultrassonic.measure()} cm")
    # print(f"Presença: {'Tem movimento.' if pir.hasMovement() else 'Sem movimento'}")
    # print("card: " + rfid.read())
    print("botão: " + str(btn.read()))  
    sleep(1)
