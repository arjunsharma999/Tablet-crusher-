import serial
import time

class GetData:
    def __init__(self, port='COM4', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def read_continuous(self, command="RAI01;", delay=1):
        if self.ser.is_open:
            try:
                while True:
                    # Send the command
                    self.ser.write(command.encode('ascii'))

                    # Read response
                    data = self.ser.readline().decode(errors='ignore').strip()
                    if data:
                        print("Card Response:", data)

                    time.sleep(delay)  # wait before sending next command
            except KeyboardInterrupt:
                print("Stopped by user.")
        else:
            raise ConnectionError("Serial port is not open.")

    def close(self):
        if self.ser.is_open:
            self.ser.close()


if __name__ == "__main__":
    card = GetData(port="/dev/ttyUSB0")
    try:
        print("Fetching continuous data... Press Ctrl+C to stop.")
        card.read_continuous(command="RAI01;", delay=0.1)
    finally:
        card.close()
