import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID = ""
AIO_USERNAME = "namelessbtw"
AIO_KEY = "aio_QMsK29fJHPQvTTmWofsI26snFeSA"

def  connected(client):
    print("Service connected")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribed")

def  disconnected(client):
    print("Disconnected!!!")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Data received " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    // ladtitude here.
    ladtitude = random.randint(30, 60)    //range -90, 90 ladtitude
    print("Update humidity:", ladtitude) // change ladtitude
    client.publish("humidity", ladtitude)       // -180, 180 update longtitude, set the range a bit further.
    
    // longtitude here.
    longtitude = random.randint(0, 50)
    print("Update temperature:", longtitude)
    client.publish("temperature",longtitude)
    time.sleep(10)
