import struct
import time
import snap7
from snap7.util import set_bool
from snap7.type import Areas
from opcua import Client, ua

PLC_IP = "10.72.101.68"
OPC_URL = f"opc.tcp://{PLC_IP}:4840"

# ============================================================
# NS1 FUNCTIONS (Snap7)
# ============================================================

NS1_ON_TIMER = 1
NS1_OFF_TIMER = 1

def s7_connect():
    c = snap7.client.Client()
    c.connect(PLC_IP, 0, 1)
    return c

def s7_set_timers(c: Client):
    c.write_area(Areas.DB, 1, 2, struct.pack('>H', NS1_ON_TIMER))
    c.write_area(Areas.DB, 1, 4, struct.pack('>H', NS1_OFF_TIMER))

# ============================================================
# NS2 FUNCTIONS (OPC UA)
# ============================================================

NODE_ON_OFF    = 'ns=3;s="DATA_HACK_NS2"."ON_OFF"'
NODE_TEMPS_ON  = 'ns=3;s="DATA_HACK_NS2"."TEMPS_ON"'
NODE_TEMPS_OFF = 'ns=3;s="DATA_HACK_NS2"."TEMPS_OFF"'
HELP_VALUE = 'ns=3;s="DATA_HACK_NS2"."NS1_HELP"'

def opc_write_any(client, nodeid, value):
    node = client.get_node(nodeid)
    t = node.get_data_value().Value.VariantType
    dv = ua.DataValue(ua.Variant(value, t))
    node.set_value(dv)
    print(f"[NS2] {nodeid} = {value} (type OK)")

def ns2_set_timer_and_start(ms_time):
    c = Client(OPC_URL)
    c.connect()
    opc_write_any(c, NODE_TEMPS_ON, ms_time)
    opc_write_any(c, NODE_TEMPS_OFF, ms_time)
    opc_write_any(c, NODE_ON_OFF, True)
    opc_write_any(c, HELP_VALUE, "1")
    c.disconnect()
    print("[NS2] Timer set + ON_OFF TRUE")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":

    print("\n=== NS1 ===")
    c = s7_connect()
    s7_set_timers(c)
    c.disconnect()

    print("\n=== NS2 ===")
    ns2_set_timer_and_start(1)  # 1 second

    print("\n[✓] NS1 + NS2 complete")
