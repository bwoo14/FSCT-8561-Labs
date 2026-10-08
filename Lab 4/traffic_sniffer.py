from scapy.all import rdpcap 
from scapy.all import TCP, UDP
from scapy.all import IP

# open packet capture
packets = rdpcap("botnet-capture-20110812-rbot.pcap")


# Loop through first 20 packets
for pkt in packets[:20]:
	try:
		if TCP in pkt:
			# IF TCP print packet
			print(f"Source: {pkt[IP].src} Destination: {pkt[IP].dst} Protocol: TCP Source Port: {pkt[TCP].sport} Destination Port: {pkt[TCP].dport}")
		elif UDP in pkt:
			# IF UDP, print packet
			print(f"Source: {pkt[IP].src} Destination: {pkt[IP].dst} Protocol: UDP Source Port: {pkt[UDP].sport} Destination Port: {pkt[UDP].dport}")
	except IndexError: # Handle errors
		print("ERROR with Packet")

# Set counters
tcp_count = 0
udp_count = 0

# iterate over packets
for pkt in packets:
	if TCP in pkt: # IF TCP, increase count by 1
		tcp_count += 1
	elif UDP in pkt: # IF UDP, increase count by 1
		udp_count +=1

print(f"Total TCP Packets: {tcp_count}")
print(f"Total UDP Packets: {udp_count}")
