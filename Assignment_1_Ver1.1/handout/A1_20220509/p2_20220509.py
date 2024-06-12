import sys
from oracle import Oracle

oracle = Oracle()
IV = "0x1234567890abcdef"
Fciphertext = "0x1234567890abcdef"
plaintext = sys.argv[1:]
plaintext = " ".join(plaintext)
# plaintext = "this is the secret message"
hex_values = ''.join([hex(ord(char))[2:] for char in plaintext])
plaintext_hex = int(hex_values, 16)
blocks = ((len(hex_values))//16) + 1
fin = [Fciphertext]

for i in range(blocks-1, -1, -1):
    if i == blocks-1: block = "0x"+hex_values[i*16:]
    else: block = "0x"+hex_values[i*16:i*16+16]
    if len(block)<18:
        t = "0"+str((18-len(block))//2)
        block = block + t*((18-len(block))//2)
    
    plaintext_hex = int(block, 16)
    IV_hex = int(IV, 16)
    Fciphertext_hex = int(Fciphertext, 16)
    IV = "0x" + format(IV_hex, '016x')
    Fciphertext = "0x" + format(Fciphertext_hex, '016x')
    
    Fplaintext = oracle.dec_oracle(IV, Fciphertext)
    Fplaintext_hex = int(Fplaintext, 16)
    fakeIV_hex = plaintext_hex ^ Fplaintext_hex ^ IV_hex
    fakeIV = hex(fakeIV_hex)
    fin.append(fakeIV)

#tester
    # result = oracle.dec_oracle(fakeIV, Fciphertext)
    # decoded_bytes = bytes.fromhex(result[2:])
    # decoded_text = decoded_bytes.decode('utf-8')
    # print(decoded_text)

    Fciphertext = fakeIV

fin.reverse()
print(" ".join(fin))