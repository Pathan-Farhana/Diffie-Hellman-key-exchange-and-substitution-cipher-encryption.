import socket

# Function for modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Substitution Cipher (Shift Cipher)
def encrypt(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def decrypt(text, shift):
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

# Receive p and g from server
p, g = map(int, client.recv(1024).decode().split())

# Take user input for private key
private_key = int(input("Client: Enter your private key: "))

# Compute public key
public_key = mod_exp(g, private_key, p)

# Exchange public keys
server_public_key = int(client.recv(1024).decode())
client.send(str(public_key).encode())

# Compute shared secret
shared_secret = mod_exp(server_public_key, private_key, p)
shift_key = shared_secret % 256  # Use as shift value for encryption

print(f"Shared Secret Key: {shared_secret}")

# Encrypt and send message
message = input("Client: Enter a message to send: ")
encrypted_msg = encrypt(message, shift_key)
client.send(encrypted_msg.encode())

# Close connection
client.close()
