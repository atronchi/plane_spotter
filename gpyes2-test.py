
import pynmea2 as nmea

msgs = [] 
with open('/dev/ttyACM0', 'r') as f: 
    for i in range(100): 
        ln = f.readline()
        if ln == '\n': continue

        msg = nmea.parse(ln.strip())
        print(msg)

        msgs.append(msg) 

