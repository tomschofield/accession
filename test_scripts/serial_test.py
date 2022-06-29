import serial
import serial.tools.list_ports
import utils
import time


port_name = utils.getArduinoPort()
print("running on",port_name)
arduino = serial.Serial(port_name, 9600, timeout=5)
# s.write(str.encode('50\n'))

def write_read(x):
    arduino.write(str.encode('50\n'))
    # arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value
