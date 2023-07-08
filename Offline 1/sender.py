#implement a python sender that sends bytes to receiver using socket
#start code here
import socket
import aes as aes
from diffie_hellman import *

import socket            
 
 
# Create a socket object
sock = socket.socket()        

HOST = '127.0.0.1'
PORT = 12345               
 
# connect to the server on local computer
sock.connect(('127.0.0.1', PORT))

prime_len = 128 
p = get_prime(prime_len)
g = get_primitive_root(2, p-2, p)
a = get_prime(prime_len // 2)
A = binpower(g, a, p)

key_data = str(p)+' '+str(g)+' '+str(A)
sock.sendall(key_data.encode())
print("sent:")
print("p",p,"g",g,"A",A)

# receive data from the server and decoding to get the string.
B = int(sock.recv(1024).decode())
print("received:")
print("B",B)

shared_key = binpower(B, a, p)
print("shared key:")
print(shared_key)

aes_round_keys, key_schedule_time = aes.key_schedule(str(shared_key))

while True:
    # send message
    message = input("Write message: ")
    ciphertext, encryption_time = aes.encrypt(message, aes_round_keys)
    sock.sendall(ciphertext.encode())
    if message == 'END':
        break	
    print("Alice:", message)
    # print("Alice sent ciphertext:", ciphertext)

    # receive message
    recvd_message = sock.recv(1024).decode()
    plaintext, decryption_time = aes.decrypt(recvd_message, aes_round_keys)

    if plaintext == 'END':
        break
    # print("Alice received ciphertext:", recvd_message)
    print("Bob:", plaintext)
print("Chat ended")
sock.close()