#implement a python sender that sends bytes to receiver using socket
#start code here
import socket
import aes as aes
from diffie_hellman import *			

prime_len = 128
# next create a socket object
sock = socket.socket()		
# print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
sock.bind(('', port))		
# print ("socket binded to %s" %(port))

# put the socket into listening mode
sock.listen(5)
print ("socket is listening")

client, addr = sock.accept()

rcvd_keys_data = client.recv(1024).decode()
rcvd_keys_data = rcvd_keys_data.split()
p, g, A = int(rcvd_keys_data[0]), int(rcvd_keys_data[1]), int(rcvd_keys_data[2])
print("received:")
print("p",p,"g",g,"A",A)

b = get_prime(prime_len//2)
B = binpower(g, b, p)
client.sendall(str(B).encode())
print("sent:")
print("B",B)

shared_key = binpower(A, b, p)
print("shared key:")
print(shared_key)

aes_round_keys, key_schedule_time = aes.key_schedule(str(shared_key))

while True:
    # receive message
    recvd_message = client.recv(1024).decode()
    plaintext, decryption_time = aes.decrypt(recvd_message, aes_round_keys)
    print("plaintext"+plaintext+"xyz")
    if plaintext == 'END':
        break

    # print("Bob received ciphertext:", recvd_message)
    print("From Alice:", plaintext)
    
    #send message
    message = input("Write message: ")
    ciphertext, encryption_time = aes.encrypt(message, aes_round_keys)

    client.sendall(ciphertext.encode())
    if message == 'END':
        break
    print("Bob:", message)
    # print("Bob sent ciphertext:", ciphertext)

print("Chat ended")
client.close()
sock.close()


