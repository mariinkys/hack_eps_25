import snap7

def connect_to_plc(ip="192.168.0.1", rack=0, slot=1):
    client = snap7.client.Client()
    client.connect(ip, rack, slot)

    if client.get_connected():
        print("Connected to PLC!")
    else:
        print("Connection failed")

    return client

plc = connect_to_plc("10.72.101.68", rack=0, slot=1)
