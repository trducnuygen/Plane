
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID = ""
AIO_USERNAME = "namelessbtw"
AIO_KEY = "aio_vaWy263KkFsF4qNlNIYSXOZngSWl"

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

speed_last = 0
altitude_last = 0

# vector_dict = {'up': 1, 'down': 0}
vector = 'up'

cruise_speed = 780
cruise_altitude = 12000

taking_off_alt = range(10, 2000)
mid_stage_up = range(4000, 12000)
mid_stage_down = range(3000, 12000)
landing_alt = range(10, 3000)

count = 0

# city list
list_city = {
    1: "New York",
    2: "Los Angeles",
    3: "Chicago",
    4: "Houston",
    5: "Philadelphia",
    6: "San Diego",
    7: "Dallas",
    8: "Indianapolis",
    9: "San Francisco",
    10: "Austin",
    11: "Columbus",
    12: "Charlotte",
    13: "Detroit",
    14: "Seattle",
    15: "Boston"
}

while True:
    # latitude
    latitude = random.randint(-90, 90)
    print("Update latitude: {}°".format(latitude))
    client.publish("latitude", latitude)

    #longitude
    longitude = random.randint(-180, 179)
    print("Update longitude: {}°".format(longitude))
    client.publish("temperature",longitude)


    # speed & altitude condition.
    speed = 0
    altitude = 0

    # when cruising and  wanna land.
    if speed == cruise_speed and count == 5:
        speed = speed - random.randint(25, 50)
        vector = 'down'
        count = 0
        altitude = altitude - random.randint(385, 770)

    # when on land.
    elif speed == 0 and vector == 'down':
        speed = speed + random.randint(10, 25)
        vector = 'up'
        altitude = altitude + 2
    
    elif speed == 0 and vector == 'up':
        speed = speed + random.randint(10, 25)
        altitude = altitude + 2

    # taking off stage
    elif altitude in taking_off_alt and speed >= 200 and speed <= 400:
        speed = speed + random.randint(20, 50)
        altitude = altitude + random.randint(450, 770)
    
    # stage 2 of flying
    elif altitude in mid_stage_up and speed > 400 and speed <= cruise_speed - 75:
        speed = speed + random.randint(30, 75)
        altitude = altitude + random.randint(462, 1154)

    # cruise time, rmb to set alt to cruise alt.
    elif altitude in mid_stage_up and speed > cruise_speed - 75:
        speed = cruise_speed
        count += 1
        altitude = cruise_altitude
    
    # still cruising.
    elif speed == cruise_speed and count < 5:
        speed = cruise_speed
        count += 1

    # will now be conducting operation landing.
    elif altitude in mid_stage_down and speed >= 400 and speed <= cruise_speed - 20:
        speed = speed - random.randint(30, 75)
        altitude = altitude - random.randint(462, 1154)
    
    # about to land and at alt around 500m. --> gonna update the altitude here maybe.
    elif altitude in landing_alt and speed >= 200 and speed < 400:
        speed = speed - random.randint(20, 50)
        altitude = random.choice(range(200, 500))

    # gonna land.
    elif altitude in landing_alt and speed < 200:
        altitude = 0
        speed = random.randint(10, 180)

    # on land and wanna fly up
    elif altitude_last == 0 and speed_last in range(10, 180) and vector == 'up':
        altitude = altitude + random.randint(10, 200)
        speed = 200

    # update speed
    print("Update speed:", min([speed, 780]))
    client.publish("speed", min([speed, 780]))
    speed_last = speed

    # update altitude
    print("Update altitude:", min([altitude, 12000]))
    client.publish("altitude", min([altitude, 12000]))
    altitude_last = altitude
    
    
    # end.
    time.sleep(10)

