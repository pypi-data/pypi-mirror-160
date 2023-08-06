from pigpio import pi
import time

from pn5180.sensor import ISO15693Sensor

if __name__ == "__main__":
    pi = pi()
    reader = ISO15693Sensor(pi)
    while True:
        response = reader.read_tag()
        print(f"Response: {response}")
        time.sleep(0.1)
