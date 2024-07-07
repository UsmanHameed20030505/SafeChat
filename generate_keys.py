from Crypto.PublicKey import RSA
def generate_keys(username):
    # Generate a new RSA key pair
    key = RSA.generate(2048)
    # Export the private key in PEM format
    private_key = key.export_key()
    # Export the public key in PEM format
    public_key = key.publickey().export_key()
    
