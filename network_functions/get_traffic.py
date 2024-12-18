from scapy.all import sniff, TCP, IP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time
from collections import deque
import os
import socket

class TrafficWidget:
    def __init__(self):
        self.ip_list = []  
        self.packet_count = deque([0] * 10, maxlen=10)  
        self.time_window = deque(range(10), maxlen=10)  
        self.start_time = time.time()
    
    # function to resolve IP addresses 
    def resolve_ipv2(self, ip):
        try:
            return f"{ip} -> {socket.gethostbyaddr(ip)[0]}"
        except Exception:
            return f"{ip} -> Unknown Host"

    def http_traffic(self, packet):
        if packet.haslayer(IP) and packet.haslayer(TCP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

            # Filter for HTTP/HTTPS traffic (ports 80 and 443)
            if dst_port in [80, 443] or src_port in [80, 443]:
                if src_ip not in self.ip_list:
                    self.ip_list.append(src_ip)
                    print(self.resolve_ipv2(src_ip))
                if dst_ip not in self.ip_list:
                    self.ip_list.append(dst_ip)
                    print(self.resolve_ipv2(dst_ip))
                
                # Update packet count for the current time window
                elapsed_time = int(time.time() - self.start_time)
                if elapsed_time > self.time_window[-1]:  
                    self.packet_count.append(1)
                    self.time_window.append(elapsed_time)
                else:
                    self.packet_count[-1] += 1

    def update_plot(self):
        plt.plot(self.time_window, self.packet_count, linestyle='-', color='b')
        plt.title("Packets Received Over Time")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Number of Packets")
        output_path = os.path.abspath("outputs/packet_traffic.jpeg")
        plt.savefig(output_path)
        plt.close()

    def plot_traffic(self):
        try:
            while True:
                sniff(prn=self.http_traffic, store=0, timeout=1)  # Capture packets for 1 second
                self.update_plot()  # Update the graph
        except KeyboardInterrupt:
            print("Stopping traffic monitoring...")

if __name__ == "__main__":
    widget = TrafficWidget()
    widget.plot_traffic()
