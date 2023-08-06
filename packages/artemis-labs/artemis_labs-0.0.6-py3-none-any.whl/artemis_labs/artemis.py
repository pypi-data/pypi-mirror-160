from artemis_labs.artemis_socket import artemis_socket 
import json 
from time import sleep
import base64
import os

class artemis:
    
    APP_PATH = "app.json"

    def __init__(self):
        self.callbackMap = {}
        self.artemis_socket = artemis_socket(self.callback_handler)
        try:
            with open(self.APP_PATH, "r") as f:
                self.app = json.load(f)
        except Exception as e:
            print(e)
            print('[Artemis] Exception: Unable to load app.json')
            self.app = {}       
        self.run() 

    # Callback handler
    def callback_handler(self, message):
        if message != 'ping':
            message = json.loads(message)
            callbackTag = message["type"] + "-" + message["attribute"] + "-" + message["name"]
            if callbackTag in self.callbackMap:
                self.callbackMap[callbackTag](json.loads(message["state"]))
            else:
                print('Callback not found: ', message)

    # Check if connected
    def isConnected(self):
        return self.artemis_socket.isConnected()

    # Enqueue callback to receive message when message received
    def on(self, action, name, callback):
        onPacket = {}
        onPacket["type"] = "callback"
        onPacket["attribute"] = action
        onPacket["name"] = name
        callbackTag = onPacket["type"] + "-" + onPacket["attribute"] + "-" + onPacket["name"]
        self.callbackMap[callbackTag] = callback
        self.artemis_socket.send(json.dumps(onPacket))

    # Send update message
    def update(self, elementName, newValue):
        updatePacket = {}
        updatePacket["type"] = "update"
        updatePacket['name'] = elementName
        updatePacket['value'] = newValue
        self.artemis_socket.send(json.dumps(updatePacket))

    # Enqueue callback
    def setCallback(self, callback):
        self.artemis_socket.enqueueCallback(callback)

    # Launch server
    def run(self):
        self.artemis_socket.run()

        if os.name == 'nt':
            os.system("start chrome https://artemisardesignerdev.com/launcher_local.html")
        else:
            print('[Artemis] Please open Chrome and navigate to https://artemisardesignerdev.com/launcher_local.html')

        while not self.artemis_socket.isConnected():
            sleep(0.1)
        init_packet = { 'type' : 'init', 'state' : json.dumps(self.app) }
        self.artemis_socket.send(json.dumps(init_packet))

    # Helpers
    def load_image(path):
        try:
            with open(path, "rb") as image_file:
                b64Encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64Encoding
        except Exception as e:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(e))
    
    def load_gif(path):
        try:
            with open(path, "rb") as image_file:
                b64Encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64Encoding
        except Exception as e:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(e))