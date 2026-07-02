import paho.mqtt.client as mqtt
import time
import random

BROKER = "localhost"
PORT = 1883
POWER_TOPIC = "home/energy/power"
ENERGY_TOPIC = "home/energy/total"
POWER_STATE_TOPIC = "home/energy/main/status"

power_on = True
total_kwh = 0.0

def on_connect(client, userdata, flags, rc):
    print(f"Energy meter connected (rc={rc})", flush=True)
    client.subscribe(POWER_STATE_TOPIC)

def on_message(client, userdata, msg):
    global power_on
    if msg.topic == POWER_STATE_TOPIC:
        power_on = msg.payload.decode().upper().strip() == "ON"
        print(f"Power: {'ON' if power_on else 'OFF'}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Energy meter started (respects power state)", flush=True)
while True:
    if power_on:
        power = round(random.uniform(50.0, 500.0), 2)
        total_kwh += round(power * (10 / 3600), 3)
        client.publish(POWER_TOPIC, power)
        client.publish(ENERGY_TOPIC, round(total_kwh, 3))
        print(f"Energy: {power}W / {total_kwh:.3f}kWh", flush=True)
    else:
        print("Energy meter — power OFF, sleeping...", flush=True)
    time.sleep(10)
