from scapy.all import get_if_list, get_if_addr, sniff

def find_wifi_interface():
    interfaces = get_if_list()
    for iface in interfaces:
        ip_address = get_if_addr(iface)
        if ip_address.startswith("192.168.") or ip_address.startswith("172."):
            return iface
    raise ValueError("No se encontró ninguna interfaz Wi-Fi activa.")

def packet_callback(packet):
    if packet.haslayer('TCP'):
        print(f"Tráfico TCP detectado: {packet.summary()}")
    elif packet.haslayer('UDP'):
        print(f"Tráfico UDP detectado: {packet.summary()}")
    else:
        print(f"Otro tipo de tráfico detectado: {packet.summary()}")

def start_traffic_monitor():
    try:
        wifi_interface = find_wifi_interface()
        print(f"Iniciando monitoreo de tráfico en la interfaz: {wifi_interface}")
        sniff(iface=wifi_interface, prn=packet_callback, store=False)
    except Exception as e:
        print(f"Error al iniciar el monitoreo: {e}")

    def monitor_traffic(interface, callback):
        def packet_callback(packet):
            # Procesamiento del paquete
            callback(packet)
            
        sniff(iface=interface, prn=packet_callback, store=False)