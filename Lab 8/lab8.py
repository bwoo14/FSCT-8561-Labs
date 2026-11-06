# Uncomment if needed, then run once:
# %pip install pillow stepic
from pathlib import Path
import stepic
from PIL import Image
import hashlib
ASSET_DIR = Path("Lab8")
LOGO = ASSET_DIR / "compay_logo.png"
PROFILE = ASSET_DIR / "profile.png"
PYTHON_IMG = ASSET_DIR / "python.png"
OUTPUT_DIR = Path("Lab8_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

for path in [LOGO, PROFILE, PYTHON_IMG]:
	if not path.exists():
		raise FileNotFoundError(f"Missing {path}. Check where you extracted Lab8.zip")
	with Image.open(path) as image:
		print(path.name, image.size, image.mode, path.stat().st_size,"bytes")



def sha256_file(path):
	"""Calculate the SHA-256 digest of a file's exact bytes."""
	with open(path, "rb") as file:
		return hashlib.sha256(file.read()).hexdigest()
# Save baseline hashes now; we will use these values again in Part 5.
original_logo_hash = sha256_file(LOGO)
original_profile_hash = sha256_file(PROFILE)

print("Original logo SHA-256: ", original_logo_hash)
print("Original profile SHA-256:", original_profile_hash)


def set_LSB(value, bit):
	"""Return an integer with its least significant bit set to 0 or 1."""
	if bit not in ("0", "1"):
		raise ValueError("bit must be '0' or '1'")
	return (value & 254) if bit == "0" else (value | 1)

def get_LSB(value):
	return str(value & 1)
value = 201
for bit in ("0", "1"):
	changed = set_LSB(value, bit)
	print(value, format(value, "08b"), "→", changed, format(changed, "08b"), "LSB", get_LSB(changed))
assert set_LSB(150, "1") == 151
assert get_LSB(151) == "1"


sample = "HI"
raw = sample.encode("utf-8")
print("Characters:", list(sample))
print("Byte values:", list(raw))
print("Bits:", " ".join(format(b, "08b") for b in raw))
print("Terminator:", format(0, "08b"))

def max_message_bytes(width, height, channels=4, terminator_bytes=1):
	capacity_bytes = (width * height * channels) // 8
	return max(0, capacity_bytes - terminator_bytes)

print("100×100 RGBA:", max_message_bytes(100, 100, 4), "message bytes")
print("100×100 RGB:", max_message_bytes(100, 100, 3), "message bytes")
payload = "TARGET:192.168.1.50"
required_bytes = len(payload.encode("utf-8")) + 1

print("Payload + terminator:", required_bytes, "bytes")
print("Pixels needed (supplied RGBA method):", required_bytes * 2)
assert required_bytes == 20


# import sys
# sys.path.insert(0, str(ASSET_DIR.resolve()))
from steganography_LSB import hide_message, extract_message
TEST_STEGO = OUTPUT_DIR / "python_test_stego.png"
hide_message(str(PYTHON_IMG), "HI", str(TEST_STEGO))
recovered = extract_message(str(TEST_STEGO))
print("Recovered:", recovered)
assert recovered == "HI"

def encode_checked(source_path, message, output_path):
	"""Validate a short ASCII message, then call the supplied encoder."""
	source_path = Path(source_path)
	output_path = Path(output_path)
	if not source_path.is_file():
		raise FileNotFoundError(source_path)
	if not message:
		raise ValueError("Message must not be empty")
	if "\x00" in message:
		raise ValueError("Zero byte is reserved as a terminator")
	with Image.open(source_path) as image:
		available_pixels = image.width * image.height
	needed_pixels = 2 * (len(message.encode("utf-8")) + 1)
	# TODO 1: If needed_pixels exceeds available_pixels, raise ValueError.
	if available_pixels < needed_pixels:
		raise ValueError("Not enough available pixels")
	else:
		hide_message(source_path, message, output_path)
		return output_path
	# TODO 2: Call hide_message(...) with the three parameters.
	# TODO 3: Return output_path.
	raise NotImplementedError("Complete TODOs before running")

# After implementing, uncomment:
LOGO_STEGO = encode_checked(LOGO, "TARGET:192.168.1.50", OUTPUT_DIR / "company_logo_stego.png")
print(LOGO_STEGO)


def decode_manual(path):
	with Image.open(path) as image:
		pixels = list(image.convert("RGBA").get_flattened_data())
	decoded_bytes = bytearray()
	for index in range(0, len(pixels) - 1, 2):
		first, second = pixels[index], pixels[index + 1]
		# TODO: collect the eight LSBs from first + second
		byte = ''
		for channel in first:
			byte += get_LSB(channel)
		for channel in second:
			byte += get_LSB(channel)
		# TODO: convert the 8-bit string to an integer
		value = int(byte, 2)
		# TODO: stop if value == 0; otherwise append to decoded_bytes
		if value == 0:
			break
		else:
			decoded_bytes.append(value)
	# TODO: 
	return decoded_bytes.decode("utf-8")
	raise NotImplementedError("Complete the decoder")
# Test after completing both functions:
print(f"Result of Manual Decode: {decode_manual(LOGO_STEGO)}")
assert decode_manual(LOGO_STEGO) == "TARGET:192.168.1.50"
print(f"Result of Extract_message function {extract_message(str(LOGO_STEGO))}")
assert extract_message(str(LOGO_STEGO)) == "TARGET:192.168.1.50"



ports = [80, 443, 3478, 5060]
port_text = ",".join(str(port) for port in ports)
port_bytes = port_text.encode("utf-8")
print("Message:", port_text)
print("Bytes:", port_bytes)
assert port_text == "80,443,3478,5060"



# If Stepic is installed:

with Image.open(PROFILE) as source:
	rgb_image = source.convert("RGB")
	# TODO: call stepic.encode(rgb_image, port_bytes)
	encoded_image = stepic.encode(rgb_image, port_bytes)
	# TODO: save returned image to OUTPUT_DIR / "profile_secret.png"
	encoded_image.save(str(OUTPUT_DIR / "profile_secret.png"))

# TODO: Open profile_secret.png, call stepic.decode, normalize to text if needed.
with Image.open(OUTPUT_DIR / "profile_secret.png") as photo:
	recovered_port_text = stepic.decode(photo)
# TODO: assert recovered_port_text == port_text
	assert recovered_port_text == port_text
# Print the recovered text
print(f"Recovered text: {recovered_port_text}")

import json

def compare_images(original_path, stego_path):
	with Image.open(original_path) as original, Image.open(stego_path) as stego:
		a = list(original.convert("RGBA").get_flattened_data())
		b = list(stego.convert("RGBA").get_flattened_data())
		if original.size != stego.size:
			raise ValueError("Image dimensions differ")
	changed_pixels = sum(p != q for p, q in zip(a, b))
	changed_channels = sum(x != y for p, q in zip(a, b) for x, y in zip(p, q))
	return {
		"original_bytes": Path(original_path).stat().st_size,
		"stego_bytes": Path(stego_path).stat().st_size,
		"original_sha256": sha256_file(original_path),
		"stego_sha256": sha256_file(stego_path),
		"same_file_bytes": sha256_file(original_path) == sha256_file(stego_path),
		"changed_pixels": changed_pixels,
		"changed_channels": changed_channels,
		"total_pixels": len(a),
	}

print("Reference test:", json.dumps(compare_images(PYTHON_IMG, TEST_STEGO), indent=4))

# Task 5A — Complete after Parts 3 and 4.
# Uncomment and adapt these lines; keep the earlier baseline variables.
#
logo_stats = compare_images(LOGO, LOGO_STEGO)
profile_stego = OUTPUT_DIR / "profile_secret.png"
profile_stats = compare_images(PROFILE, profile_stego)

print("Original logo baseline matches current original:",
original_logo_hash == sha256_file(LOGO))
print("Original logo vs. stego identical:",
original_logo_hash == sha256_file(LOGO_STEGO))
print("Original profile vs. stego identical:",
original_profile_hash == sha256_file(profile_stego))

print("Logo pixel comparison:", json.dumps(logo_stats, indent=4))
print("Profile pixel comparison:", json.dumps(profile_stats, indent=4))

# TODO: Calculate and print the percentage of changed pixels for each pair.
logo_change = ( logo_stats["changed_pixels"] / logo_stats["total_pixels"]  ) * 100
profile_change = ( profile_stats["changed_pixels"] / profile_stats["total_pixels"]  ) * 100

print(f"Percent change for Logo Picture: {logo_change:.10f}%")
print(f"Percent change for Profile Picture: {profile_change:.10f}%")

# TODO: In a Markdown cell, explain what your actual hash results demonstrate.

# The hash results show that changing the pixels even slightly results in a completely different hash. This means we can easily tell if
# an image has been tampered with if we have the original hash.


# Run after completing your manual decoder in Part 3.
before_extract = sha256_file(LOGO_STEGO)
recovered = decode_manual(LOGO_STEGO)
after_extract = sha256_file(LOGO_STEGO)

print("Recovered message:", recovered)
print("Before extraction:", before_extract)
print("After extraction: ", after_extract)
assert before_extract == after_extract, "Extraction unexpectedly changed the file!"
assert recovered == "TARGET:192.168.1.50"

# TODO: Repeat for profile_secret.png with stepic.decode(...).

before_extract = sha256_file(profile_stego)

with Image.open(profile_stego) as photo:
	recovered = stepic.decode(photo)
after_extract = sha256_file(profile_stego)

print("Recovered message:", recovered)
print("Before extraction:", before_extract)
print("After extraction: ", after_extract)
assert before_extract == after_extract, "Extraction unexpectedly changed the file!"
assert recovered == "80,443,3478,5060"


# TODO: Record whether the hash changed and explain why this matters.


def show_pair(original_path, stego_path):
	with Image.open(original_path) as original, Image.open(stego_path) as stego:
		print("Original:")
		original.resize((300, 300)).show()

		print("Stego:")
		stego.resize((300, 300)).show()

# TODO: 
show_pair(LOGO, LOGO_STEGO)
# TODO: 
show_pair(PROFILE, OUTPUT_DIR / "profile_secret.png")
