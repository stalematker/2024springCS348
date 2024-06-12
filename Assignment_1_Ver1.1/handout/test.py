from oracle import Oracle
oracle = Oracle()

# tester
IV = "0x920f636487b871a8"
Cipher = "0x1234567890abcdef"
result = oracle.dec_oracle(IV, Cipher)
decoded_bytes = bytes.fromhex(result[2:])
decoded_text = decoded_bytes.decode('utf-8')
print(decoded_text)