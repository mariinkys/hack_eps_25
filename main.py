import time
import snap7
from snap7.util import set_bool
from snap7.type import Areas

def connect_to_plc(ip="192.168.0.1", rack=0, slot=1):
    client = snap7.client.Client()
    client.connect(ip, rack, slot)

    if client.get_connected():
        print("Connected to PLC!")
    else:
        print("Connection failed")

    return client

def on_light(client, db_number, byte_index, bit_index):
    """
    Enciende y apaga un bit en un DB concreto.
    """

    data = client.read_area(Areas.DB, db_number, byte_index, 1)

    print(f"[+] Luz en DB{db_number}.BYTE{byte_index}.BIT{bit_index} → ON")
    set_bool(data, 0, bit_index, True)
    client.write_area(Areas.DB, db_number, byte_index, data)

plc = connect_to_plc("10.72.101.68", rack=0, slot=1)
on_light(plc, db_number=1, byte_index=0, bit_index=0)
on_light(plc, db_number=2, byte_index=0, bit_index=0)

try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    print("Script detenido por el usuario.")
    plc.disconnect()