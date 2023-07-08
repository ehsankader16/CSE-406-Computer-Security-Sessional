import time
from utils import *

def key_schedule(given_key):
    key = given_key.ljust(16,'0')
    if(len(key) < 16):
        key = key + '0' * (16-len(key))
    elif(len(key) > 16):
        key = key[:16]

    init_key_matrix = convert_to_matrix(key)
    # print("key")
    # print_matrix_in_hex(init_key_matrix)

    key_schedule_start = time.time()
    round_key_matrix = []
    round_key_matrix.append(init_key_matrix)
    #print("round 0")
    #print_matrix_in_hex(round_key_matrix[0])
    for round in range(1,11) :
        old_word_matrix = round_key_matrix[round-1]
        old_word_matrix = transpose_matrix(old_word_matrix)
        #print("old word matrix",round)
        # print_matrix_in_hex(old_word_matrix)
        g_word = g_func(old_word_matrix[3], round)
        # print("g word",round)
        # print_list_in_hex(g_word)
        new_word_matrix = [[0 for i in range(4)] for j in range(4)]
        new_word_matrix[0] = xor_word(old_word_matrix[0], g_word)
        for i in range(1,4) :
            new_word_matrix[i] = xor_word(old_word_matrix[i], new_word_matrix[i-1])
        round_key_matrix.append(transpose_matrix(new_word_matrix))
        # print("round", round)
        # print_matrix_in_hex(round_key_matrix[round])
    key_schedule_end = time.time()
    return round_key_matrix, key_schedule_end - key_schedule_start

def encrypt_block(data, round_key_matrix):
    data_matrix = convert_to_matrix(data)
    # print("data")
    # print_matrix_in_hex(data_matrix)
    #round 0
    state_matrix = xor_matrix(data_matrix, round_key_matrix[0])
    # print("after round 0 in encryption")
    # print_matrix_in_hex(state_matrix)

    #round 1-9
    for round in range(1,10) :
        state_matrix = sub_bytes(state_matrix)
        state_matrix = shift_matrix_left(state_matrix)
        state_matrix = mix_columns(state_matrix)
        state_matrix =xor_matrix(state_matrix, round_key_matrix[round])
        # print("after round",round,"in encryption"")
        # print_matrix_in_hex(state_matrix)

    #round 10
    state_matrix = sub_bytes(state_matrix)
    state_matrix = shift_matrix_left(state_matrix)
    state_matrix = xor_matrix(state_matrix,round_key_matrix[10])
    # print("after round 10 in encryption")
    # print_matrix_in_hex(state_matrix)

    cipher_text = convert_to_string(state_matrix)
    return cipher_text

def decrypt_block(ciphertext, round_key_matrix):
    state_matrix = convert_to_matrix(ciphertext)
    # print("ciphertext")
    # print_matrix_in_hex(state_matrix)

    #round 0
    state_matrix = xor_matrix(state_matrix,round_key_matrix[10])
    state_matrix = shift_matrix_right(state_matrix)
    state_matrix = inv_sub_bytes(state_matrix)
    # print("after round 0 in decryption")
    # print_matrix_in_hex(state_matrix)

    #round 1-9
    for round in range(1,10) :
        state_matrix = xor_matrix(state_matrix, round_key_matrix[10-round])
        state_matrix = inv_mix_columns(state_matrix)
        state_matrix = shift_matrix_right(state_matrix)
        state_matrix = inv_sub_bytes(state_matrix)
        # print("after round",round,"in decryption")
        # print_matrix_in_hex(state_matrix)

    #round 10
    state_matrix =xor_matrix(state_matrix, round_key_matrix[0])
    # print("after round 10 in decryption")
    # print_matrix_in_hex(state_matrix)
    plain_text = convert_to_string(state_matrix)
    return plain_text
    
def encrypt(plaintext, round_key_matrix):
    blocks = []
    for i in range(0, len(plaintext), 16):
        blocks.append(plaintext[i:i+16])
    #encrypt each block
    ciphertext = ""
    encryption_start = time.time()
    for block in blocks:
        ciphertext += encrypt_block(block, round_key_matrix)
    encryption_end = time.time()

    

    return ciphertext, encryption_end - encryption_start


def decrypt(ciphertext, round_key_matrix):
    blocks = []
    for i in range(0, len(ciphertext), 16):
        blocks.append(ciphertext[i:i+16])
    #decrypt each block
    plaintext = ""
    decryption_start = time.time()
    for block in blocks:
        plaintext += decrypt_block(block, round_key_matrix)
    decryption_end = time.time()

    return plaintext, decryption_end - decryption_start

if __name__ == '__main__':
    input_text = "Aungon" #"Two One Nine Two abcd"
    # input_text = input("Enter the text to encrypt: ")
    print("Input plain Text:")
    print("In ASCII:", input_text)
    print("In Hex:", input_text.encode("utf-8").hex(), "\n")

    key = "BUET CSE18 Batch" # "Thats my Kung Fu"
    #key = input("Enter the key: ")
    print("Key:")
    print("In ASCII:", key)
    print("In Hex:", key.encode("utf-8").hex(), "\n")

    round_keys, key_schedule_time = key_schedule(key)
    ciphertext, encryption_time = encrypt(input_text, round_keys)

    print("Cipher Text:")
    print("In ASCII:", ciphertext)
    print("In Hex:", ciphertext.encode("utf-8").hex(), "\n")

    plaintext, decryption_time = decrypt(ciphertext, round_keys)
    
    print("Deciphered Text:")
    print("In ASCII:", plaintext)
    print("In Hex:", plaintext.encode("utf-8").hex(), "\n")

    print("Execution Time details")
    print("Key Scheduling:", key_schedule_time, "seconds")
    print("Encryption Time:", encryption_time, "seconds")
    print("Decryption Time:", decryption_time, "seconds")