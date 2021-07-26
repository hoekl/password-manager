import random
import os
currentDIR = os.path.dirname(__file__)  # getting the path to the program file. All file operations are relative to this path
covertext_path = currentDIR + '//configuration//covertext.txt'              # declare path of covertext file and hidden message file


def one_time_pad(array_length):
    ''' This function creates a list of integers in range 0-255 of the same length as the amount of bytes in the secret message.
        Each integer in int_array is XOR'ed bitwise with each character in secret message to encrypt or decrypt'''
    int_array = []
    random.seed(67)
    for i in range(array_length):
        num = random.randrange(0,255)
        int_array.append(num)
        i += 1
    return int_array

def encrypt_xor(otp_array, byte_array):
    i = 0
    encrypted_ints = []
    for byte in byte_array:
        result_xor = byte^otp_array[i]  # doing bitwise XOR between each byte of secret message and otp_array
        encrypted_ints.append(result_xor)
        i += 1

    return encrypted_ints

def decrypt_xor(otp_array, encrypted_msg):
    i = 0
    decrypted_ints = []
    for byte in encrypted_msg:
        reversed_xor = byte^otp_array[i]    # doing bitwise XOR between each byte of secret message and otp_array
        decrypted_ints.append(reversed_xor)
        i += 1

    return decrypted_ints

def convert_to_binary(encrypted_msg):
    ''' Preparing the data to be merged with the cover text by formatting the binary representation
        of the secret message to strings of binary with 8 bits per byte.
        Then splitting each byte into a list and appending to list of lists binary_split_list.
        This list is then flattened so that all bits are single items in the list flat_binary_split_list. '''
    binary_list = []
    binary_split_list = []
    for digit in encrypted_msg:
        binary_digit = format(digit, '008b')
        binary_list.append(binary_digit)

    for item in binary_list:
        list_bin = list(item)
        binary_split_list.append(list_bin)
    flat_binary_split_list = [bit for byte in binary_split_list for bit in byte]
    return flat_binary_split_list

def get_cover_text():
    with open(covertext_path, 'r', encoding='latin-1') as f:
        read = f.read()
        covertext = read.split()
    return covertext

def merge_cover_with_secret(covertext, binary_list):
    merged_list = []
    if len(binary_list) > len(covertext):   # one word of cover text is needed for each bit of the secret message. If there are more bits than words it's not possible to encode the whole message
        print('\nMessage too long. Shorten message to encode or supply longer cover text')
        raise SystemExit(0)

    for bit in binary_list:                 # Merging cover text and secret message by appending a word of cover text, followed by a '0' or a '1' in turn until there are no more bits to encode
        cover_word = covertext.pop(0)
        merged_list.append(cover_word)
        if bit == '0':
            merged_list.append(" ")         # 0 is represented by a space in latin-1 encoding. (Unicode integer code point:32, hex code point: x20)
        if bit == '1':
            merged_list.append("\xA0")      # 1 is represented by a nbsp in latin-1 encoding. (Unicode integer code point:32, hex code point: xA0)
    return merged_list

def write_message_to_file(merged_message):
    try:
        with open(secret_message_path, 'w', encoding='latin-1') as f:
            f.writelines(merged_message)
        print('\nMessage successfully encoded')
    except:
        print('\nUnable to write to file. Ensure all charcters in secret message are in latin-1 encoding')

def decode_message(msg):
    listmsg = list(msg)
    bit_list = []
    for character in listmsg:
        if character == ' ' or character == '\xa0':   # going through all characters of the file and extracting only spaces and non breaking spaces (nbsp)
            bit_list.append(character)

    return bit_list

def convert_to_bits(bit_list):
    ''' Converting from custom encoding scheme of space and nbsp to binary '''
    temp_bit_list = []
    for bit in bit_list:
        if bit == ' ':
            temp_bit_list.append('0')
        if bit == '\xa0':
            temp_bit_list.append('1')
    return temp_bit_list

def split_to_bytes(byte_list, byte_str_list):
    ''' Splitting into 8 bits per byte '''
    counter = 0
    byte = []
    while byte_str_list:
        bit = byte_str_list.pop(0)
        byte.append(bit)
        counter += 1
        if counter % 8 == 0:
            byte_list.append(byte)
            byte = []
    return byte_list

def string_bits_to_binary(byte_list):
    ''' Converting from string of 0's and 1's to binary '''
    string_list = []
    for byte in byte_list:
        byte_str = "".join(byte)
        string_list.append([byte_str])
    return string_list

def binary_to_int(binary_list):
    ''' Convert binary bytes to integers to allow character look up using Unicode integer code point '''
    int_list = []
    for byte in binary_list:
        int_val = int(byte[0], base=2)
        int_list.append(int_val)
    return int_list

def int_to_characters(decoded_message):
    ''' Converting from Unicode integer code point to character and convert to string '''
    char_list = [chr(byte) for byte in decoded_message]
    str_message = ''.join(char_list)
    return str_message

if __name__ == "__main__":
    pass

