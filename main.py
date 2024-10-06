from state import *
from config import *

roundKey = [] # Round Key
roundKeyBinary = [] # Round Key Binary

pt = input("Input 16 karakter dari 1-9 | A-F: ")
key = input("Input key 16 karakter dari 1-9 | A-F: ")

# Key Process
key = hex2binary(key)
key = permute(key, keyp, 56)
left = key[0:28]
right = key[28:56]

i = 0
while i < 16:
    # Left Shift
    left = left_shift(left, shift_table[i])
    right = left_shift(right, shift_table[i])

    # Combine
    combined_string = left + right

    # Compress to 48-bit
    round_key = permute(combined_string, key_comp, 48)

    roundKeyBinary.append(round_key)
    roundKey.append(binary2hex(round_key))
    
    i += 1

# Encryption
print("Encryption:")
binaryCipher = encrypt(pt, roundKeyBinary, roundKey)  # Get the binary cipher text
cipherText = binary2hex(binaryCipher)  # Convert the binary cipher text to hexadecimal
print("Cipher Text: ", cipherText)

# Decryption
print("\nDecryption:")
rkb_rev = roundKeyBinary[::-1]
rk_rev = roundKey[::-1]
text = binary2hex(encrypt(cipherText, rkb_rev, rk_rev))
print("Plain Text: ", text)