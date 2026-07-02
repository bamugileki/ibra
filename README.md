# IoT Lab

A lightweight IoT simulation environment using Docker, MQTT, Home Assistant, and simulated smart devices.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Docker Network                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Mosquitto │  │ Home         │  │ Node-RED     │   │
│  │ MQTT      │←─→│ Assistant    │  │ (optional)   │   │
│  │ Broker    │  │ :8123        │  │ :1880        │   │
│  │ :1883     │  └──────────────┘  └──────────────┘   │
│  └────┬─────┘                                        │
│       │                                              │
│  ┌────┴──────────────────────────────────────────┐   │
│  │  Simulated Devices (Python)                   │   │
│  │  ┌───────┐ ┌───────┐ ┌──────┐ ┌─────────┐   │   │
│  │  │ Light │ │ Door  │ │Motion│ │ Temp    │   │   │
│  │  │       │ │ Lock  │ │Sensor│ │ Sensor  │   │   │
│  │  └───────┘ └───────┘ └──────┘ └─────────┘   │   │
│  │  ┌────────────┐ ┌──────────────────────┐     │   │
│  │  │ Energy     │ │ Master Power Switch  │     │   │
│  │  │ Meter      │ │ (controls all        │     │   │
│  │  │            │ │  devices on/off)     │     │   │
│  │  └────────────┘ └──────────────────────┘     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

All communication goes through the **MQTT broker** — devices publish sensor data and listen for commands.

## Services

| Service         | Port   | Description                                      |
|-----------------|--------|--------------------------------------------------|
| **Mosquitto**   | 1883   | MQTT message broker                              |
| **Home Assistant** | 8123 | Web UI for dashboards, automation, device control |
| **Node-RED**    | 1880   | Flow-based visual automation editor              |

## MQTT Topics

| Topic                          | Direction      | Description                          |
|--------------------------------|----------------|--------------------------------------|
| `home/light/cmd`               | ⬅ Command      | Send `ON` or `OFF`                   |
| `home/light/status`            | ➡ Status       | Publishes `ON` / `OFF` / `OFFLINE`   |
| `home/door/cmd`                | ⬅ Command      | Send `LOCK` or `UNLOCK`              |
| `home/door/status`             | ➡ Status       | Publishes `LOCKED` / `UNLOCKED` / `OFFLINE` |
| `home/motion/status`           | ➡ Status       | `MOTION_DETECTED` / `NO_MOTION`      |
| `home/temperature/value`       | ➡ Status       | Temperature reading (e.g. `27.4`)    |
| `home/energy/power`            | ➡ Status       | Current power consumption in Watts   |
| `home/energy/total`            | ➡ Status       | Total accumulated energy in kWh      |
| `home/energy/main/cmd`         | ⬅ Command      | Send `ON` or `OFF` (master power)    |
| `home/energy/main/status`      | ➡ Status       | Master power state (`ON` / `OFF`)    |

## Master Power Switch

The **Energy Master Switch** (`energy_switch.py`) acts as a virtual main breaker. When set to `OFF`, all devices go **OFFLINE** — they stop publishing data and ignore commands. Turning it `ON` restores normal operation.

## How to Run

```bash
# Start infrastructure containers
docker compose up -d

# Open separate terminals and run each device:
python devices/energy/energy_switch.py
python devices/energy/energy.py
python devices/light/light.py
python devices/door/door_lock.py
python devices/motion/motion.py
python devices/temperature/temperature.py
```

Once running, open **Home Assistant** at `http://localhost:8123` to see and control the devices.
