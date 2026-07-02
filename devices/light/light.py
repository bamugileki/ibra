import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
CMD_TOPIC = "home/light/cmd"
STATUS_TOPIC = "home/light/status"
POWER_TOPIC = "home/energy/main/status"

light_state = "OFF"
power_on = True

def on_connect(client, userdata, flags, rc):
    print(f"Light connected (rc={rc})", flush=True)
    client.subscribe(CMD_TOPIC)
    client.subscribe(POWER_TOPIC)

def on_message(client, userdata, msg):
    global light_state, power_on

    if msg.topic == POWER_TOPIC:
        power_on = msg.payload.decode().upper().strip() == "ON"
        print(f"Power: {'ON' if power_on else 'OFF'}", flush=True)
        if not power_on:
            client.publish(STATUS_TOPIC, "OFFLINE")
        else:
            client.publish(STATUS_TOPIC, light_state)
        return

    if not power_on:
        print(f"Ignored {msg.payload.decode()} — power OFF", flush=True)
        return

    command = msg.payload.decode().upper()
    if command == "ON":
        light_state = "ON"
    elif command == "OFF":
        light_state = "OFF"
    else:
        return

    client.publish(STATUS_TOPIC, light_state)
    print(f"Light: {light_state}", flush=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
