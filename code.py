import time
import SCD4X
import wifi
import socketpool
import os
import adafruit_minimqtt.adafruit_minimqtt as MQTT

SSID = os.getenv("CIRCUITPY_WIFI_SSID")
WIFI_PASSWORD = os.getenv("CIRCUITPY_WIFI_PASSWORD")

try:
    print("Connecting to %s" % SSID)
    wifi.radio.connect(SSID, WIFI_PASSWORD)
    print("Connected to %s!" % SSID)
except Exception:  # pylint: disable=broad-except
    print("Failed to connect to WiFi.")

pool = socketpool.SocketPool(wifi.radio)

mqtt_client = MQTT.MQTT(
    broker="192.168.1.100",
    socket_pool=pool
)

def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT broker!")


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected

mqtt_client.connect()

device = SCD4X.SCD4X(quiet=False)
device.start_periodic_measurement()


while True:
    co2, temperature, relative_humidity, timestamp = device.measure()
    print(co2, temperature, relative_humidity, timestamp)

    mqtt_client.publish("/broker/feeds/sensors/SCD4X", co2)

    time.sleep(1)
