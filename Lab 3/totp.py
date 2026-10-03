import pyotp
import hashlib

USERS = {
	
}

# Return true if OTP is correct
def verify_otp(secret, otp):
	totp = pyotp.TOTP(secret)
	return totp.verify(otp)

# Returns a 256 Hashed string
def hash_password(password):
	return hashlib.sha256(
		password.encode()
	).hexdigest()

alice_secret = pyotp.random_base32()
users = {
	"alice": {
	"password_hash": hash_password(
		"Cyber123!"
	),
	"totp_secret": alice_secret
	}
}
print(
	"Alice's TOTP secret:",
	users["alice"]["totp_secret"]
)

# Create TOTP object
totp = pyotp.TOTP(
	users["alice"]["totp_secret"]
)

# Get Authenticator link
uri = totp.provisioning_uri(
	name="alice",
	issuer_name="FSCT8561-Lab3"
)
print(uri)



# # Create otp secret
# secret = pyotp.random_base32()

# # Print secret
# # print("TOTP secret:")
# # print(secret)

# # get totp object using secret
# totp = pyotp.TOTP(secret)
# # get the current TOTP
# current_otp = totp.now()
# print("Current OTP:", current_otp)

# # Get OTP
# entered_otp = input('Type in OTP: ')

# # Confirm if OTP accepted
# if verify_otp(secret, entered_otp):
# 	print("OTP accepted")
# else:
# 	print("OTP rejected")