import paho.mqtt.client as mqtt
import time
import random

BROKER = "localhost"
PORT = 1883
TOPIC = "home/temperature/value"
POWER_TOPIC = "home/energy/main/status"

power_on = True

def on_connect(client, userdata, flags, rc):
    print(f"Temp sensor connected (rc={rc})", flush=True)
    client.subscribe(POWER_TOPIC)

def on_message(client, userdata, msg):
    global power_on
    if msg.topic == POWER_TOPIC:
        power_on = msg.payload.decode().upper().strip() == "ON"
        print(f"Power: {'ON' if power_on else 'OFF'}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Temperature sensor started (respects power state)", flush=True)
while True:
    if power_on:
        temp = round(random.uniform(22.0, 35.0), 2)
        client.publish(TOPIC, temp)
        print(f"Temp: {temp}C", flush=True)
    else:
        print("Temp sensor — power OFF, sleeping...", flush=True)
    time.sleep(5)
