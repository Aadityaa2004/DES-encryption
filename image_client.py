import des
import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
from RSA import generate_keypair, encrypt, decrypt
import struct

# Set up server connection details
SERVER_IP = gethostbyname('DE1_SoC')
PORT_NUMBER = 5000
BUFFER_SIZE = 1024
des_key = 'secret_k'
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

# Initialize socket for UDP communication
client_socket = socket(AF_INET, SOCK_DGRAM)
initial_message = 'hello'

# Generate RSA key pair using specified p and q values (provided in Excel)
p, q = 1297169, 1297523
public, private_key = generate_keypair(p, q)
message = ('public_key: %d %d' % (public[0], public[1])).encode()
client_socket.sendto(message, (SERVER_IP, PORT_NUMBER))

# Send DES key after encoding
message = 'des_key'
client_socket.sendto(message.encode(), (SERVER_IP, PORT_NUMBER))

# Encrypt DES key using RSA and store it in des_encoded
# Example placeholder values
des_encoded = [str(encrypt(private_key, char)) for char in des_key]

# Send the RSA-encrypted DES key over UDP
for code in des_encoded:
    client_socket.sendto(code.encode(), (SERVER_IP, PORT_NUMBER))

# Read image file, encrypt it with DES, and prepare for sending
with open(r'penguin.jpg', "rb") as img_file:
    image_data = img_file.read()
img_file.close()

# Encrypt the image using DES, with CBC mode set to False
coder = des.des()
encrypted_image = coder.encrypt(des_key, image_data, cbc=False)

# Convert encrypted image data to a byte array for transmission
encrypted_byte_array = bytearray()
for byte in encrypted_image:
    encrypted_byte_array += bytes([ord(byte)])

# Send encrypted image data to server
client_socket.sendto(bytes(encrypted_byte_array), (SERVER_IP, PORT_NUMBER))
print('encrypted image sent!')
