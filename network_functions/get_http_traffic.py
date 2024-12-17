from scapy.all import sniff, TCP, IP, Raw
import socket
import whois

def http_traffic(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        # Filter for HTTP traffic (port 80 for unencrypted HTTP)
        # HTTPS uses port 443
        if dst_port == 443 or src_port == 443:
            if(src_ip not in ip_list):
                ip_list.append(src_ip)
                print(resolve_ipv2(src_ip))
            if(dst_ip not in ip_list):
                ip_list.append(dst_ip)
                print(resolve_ipv2(dst_ip))

# def extract_sni(packet):
#     if packet.haslayer(Raw):
#         raw_data = packet[Raw].load
#         # Check for TLS Handshake message (0x16 is the Handshake type)
#         if raw_data[0] == 0x16:  # TLS Handshake
#             handshake_type = raw_data[5]  # Client Hello type
#             if handshake_type == 1:  # 1 means Client Hello
#                 # Look for SNI in the extensions part of the Client Hello message
#                 sni_offset = 43  # Offset to the extensions
#                 while sni_offset < len(raw_data):
#                     # Extension type 0x00 is for SNI
#                     extension_type = raw_data[sni_offset:sni_offset+2]
#                     if extension_type == b'\x00\x00':  # SNI extension type
#                         sni_len = raw_data[sni_offset + 2] * 256 + raw_data[sni_offset + 3]
#                         sni = raw_data[sni_offset + 4: sni_offset + 4 + sni_len].decode('utf-8', errors='ignore')
#                         if sni in sni_list:
#                             sni_list[sni] += 1
#                         else:
#                             sni_list[sni] = 1
#                         print(sni)
#                         break
#                     sni_offset += 4 + (len(extension_type) + 2)  # Move by extension length
#     return


# Function to extract SNI from TLS Client Hello message
def extract_sni(packet):
    if packet.haslayer(Raw):
        raw_data = packet[Raw].load
        # Check for TLS Handshake message (0x16 is the Handshake type)
        if raw_data[0] == 0x16:  # TLS Handshake
            handshake_type = raw_data[5]  # Client Hello type
            if handshake_type == 1:  # 1 means Client Hello
                # Look for SNI in the extensions part of the Client Hello message
                sni_offset = 43  # Offset to the extensions
                while sni_offset < len(raw_data):
                    # Extension type 0x00 is for SNI
                    extension_type = raw_data[sni_offset:sni_offset+2]
                    if extension_type == b'\x00\x00':  # SNI extension type
                        sni_len = raw_data[sni_offset + 2] * 256 + raw_data[sni_offset + 3]
                        try:
                            sni = raw_data[sni_offset + 4: sni_offset + 4 + sni_len].decode('utf-8', errors='ignore')
                            print(f"Detected SNI: {sni}")
                        except UnicodeDecodeError:
                            # If decoding fails, just print that the SNI could not be decoded
                            print("SNI could not be decoded")
                        break
                    sni_offset += 4 + (len(extension_type) + 2)  # Move by extension length

def resolve_ip(ip):
    try:
        domain_name = socket.gethostbyaddr(ip)[0]
        return domain_name
    except socket.herror:
        return ip
    
def resolve_ipv2(ip):
    try:
        # Perform a WHOIS lookup
        w = whois.whois(ip)
        # Extract relevant company information
        return w.org or w.name or w.emails  # Return organization name, fallback to name or email
    except Exception as e:
        return ip
    
def stop_sniff(packet):
    return len(sni_list) >= 30

def start_sniff(target_ip):
    global ip_list, sni_list
    ip_list = []
    sni_list = {}
    sniff(
        filter=f"host {target_ip} and tcp port 443", 
        prn=extract_sni, 
        store=False,
        stop_filter=stop_sniff
    )
    return sni_list
