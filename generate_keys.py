from Crypto.PublicKey import RSA
def generate_keys(username):
    # Generate a new RSA key pair
    key = RSA.generate(2048)
