from state import *

# Hexadicimal to Binary Conversion
def hex2binary(s):
    mp = {'0': "0000", '1': "0001", '2': "0010", '3': "0011",
          '4': "0100", '5': "0101", '6': "0110", '7': "0111",
          '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
          'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}

    bin = ""
    i = 0
    while i < len(s):
        bin += mp[s[i]]
        i += 1
    return bin

# Binary to Hexadecimal Conversion
def binary2hex(s):
    mp = {"0000": '0', "0001": '1', "0010": '2', "0011": '3',
          "0100": '4', "0101": '5', "0110": '6', "0111": '7',
          "1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
          "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'}

    hex = ""
    i = 0
    while i < len(s):
        ch = s[i:i+4]
        hex += mp[ch]
        i += 4
    return hex

# Binary to Decimal Conversion
def binary2decimal(binary):
    decimal, i = 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

# Decimal to Binary Conversion
def decimal2binary(num):
    res = bin(num).replace("0b", "")
    if len(res) % 4 != 0:
        div = len(res) // 4
        counter = (4 * (div + 1)) - len(res)
        i = 0
        while i < counter:
            res = '0' + res
            i += 1
    return res

# Permutation Function
def permute(k, arr, n):
    permute = ""
    i = 0
    while i < n:
        permute += k[arr[i] - 1]
        i += 1
    return permute

# Left Shift Function
def left_shift(k, nth_shifts):
    s = ""
    count = 0
    while count < nth_shifts:
        j = 1
        while j < len(k):
            s += k[j]
            j += 1
        s += k[0]
        k = s
        s = ""
        count += 1
    return k

# XOR Function
def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans

# Encrypt Function
def encrypt(pt, roundKeyBinary, roundKey):
    # Convert Plaintext to Binary
    pt = hex2binary(pt)

    # Initial permute
    pt = permute(pt, initial_perm, 64)
    print("After initial permute", binary2hex(pt))

    # Splitting to LPT and RPT
    left = pt[0:32]
    right = pt[32:64]
    
    # Print header for columns
    print(f"{'Round':<8}{'Left':<15}{'Right':<15}{'Round Key':<48}")
    print("=" * 52)  # Divider for better readability

    for i in range(0, 16):
        # Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, exp_d, 48)

        # XOR RTP with RoundKey
        xor_x = xor(right_expanded, roundKeyBinary[i])

        # S-Box
        sbox_str = ""
        for j in range(0, 8):
            row = binary2decimal(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = binary2decimal(
                int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + decimal2binary(val)

        # P-box
        sbox_str = permute(sbox_str, per, 32)

        # XOR LTP and S-Box Output
        result = xor(left, sbox_str)
        left = result

        # Swap
        if (i != 15):
            left, right = right, left

        # Print the round details in formatted columns
        print(f"{i + 1:<8}{binary2hex(left):<15}{binary2hex(right):<15}{roundKey[i]:<48}")
    
    # Combine left and right after the 16 rounds
    combined = left + right
    
    # Apply the final permutation
    cipherText = permute(combined, final_perm, 64)

    return cipherText  # Make sure to return the final binary ciphertext
