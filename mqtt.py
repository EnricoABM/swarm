import network
import time
from umqtt.simple import MQTTClient

class Wifi:    
    def __init__(self):
        self.sta_if = None

    def connect(self):       
        # Comando de Conexão retirado do exemplo MQTT
        print("Connecting to WiFi", end="")

        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect('Wokwi-GUEST', '')

        while not self.sta_if.isconnected():
            # TODO Verificação de Erro
            print(".", end="")
            time.sleep(0.1)
        print(" Connected!")

    def is_connected(self):
        if (self.sta_if == None):
            return False
        return self.sta_if.is_connected()

class MQTT:
    def __init__(self, client_id, broker, user, password, wifi):
        self.client_id = client_id
        self.broker = broker
        self.user = user
        self.password = password
        self.client = None
        self.prev_message = ""
        self.wifi = wifi
    
    def reconnect(self):
        # TODO: Reconectar com MQTT
        ...

    def is_connected(self):
        # TODO: Adicionar forma de verificação de conexão
        ...

    def connect(self):
        self.wifi.connect()
        print(f"Broker: {self.broker}")
        print("Connecting to MQTT server... ", end="")
        self.client = MQTTClient(
            client_id=self.client_id, 
            server=self.broker, 
            port=8883,               
            user=self.user, 
            password=self.password,
            ssl=True,
            ssl_params={'server_hostname': self.broker} 
        )
        self.client.connect()
        print("Connected!")
    
    def publish(self, topic, message):
        # Guard Clause para evitar envio de mensagem sem client
        if (self.client == None):
            return
        
        # Verifica se houve alteração na mensagem enviada
        # Evita envio desnecessário
        if (message != self.prev_message):
            print(f"Send MQTT Topic: {topic}")
            print(f"Message: {message}")
            self.client.publish(topic, message)
            self.prev_message = message
        else:
            print("Sem alterações")