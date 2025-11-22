import struct
import snap7
from snap7.util import set_bool
from snap7.type import Areas
from opcua import Client, ua


PLC_IP = "10.72.101.68"
OPC_URL = f"opc.tcp://{PLC_IP}:4840"

# ------------------------------------------------------------
# NS1 (Snap7)
# ------------------------------------------------------------

def s7_connect():
    c = snap7.client.Client()
    c.connect(PLC_IP, 0, 1)
    return c


def ns1_turn_on():
    c = s7_connect()
    data = c.read_area(Areas.DB, 1, 0, 1)
    set_bool(data, 0, 0, True)   # DB1.DBX0.0
    c.write_area(Areas.DB, 1, 0, data)
    c.disconnect()
    print("[NS1] Light ON")


def ns1_set_timer_via_db(db, byte_offset, value_ms):
    """
    Writes a DINT timer in milliseconds to NS1 DB.
    Adjust DB/offset according to your PLC.
    """
    c = s7_connect()
    data = struct.pack(">i", value_ms)
    c.write_area(Areas.DB, db, byte_offset, data)
    c.disconnect()
    print(f"[NS1] Timer set to {value_ms} ms (DB{db}.DBD{byte_offset})")


# ------------------------------------------------------------
# NS2 (OPC UA)
# ------------------------------------------------------------

NODE_ON_OFF    = 'ns=3;s="DATA_HACK_NS2"."ON_OFF"'
NODE_TEMPS_ON  = 'ns=3;s="DATA_HACK_NS2"."TEMPS_ON"'
NODE_TEMPS_OFF = 'ns=3;s="DATA_HACK_NS2"."TEMPS_OFF"'


def opc_write_any(client, nodeid, value):
    node = client.get_node(nodeid)
    current_type = node.get_data_value().Value.VariantType
    dv = ua.DataValue(ua.Variant(value, current_type))
    node.set_value(dv)
    print(f"[NS2] {nodeid}={value} (type matched)")


def ns2_set_timer_and_start(time_ms):
    c = Client(OPC_URL)
    c.connect()

    opc_write_any(c, NODE_TEMPS_ON, time_ms)
    opc_write_any(c, NODE_TEMPS_OFF, time_ms)
    opc_write_any(c, NODE_ON_OFF, True)

    c.disconnect()
    print("[NS2] Timer configured + ON_OFF TRUE")


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------

print("\n=== NS1 ===")
ns1_turn_on()

ns1_set_timer_via_db(db=1, byte_offset=4, value_ms=4000)

print("\n=== NS2 ===")
ns2_set_timer_and_start(1)  

print("\n[OK] NS1 and NS2 done.")
