from Crypto.PublicKey import RSA
def generate_keys(username):
    # Generate a new RSA key pair
    key = RSA.generate(2048)
    # Export the private key in PEM format
    private_key = key.export_key()
    # Export the public key in PEM format
    public_key = key.publickey().export_key()
    # Save the private key to a file with the username in the filename
    with open(f'{username}_private.pem', 'wb') as priv_file:
        priv_file.write(private_key)
    
    
