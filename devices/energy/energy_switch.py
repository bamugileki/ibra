import paho.mqtt.client as mqtt
import sys

BROKER = "localhost"
PORT = 1883
CMD_TOPIC = "home/energy/main/cmd"
STATUS_TOPIC = "home/energy/main/status"

state = "ON"

def on_connect(client, userdata, flags, rc):
    print(f"Energy Master Switch connected (rc={rc})", flush=True)
    client.subscribe(CMD_TOPIC)

def on_message(client, userdata, msg):
    global state
    cmd = msg.payload.decode().upper().strip()
    if cmd in ("ON", "OFF") and cmd != state:
        state = cmd
        client.publish(STATUS_TOPIC, state)
        print(f"Power: {state}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.publish(STATUS_TOPIC, "ON")

print("Energy Master Switch started (publish ON/OFF to home/energy/main/cmd)", flush=True)
client.loop_forever()
