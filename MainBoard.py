import serial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port


ser.write(sd:10:10:0:0)     # write a string

for i in range(300):
    if i%30==0:
        ser.write(sd:10:10:0:0)
    if 0xFF == ord('q'):
        ser.write(sd:0:0:0:0)
        break

ser.write(sd: 0:0: 0:0)
ser.close()