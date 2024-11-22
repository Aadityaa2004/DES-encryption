from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import re
from RSA import decrypt
PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( 'DE1_SoC' )
#hostName = gethostbyname( 'DESKTOP-A30LB1P' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key=''
while True:
        (data,addr) = mySocket.recvfrom(SIZE)
        data=data.decode()
        if data.find('public_key')!=-1: #client has sent their public key\
            ###################################your code goes here#####################################
            # Extract e and n from the message format "public_key: e n"
            key_parts = data.split(': ')[1].split(' ')
            public_key_e = int(key_parts[0])
            public_key_n = int(key_parts[1])
            print ('public key is : %d, %d'%(public_key_e,public_key_n))
        else:
            cipher=int(data)
            ###################################your code goes here#####################################
            # Create public key tuple for decryption
            public_key = (public_key_e, public_key_n)
            data_decoded = decrypt(public_key, cipher)
            print (str(cipher)+':'+str(data_decoded))
                #python2: print data ,
sys.ext()
#What could I be doing wrong?

