from scapy.all import rdpcap 
from scapy.all import TCP
# Get capture
packets = rdpcap("botnet-capture-20110812-rbot.pcap")


# Count packets
print("Number of packets:", len(packets))


# Look at first packet
print(packets[0].summary())


# Get five packets
for pkt in packets[:5]:
	print(pkt.summary())



pkt = packets[0]
print("Is this TCP?", TCP in pkt)

# keep only tcp packets
tcp_packets = []
for pkt in packets:
	if TCP in pkt:
		tcp_packets.append(pkt)

print("TCP packets:", len(tcp_packets))

# Print 50 packets
for pkt in tcp_packets[:50]:
	print(pkt.summary())

# Filter traffic using TCP port 80
if len(tcp_packets) > 0:
	pkt = tcp_packets[0]
	print("Source port:", pkt[TCP].sport)
	print("Destination port:", pkt[TCP].dport)


http_packets = []
for pkt in tcp_packets:
	if pkt[TCP].sport == 80 or pkt[TCP].dport == 80:
		http_packets.append(pkt)
print("TCP port 80 packets:", len(http_packets))
for pkt in http_packets[:50]:
	print(pkt.summary())



from scapy.all import UDP
dns_packets = []
for pkt in packets:
	if UDP in pkt:
		if pkt[UDP].sport == 53 or pkt[UDP].dport == 53:
			dns_packets.append(pkt)


print("UDP port 53 packets:", len(dns_packets))
for pkt in dns_packets[:50]:
	print(pkt.summary())