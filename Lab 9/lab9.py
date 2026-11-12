import hashlib
# password = input("Enter a password: ")
# hash_object = hashlib.sha256(password.encode())
# hash_object = hashlib.md5(password.encode())
# print("SHA-256 hash:", hash_object.hexdigest())


import uuid
def hash_password(password):
	salt = uuid.uuid4().hex
	hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
	return hashed + ":" + salt
def check_password(stored_password, user_input):
	hashed, salt = stored_password.split(":")
	return hashed == hashlib.sha256(salt.encode() + user_input.encode()).hexdigest()

# password = input("Enter password: ")
# stored = hash_password(password)
# print("Stored:", stored)
# verify = input("Re-enter password: ")
# print("Match:", check_password(stored, verify))


# from Crypto.Cipher import DES
# key = "myc1pher".encode("utf8") # 8 bytes
# message = "message".ljust(8).encode("utf8") # 8 bytes
# cipher = DES.new(key, DES.MODE_ECB)
# cipher_text = cipher.encrypt(message)
# print("Encrypted:", cipher_text)
# cipher = DES.new(key, DES.MODE_ECB)
# plain_text = cipher.decrypt(cipher_text)
# print("Decrypted:", plain_text.decode())


# from Crypto.Cipher import AES
# # AES-128 requires a 16-byte key
# key = "secret-key-12345".encode("utf8")
# iv = "This is an IV456".encode("utf8")
# cipher = AES.new(key, AES.MODE_CBC, iv)
# # Data must be a multiple of 16 bytes
# message = "This is a secret message for lab".ljust(234).encode("utf8")
# cipher_text = cipher.encrypt(message)
# print(f"AES Encrypted: {cipher_text.hex()}")
# # Decrypt using the same IV
# decipher = AES.new(key, AES.MODE_CBC, iv)
# plain_text = decipher.decrypt(cipher_text)
# print(f"Decrypted: {plain_text.decode().strip()}")

from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
# password = "mypassword"
# # salt = Random.new().read(16)
# salt = b'fixedsalt123456'
# key = PBKDF2(password, salt, dkLen=16, count=100)
# print("Key:", key)

from cryptography.fernet import Fernet, InvalidToken
# key = Fernet.generate_key()
# cipher = Fernet(key)
# message = "Secret message".encode()
# encrypted = cipher.encrypt(message)
# print("Encrypted:", encrypted)
# decrypted = cipher.decrypt(encrypted)
# print("Decrypted:", decrypted.decode())

# Generate a key and encrypt a message
# key = Fernet.generate_key()
# cipher = Fernet(key)
# encrypted = cipher.encrypt(b"Secret message")

# bad_key = Fernet.generate_key() 

# bad_cipher = Fernet(bad_key)

# try:
#     decrypted = bad_cipher.decrypt(encrypted)
#     print("Decrypted:", decrypted.decode())
# except InvalidToken:
#     print("Error: Decryption failed because the key was modified or incorrect!")

import hashlib
target_hash = "81dc9bdb52d04dc20036dbd8313ed055"
print("Starting Brute Force Attack...")
# --- STUDENT TODO: COMPLETE THE LOGIC BELOW ---
# 1. Create a loop that goes from 0 to 9999
# 2. Use str(i).zfill(4) to ensure numbers like 7 become "0007"
# 3. Hash the string using hashlib.md5()
# 4. Compare the result to the target_hash
# 5. Print the PIN if you find a match
# YOUR CODE HERE:
for i in range(0, 9999 + 1):
	index = str(i).zfill(4)
	hashed = hashlib.md5(index.encode())
	if hashed.hexdigest() == target_hash:
		print(f"PIN FOUND: {index}")
		break
# --- END TODO --

from Crypto.Cipher import DES
# key = "security".encode("utf8")
# cipher = DES.new(key, DES.MODE_ECB)
# # Encrypting two separate data packets
# packet_1 = "DATA_REQ".encode("utf8")
# packet_2 = "DATA_REQ".encode("utf8")
# print(f"Packet 1 Ciphertext: {cipher.encrypt(packet_1).hex()}")
# print(f"Packet 2 Ciphertext: {cipher.encrypt(packet_2).hex()}")