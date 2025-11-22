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

def blink_light(client, db_number, byte_index, bit_index, duration=1):
    """
    Enciende y apaga un bit en un DB concreto (parpadeo visible).
    """

    # Leer 1 byte del DB donde está la luz
    data = client.read_area(Areas.DB, db_number, byte_index, 1)

    print(f"[+] Luz en DB{db_number}.BYTE{byte_index}.BIT{bit_index} → ON")
    set_bool(data, 0, bit_index, True)
    client.write_area(Areas.DB, db_number, byte_index, data)

    time.sleep(duration)

    print(f"[-] Luz en DB{db_number}.BYTE{byte_index}.BIT{bit_index} → OFF")
    set_bool(data, 0, bit_index, False)
    client.write_area(Areas.DB, db_number, byte_index, data)


plc = connect_to_plc("10.72.101.68", rack=0, slot=1)
blink_light(plc, db_number=1, byte_index=0, bit_index=0, duration=10)
