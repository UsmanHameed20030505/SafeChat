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
    # Save the public key to a file with the username in the filename
    with open(f'{username}_public.pem', 'wb') as pub_file:
        pub_file.write(public_key)
    # Print a message indicating that the keys were generated successfully
    print(f'Keys generated for {username}')
    
