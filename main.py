# ========= OLED =========
# 21 - SDA OLED
# 16 - SCL OLED

# ========= FOGÃO =========
# 34 - Termostato - ADC
# 35 - Ponteciometro - ADC
# 17 - Valvula Solenoide

# ========= JANELA =========
# 32 - TRIGGER - DIG
# 15 - ECHO - DIG
# 26 - STEP
# 22 - DIR
# 27 - BTN

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


from sensors import Thermostat, Ultrassonic, PIR, MFRC522, Button, Analog
from actuators import Motor, Actuator
from display import Display, Page
from time import sleep, ticks_diff, ticks_ms

# Sensores
tempSensor = Thermostat(34)
ultrassonic = Ultrassonic(trig = 32, echo = 15)
pir = PIR(33)
rfid = MFRC522()
lock_btn = Button(25)
window_btn = Button(27)
pot = Analog(35)

# Atuadores
motor = Motor(direc = 22, step = 26)
valv = Actuator(pin = 17, name = "Válvula Solenoide")
lock = Actuator(pin = 14, name = "Fechadura")
buzzer = Actuator(pin = 12, name = "Buzzer")
led = Actuator(pin = 13, name = "LED de Alarme")

# Logica
# Alarme
alarmMode = True
alarmTrig = False
def alarmLogic():
    if alarmMode == False:
        led.off()
        buzzer.off()
        alarmTrig = False
        return
    
    led.on()

    if (pir.hasMovement()):
        buzzer.toggle()
        alarmTrig = True
        
# Fechadura
cards = [
    "0x01030400",
    "0x11334400"
]

def lockLogic():
    card_id = rfid.read()

    if card_id in cards:
        lock.off()

    if lock_btn.read() == 1:
        lock.on()

# Janela
windowState = "closed"
def windowLogic():
    
    global windowState

    if windowState == "opened":
        if ultrassonic.measure() <= 95:
            motor.move(1, 10, 2000)

    elif windowState == "closed":
        if ultrassonic.measure() >= 5:
            motor.move(0, 10, 2000)

def toggleWindowState():
    global windowState

    if windowState == "opened":
        windowState = "closed"
    elif windowState == "closed":
        windowState = "opened"

# Fogão
startTemp = 0
timeout = 4_000
startTime = 0
timeStarted = False
timeoutState = False
def cook():
    global startTime
    global timeStarted
    global startTemp
    global timeoutState 

    if pot.voltage() >= 1 and not timeStarted and not timeoutState:
        startTime = ticks_ms()
        timeStarted = True
        startTemp = tempSensor.calc() 


    if pot.voltage() <= 0.3:
        valv.off()
        timeoutState = False
        timeStarted = False

    if timeStarted:
        tempChange = tempSensor.calc() - startTemp 


        if tempChange >= 20:
            valv.off()
            return 

        timeDiff = ticks_diff(ticks_ms(), startTime)

        if timeDiff >= timeout:
            valv.on()
            timeStarted = False
            timeoutState = True
            return
     


# Exibição 
oled = Display(sda = 21, scl = 16)

lock.on()
window_btn.setIrq(toggleWindowState)
print("Iniciando...")
while True:
    
    alarmLogic()
    lockLogic()
    windowLogic()
    cook()