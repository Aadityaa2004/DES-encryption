import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
from RSA import generate_keypair,encrypt,decrypt

SERVER_IP    = gethostbyname( 'DE1_SoC' )
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
message='hello'

#first generate the keypair
#get these two numbers from the excel file
p=1297273
q=1297651
###################################your code goes here#####################################
#generate public and private key from the p and q values
#hint: use generate_keypair() function from RSA.py
public, private = generate_keypair(p, q)

print("Generated public key:" + str(public))

message=('public_key: %d %d' % (public[0], public[1]))
mySocket.sendto(message.encode(),(SERVER_IP,PORT_NUMBER))
while True:
        message=raw_input() if sys.version_info[0] < 3 else input()
        message.join('\n')
        ###################################your code goes here#####################################
        #message is a string input received from the user, encrypt it with RSA character by character and save in message_encoded
        #message encoded is a list of integer ciphertext values in string format e.g. ['23131','352135','54213513']
        #hint: encrypt each character in message using RSA and store in message_encoded
        message_encoded = []
        for char in message:
            # Encrypt each character using the public key
            cipher = encrypt(private, char)
            # Convert to string and append to message_encoded
            message_encoded.append(str(cipher))
        [mySocket.sendto(code.encode(),(SERVER_IP,PORT_NUMBER)) for code in message_encoded] # do not change [sends message through socket]

        print("Encrypting message: {message}")
        print("Encrypted message: {message_encoded}")
sys.exit()
