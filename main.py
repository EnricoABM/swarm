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
from mqtt import Wifi, MQTT
import urequests
import ujson

# Alarme

pir = PIR(33)
buzzer = Actuator(pin = 12, name = "Buzzer")
led = Actuator(pin = 13, name = "LED de Alarme")

alarmMode = True
alarmTrig = False
alarmEmailSend = False
def alarmLogic():
    global alarmEmailSend

    if alarmMode == False:
        led.off()
        buzzer.off()
        alarmTrig = False
        return
    
    led.on()

    if (pir.hasMovement()):
        buzzer.toggle()
        alarmTrig = True
        if not alarmEmailSend:
            sendAlarmTrig()
            alarmEmailSend = True
    else:
        alarmTrig = False
        alarmEmailSend = False

# Fechadura

rfid = MFRC522()
lock_btn = Button(25)
lock = Actuator(pin = 14, name = "Fechadura")

cards = [
    "0x01030400",
    "0x11334400"
]
doorSendEmail = False
def lockLogic():
    global doorSendEmail
    card_id = rfid.read()

    if card_id in cards:
        lock.off()
        if not doorSendEmail:
            sendOpenDoor()
            doorSendEmail = True

    if lock_btn.read() == 1:
        lock.on()
        doorSendEmail = False
        

# Janela

ultrassonic = Ultrassonic(trig = 32, echo = 15)
window_btn = Button(27)
motor = Motor(direc = 22, step = 26)

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
tempSensor = Thermostat(34)
pot = Analog(35)
valv = Actuator(pin = 17, name = "Válvula Solenoide")

startTemp = 0
timeout = 4_000
startTime = 0
timeStarted = False
timeoutState = False
timeDiff = 0
def cook():
    global startTime
    global timeStarted
    global startTemp
    global timeoutState
    global timeDiff 

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
            startTime = ticks_ms()
            return 

        timeDiff = ticks_diff(ticks_ms(), startTime)

        if timeDiff >= timeout:
            valv.on()
            timeStarted = False
            timeoutState = True
            return
     

# Exibição 
oled = Display(sda = 21, scl = 16)

# Google Sheets
URL = "https://script.google.com/macros/s/AKfycbww3km1fySzPCaALdb9hLWHnaIJb-5eO_1l3G3H1ndMunG0QtZ1-FWeGBWk8tIPSLuJ/exec"

def sendAlarmTrig():
    try:
        alarmData = {"Alarme": "ACIONADO"}
        resposta = urequests.post(URL, json=alarmData)
        print("Enviado;", alarmData, "| Resposta:", resposta.text)
        resposta.close()
    except Exception as e:
        print("Erro ao enviar:", e)

def sendOpenDoor():
    try:
        lockData = {"Fechadura": "ABERTA"}
        resposta = urequests.post(URL, json=lockData)
        print("Enviado;", lockData, "| Resposta:", resposta.text)
        resposta.close()
    except Exception as e:
        print("Erro ao enviar:", e)


#MQTT
wifi = Wifi()

mqtt = MQTT(
    client_id = "esp32", 
    broker = "bf2c85f1ce9144188a440df97e370c23.s1.eu.hivemq.cloud",
    user = "hivemq.webclient.1776723263165", 
    password = "60cN%d>Y;M4oQzL5h&Vn", 
    wifi = wifi
)

mqtt.connect()

mqttData = {}

lock.on()
window_btn.setIrq(toggleWindowState)
print("Iniciando...")
while True:

    mqttData['alarmMode'] = alarmMode
    mqttData['alarmTrig'] = alarmTrig
    mqttData['lockMode'] = lock.value()
    mqttData['windowState'] = windowState
    mqttData['valv'] = valv.value()
    mqttData['timeDiff'] = timeDiff
    mqttData['timeoutState'] = timeoutState
    mqttData['timeStarted'] = timeStarted
    
    alarmLogic()
    lockLogic()
    windowLogic()
    cook()

    mqtt.publish("data", ujson.dumps(mqttData))
