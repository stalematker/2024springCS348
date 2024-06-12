import sys
from oracle import Oracle

oracle = Oracle()

a = sys.argv[1]
b = sys.argv[2]
IV = int(a, 16)
ciphertext = int(b, 16)

result_iv = ""
results = []

for i in range(1, 9):
    temp_iv = 0
    for j in range(i-1):
        temp_iv += (results[j]^i) << (8*j)
    #ex: temp_iv = 1122334455007788

    for guess in range(256):
        modified_iv = temp_iv + (guess << 8*(i-1))
        modified_iv_hex = format(modified_iv, '016x')
        if oracle.pad_oracle("0x"+modified_iv_hex, hex(ciphertext)) == b'1':
            result = guess ^ i
            results.append(result)
            formatted_string = format(result, '02x')
            result_iv = formatted_string + result_iv
            break
    #guess and use oracle

iv_plaintext = int(result_iv, 16)
plaintext = hex(iv_plaintext ^ IV)[2:]
decoded_bytes = bytes.fromhex(plaintext)
decoded_text = decoded_bytes.decode('utf-8')
print(decoded_text)
#decode the result to plaintext