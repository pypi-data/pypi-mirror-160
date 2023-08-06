from pn5180.sensor import ISO15693Sensor
import time

if __name__ == "__main__":
    reader = ISO15693Sensor()
    while True:
        response = reader.read_tag()
        print(f"Response: {response}")
        time.sleep(0.2)
