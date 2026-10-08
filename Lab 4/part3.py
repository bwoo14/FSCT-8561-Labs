from scapy.all import rdpcap 
from scapy.all import TCP
from scapy.all import Raw
# Get capture
packets = rdpcap("botnet-capture-20110812-rbot.pcap")

# check if there is a raw payload
pkt = packets[0]
print("Contains Raw payload?", Raw in pkt)


# Show sample
if Raw in pkt:
	print(repr(bytes(pkt[Raw].load)[:80]))
else:
	print("No Raw payload in this packet")

# Find raw packets, stop at first
for pkt in packets:
	if Raw in pkt:
		print("RIGHT HERE")
		print("Payload sample:", repr(bytes(pkt[Raw].load)[:80]))
	break

# display small sample
for pkt in packets:
	if Raw in pkt:
		sample = bytes(pkt[Raw].load)[:80]
		print(sample.decode("utf-8", errors="replace"))
		break

# Look for familiar http header
found = False
for pkt in packets:
	if Raw in pkt:
		data = bytes(pkt[Raw].load)
		if b"User-Agent:" in data:
			print("Possible plaintext HTTP header found")
			print(data)
			found = True
			break
if not found:
	print("No matching header found in the first 500 packets")