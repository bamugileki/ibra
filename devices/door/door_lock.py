import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
CMD_TOPIC = "home/door/cmd"
STATUS_TOPIC = "home/door/status"
POWER_TOPIC = "home/energy/main/status"

door_state = "LOCKED"
power_on = True

def on_connect(client, userdata, flags, rc):
    print(f"Door connected (rc={rc})", flush=True)
    client.subscribe(CMD_TOPIC)
    client.subscribe(POWER_TOPIC)

def on_message(client, userdata, msg):
    global door_state, power_on

    if msg.topic == POWER_TOPIC:
        power_on = msg.payload.decode().upper().strip() == "ON"
        print(f"Power: {'ON' if power_on else 'OFF'}", flush=True)
        client.publish(STATUS_TOPIC, "OFFLINE" if not power_on else door_state)
        return

    if not power_on:
        print(f"Ignored {msg.payload.decode()} — power OFF", flush=True)
        return

    command = msg.payload.decode().upper()
    if command == "UNLOCK":
        door_state = "UNLOCKED"
    elif command == "LOCK":
        door_state = "LOCKED"
    else:
        return

    client.publish(STATUS_TOPIC, door_state)
    print(f"Door: {door_state}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
