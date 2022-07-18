from random import randint, choice
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

# vector takes 2 values: up and down.
vector = 'up'

# cruising value
cruise_speed = 780
cruise_altitude = 12000

# range for speed
hover_speed = range(200, 400)
mid_stage_up_speed = range(400, cruise_speed - 75)
mid_stage_down_speed = range(400, cruise_speed - 20)

# range for altitude
taking_off_alt = range(2, 4000)
mid_stage_up = range(4000, 12000)
mid_stage_down = range(3000, 12000)
landing_alt = range(310, 3000)

# define counts
count = 0
count_rep = 0
count_stop = 0


# define vars for checking errors.
speed_last = 0
altitude_last = 0

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
    latitude = randint(25, 50)
    print("Update latitude: {}°".format(latitude))
    client.publish("latitude", latitude)

    #longitude
    longitude = randint(66, 126)
    print("Update longitude: {}°".format(longitude))
    client.publish("temperature",longitude)

    # speed & altitude condition.
    speed = speed_last
    altitude = altitude_last

    # when cruising and  wanna land.
    if speed == cruise_speed and count == 5 and vector == 'up':
        speed = speed - random.randint(25, 50)

        vector = 'down'
        count = 0
        altitude = altitude - randint(385, 770)

    # when on land.
    elif speed == 0 and vector == 'down' and altitude == 0:
        speed = speed + random.randint(10, 25)

        vector = 'up'
        altitude = altitude + 2
    
    # start the flight
    elif speed == 0 and vector == 'up':
        speed = speed + randint(10, 25)
        altitude = altitude + 2

    # accelerating
    elif speed > 0 and speed < 200 and vector == 'up':
        speed = speed + random.randint(10, 25)
        
    # taking off stag
    elif altitude in taking_off_alt and speed in hover_speed and vector == 'up':
        speed = speed + random.randint(20, 35)
        altitude = altitude + random.randint(500, 700)
    
    # stage 2 of flying
    elif altitude in mid_stage_up and speed in mid_stage_up_speed and vector == 'up':
        speed = speed + random.randint(40, 75)
        altitude = altitude + random.randint(662, 1654)

    # almost cruise time, gonna increase altitude.
    elif altitude in mid_stage_up and speed > cruise_speed - 75 and vector == 'up':
        altitude = altitude + random.randint(500, 1500)
        speed = speed + random.randint(1, 3)
        
    # increase altitude
    elif altitude < cruise_altitude - 1700 and altitude > 10000 and vector == 'up':
        altitude = cruise_altitude
        speed = cruise_speed
    
    # adjust speed for cruising
    elif altitude == cruise_altitude and speed != cruise_speed and vector == 'up':
        speed = cruise_speed
    
    # still cruising.
    elif speed == cruise_speed and altitude == cruise_altitude and count <= 5:
        speed = cruise_speed
        count += 1

    # will now be conducting operation landing.
    elif altitude in mid_stage_down and speed in mid_stage_down_speed and vector == 'down':
        speed = speed - random.randint(30, 75)
        altitude = altitude - random.randint(962, 1554)
    
    # about to land and at alt around 500m. --> gonna update the altitude here maybe.
    elif altitude in landing_alt and speed in hover_speed and vector == 'down':
        speed = speed - random.randint(20, 50)
        altitude = random.choice(range(200, 1000))

    # gonna land.
    elif altitude in landing_alt and vector == 'down':
        altitude = altitude - random.randint(50, 150)
    
    # decelerate when landing on land
    elif altitude > 150 and altitude < 310 and speed < 200 and speed >= 30 and vector == 'down':
        speed = speed - random.randint(10, 25)
        altitude = 0
        
    # further decelerate on land.
    elif altitude == 0 and speed < 200 and speed >= 30 and vector == 'down':
        speed = speed - random.randint(10, 25)
    
    # stop
    elif altitude == 0 and speed < 30 and vector == 'down':
        speed = 0
        count_stop = count_stop + 1
    
    # stop for fueling
    elif altitude == 0 and speed == 0 and count_stop < 5:
        count_stop += 1
    
    # on land and wanna fly up
    elif altitude_last == 0 and speed_last in range(10, 180) and vector == 'up':
        altitude = altitude + randint(10, 200)
        speed = 200

    
    # for situation where it got bugged and repeat for ever.
    if speed_last == speed and altitude_last == altitude and speed != cruise_speed and altitude != cruise_altitude:
        count_rep += 1
        if count_rep == 3:
            # situation 1: speed too high when not in altitude for stage 2.
            if speed in mid_stage_up_speed and altitude in taking_off_alt and vector == 'up':
                altitude = altitude + random.randint(250, 500)
            
            # situation 2: speed too low when in altitude for stage 2.
            if speed in hover_speed and altitude in mid_stage_up and vector == 'up':
                speed = speed + random.randint(20, 40)
                
            # situation 3: speed too low (speed in hover) when not in altitude for stage 5 (alt for hover).
            if speed in hover_speed and altitude in mid_stage_down and vector == 'down':
                altitude = altitude - random.randint(200, 350)
                
            # situation 4: speed too high (not in hover) when in altitude for stage 5.
            if speed in mid_stage_down_speed and altitude in landing_alt and vector == 'down':
                speed = speed - random.randint(20, 40)
            
            # situation 5: speed too high (in hover) when in altitude for actual landing:
            if speed in hover_speed and altitude < 310 and vector == 'down':
                speed = speed - random.randint(20, 40)
            
            # reset count
            count_rep = 0
            
    # update speed
    print("Update speed:", min([speed, 780]))
    client.publish("speed", min([speed, 780]))
    speed_last = min([speed, 780])

    # update altitude
    print("Update altitude:", min([altitude, 12000]))
    client.publish("altitude", min([altitude, 12000]))
    altitude_last = min([altitude, 12000])
    
    
    # end.
    time.sleep(10)

