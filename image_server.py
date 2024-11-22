from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import re
import struct
from RSA import decrypt
import des

# Define server's port number and buffer size
PORT_NUMBER = 5000
SIZE = 8192

# Set up host using IP or hostname of the DE1 SoC server
hostName = gethostbyname('DE1_SoC')

# Initialize UDP socket and bind to the server's hostname and port
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((hostName, PORT_NUMBER))

print ("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key = ""
des_key = ""

# Continuously listen for incoming messages from clients
while True:
        (data,addr) = server_socket.recvfrom(SIZE)
        data=data.decode()
        if data.find('public_key')!=-1: #client has sent their public key\
            ###################################your code goes here#####################################
            #retrieve public key and private key from the received message (message is a string!)
            k = data.split()
            public_key_e = k[1]
            public_key_n = k[2]
            client_public_key_e = (int(public_key_e), int(public_key_n))
            print ('public key is : %d, %d'%client_public_key_e)
        elif data.find('des_key')!=-1: #client has sent their DES key
            ###################################your code goes here####################
            #read the next 8 bytes for the DES key by running (data,addr) = server_socket.recvfrom(SIZE) 8 times and then decrypting with RSA
            # use a for loop for that, refer to image_server.py for a reference
            des_key = ""
            for i in range(8):
                (data,addr) = server_socket.recvfrom(SIZE)
                # Convert the decrypted number to a character
                decrypted_char = decrypt(client_public_key_e, int(data))
                des_key += decrypted_char
            print ('DES key is :' + des_key)
            #now we will receive the image from the client
            (data,addr) = server_socket.recvfrom(SIZE)
            #decrypt the image
            ###################################your code goes here####################
            #the received encoded image is in data
            #perform des decryption using des.py
            decoder=des.des()
            #the final output should be saved in a byte array called rr_byte
            
            rr=decoder.decrypt(des_key, data, cbc=False)
            rr_byte=bytearray()
            for x in rr:
                 rr_byte+=bytes([ord(x)])
            #write to file to make sure it is okay
            file2=open(r'penguin_decrypted.jpg',"wb") 
            file2.write(bytes(rr_byte))
            file2.close()
            print ('decypting image completed')
            break
        else:
            continue