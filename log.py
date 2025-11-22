from opcua import Client

def browse_node_to_file(node, file, depth=0):
    indent = " " * (depth * 2)
    browse_name = node.get_browse_name().Name
    node_str = f"{indent}{node}: {browse_name}\n"
    file.write(node_str)
    for child in node.get_children():
        browse_node_to_file(child, file, depth + 1)

url = "opc.tcp://10.72.101.68:4840"
client = Client(url)
client.connect()
try:
    root = client.get_root_node()
    with open("opcua_browse_log.txt", "w", encoding="utf-8") as logfile:
        logfile.write("Browsing OPC UA address space:\n")
        browse_node_to_file(root, logfile)
finally:
    client.disconnect()

print("Browse results logged to opcua_browse_log.txt")

