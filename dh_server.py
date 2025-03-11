import socket

# Function for modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Substitution Cipher (Shift Cipher)
def encrypt(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def decrypt(text, shift):
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

# Take user input for Diffie-Hellman parameters
p = int(input("Server: Enter a prime number (p): "))
g = int(input("Server: Enter a primitive root (g): "))
private_key = int(input("Server: Enter your private key: "))

# Compute public key
public_key = mod_exp(g, private_key, p)

# Set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5555))
server.listen(1)

print("\nServer is waiting for a connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

# Send p and g to client
conn.send(f"{p} {g}".encode())

# Exchange public keys
conn.send(str(public_key).encode())
client_public_key = int(conn.recv(1024).decode())

# Compute shared secret
shared_secret = mod_exp(client_public_key, private_key, p)
shift_key = shared_secret % 256  # Use as shift value for encryption

print(f"Shared Secret Key: {shared_secret}")

# Receive encrypted message
encrypted_msg = conn.recv(1024).decode()
decrypted_msg = decrypt(encrypted_msg, shift_key)
print(f"Decrypted Message: {decrypted_msg}")

# Close connection
conn.close()
server.close()
