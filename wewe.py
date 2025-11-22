import snap7
from snap7.type import Areas

PLC_IP = "10.72.101.68"

c = snap7.client.Client()
c.connect(PLC_IP, 0, 1)

# Try reading up to 256 bytes (safe for S7-1500)
try:
    data = c.read_area(Areas.DB, 1, 0, 256)
    print(data.hex())
except Exception as e:
    print("Error:", e)

c.disconnect()
