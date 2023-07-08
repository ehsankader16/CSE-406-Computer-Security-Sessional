from helper_data import *

def convert_to_matrix(text):
    text = text.ljust(16, '\0')
    text_matrix = []
    for i in range(4):
        row = []
        for j in range(i,len(text),4):
            row.append(ord(text[j]))     
        text_matrix.append(row)
    return text_matrix

def convert_to_string(matrix):
    text = ""
    for i in range(4):
        for j in range(4):
            if(matrix[j][i] == 0):
                break
            text += chr(matrix[j][i])
    return text

def transpose_matrix(matrix):
    new_matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(matrix[j][i])
        new_matrix.append(row)
    return new_matrix

def sub_bytes(word_matrix):
    for i in range(4):
        for j in range(4):
            word_matrix[i][j] = Sbox[word_matrix[i][j]]
    return word_matrix

def inv_sub_bytes(word_matrix):
    for i in range(4):
        for j in range(4):
            word_matrix[i][j] = InvSbox[word_matrix[i][j]]
    return word_matrix

def shift_left(word, n):
    word = word[n:] + word[:n]
    return word

def shift_matrix_left(word_matrix):
    for i in range(4):
        word_matrix[i] = shift_left(word_matrix[i], i)
    return word_matrix

def shift_right(word, n):
    word = word[-n:] + word[:-n]
    return word

def shift_matrix_right(word_matrix):
    for i in range(4):
        word_matrix[i] = shift_right(word_matrix[i], i)
    return word_matrix

def xor_word(word1, word2):
    new_word = []
    for i in range(4):
        new_word.append(word1[i]^word2[i])
    return new_word

def xor_matrix(data_matrix, key_matrix):
    for i in range(4):
        data_matrix[i] = xor_word(data_matrix[i], key_matrix[i]) #hex(int(data_matrix[i][j],16) ^ int(key_matrix[i][j],16))
    return data_matrix

def g_func(old_word, n):
    new_word = shift_left(old_word, 1)
    #print("new word",new_word)
    for i in range(4):
        new_word[i] = Sbox[new_word[i]]
    #print("new word",new_word)
    #print("round const",RoundConst[n])
    new_word = xor_word(new_word,RoundConst[n])
    return new_word


def mix_columns(state_matrix):
    AES_MOD = BitVector(bitstring='100011011')
    new_state_matrix =  [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state_matrix[i][j] ^= int(Mixer[i][k].gf_multiply_modular(BitVector(intVal=state_matrix[k][j]),AES_MOD,8))
    return new_state_matrix

def inv_mix_columns(state_matrix):
    AES_MOD = BitVector(bitstring='100011011')
    new_state_matrix =  [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state_matrix[i][j] ^= int(InvMixer[i][k].gf_multiply_modular(BitVector(intVal=state_matrix[k][j]),AES_MOD,8))
    return new_state_matrix

def print_list_in_hex(list):
    for j in range(4):
        print(hex(list[j]),end=" ")
    print()


def print_matrix_in_hex(matrix):
    for i in range(4):
        print_list_in_hex(matrix[i])