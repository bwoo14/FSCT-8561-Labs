import hashlib

# Returns a 256 Hashed string
def hash_password(password):
	return hashlib.sha256(
		password.encode()
	).hexdigest()

# return true if password correct, otherwise false
def verify_password(entered_hash, stored_hash):
	if entered_hash == stored_hash:
		return True
	else:
		return False



# Stored_hash
stored_hash = hash_password("Cyber123!")

# entered password and hash
entered_password = "Cyber123!!!"
entered_hash = hash_password(
	entered_password
)
# Call verify_password and print accepted if correct, otherwise reject
# if verify_password(entered_hash, stored_hash):
# 	print("Password accepted")
# else:
# 	print("Password rejected")

hashed_password = hash_password("Cyber123!")
# User database without plaintext password
users = {
	"alice": {
		"password_hash": hashed_password
	}
}
print(users["alice"])