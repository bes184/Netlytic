from scapy.all import ARP, Ether, srp, conf, get_if_hwaddr
import socket
import os
import matplotlib.pyplot as plt

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        return hostname[0]
    except socket.herror:
        return None
    
def scan_network(ip):
    print("starting scan")
    
    # Create an ARP request packet
    ip_parts = ip.split(".")
    ip_parts[3] = "0"
    ip = ".".join(ip_parts)
    ip_range = f"{ip}/24"
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    
    # Send the packet and get the response
    answered = srp(packet, timeout=3, verbose=False)[0]        

    devices = []
    num_devices = []
    device_ips = []
    for device in answered:
        device_dict = {
            "ip": device[1].psrc,
            "mac": device[1].hwsrc,
            "hostname": get_hostname(device[1].psrc)
        }
        devices.append(device_dict)
        num_devices.append(1)
        device_ips.append(device[1].psrc)
        if(len(num_devices) == 5):
            print("scanned 5 devices")
            break

    plt.pie(num_devices, colors=plt.cm.tab20c.colors)
    plt.legend(labels=device_ips, loc="upper right")
    output_path = os.path.abspath("outputs/devices_pie.jpeg")
    plt.savefig(output_path, transparent=True)
    
    print("Devices found on the network:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}")

    return devices

def get_current_ip():
    current_ip = conf.route.route("0.0.0.0")[1]
    return current_ip

def get_current_mac():
    current_mac = get_if_hwaddr(conf.iface)
    return current_mac

if __name__ == "__main__":
    curr_ip = get_current_ip()
    scan_network(curr_ip)
    input("enter")
    curr_hostname = get_hostname(curr_ip)
    ip_list = []
    sni_list = []
    print(f"IP: {curr_ip}, Hostname: {curr_hostname}")