from Crypto.Cipher import AES, XOR
import math


##########################################################################
# Programming Assignment for Week 2 - Decrypt AES CBC/CTR using ECB mode #
##########################################################################
CBC_KEY = '140b41b22a29beb4061bda66b6747e14'
CBC_CT_1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
CBC_CT_2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
CTR_KEY = '36f18357be4dbd77f050515c73fcf9f2'
CTR_CT_1 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
CTR_CT_2 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
BLOCK_SIZE = 16


def xor(s1, s2):
    return XOR.new(s1).encrypt(s2)


def aes_decrypt_cbc(s, k):
    cipher = AES.new(bytes.fromhex(k), AES.MODE_ECB)
    iv = bytes.fromhex(s[:16 * 2])
    ct = bytes.fromhex(s[16 * 2:])
    dec_m = b''
    for i in range(0, len(ct) // BLOCK_SIZE):
        enc_block = ct[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        dec_block = xor(cipher.decrypt(enc_block), iv if i == 0 else ct[(i - 1) * BLOCK_SIZE:i * BLOCK_SIZE])
        dec_m += dec_block
    return dec_m[:len(dec_m) - dec_m[-1]]


def aes_decrypt_ctr(s, k):
    cipher = AES.new(bytes.fromhex(k), AES.MODE_ECB)
    iv = bytes.fromhex(s[:16 * 2])
    ct = bytes.fromhex(s[16 * 2:])
    dec_m = b''
    for i in range(0, math.ceil(len(ct) / BLOCK_SIZE)):
        enc_block = ct[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        iv_ctr = int.from_bytes(iv, 'big') + i
        dec_block = xor(cipher.encrypt(iv_ctr.to_bytes(BLOCK_SIZE, 'big')), enc_block)
        dec_m += dec_block
    return dec_m


for ct in [CBC_CT_1, CBC_CT_2]:
    print(aes_decrypt_cbc(ct, CBC_KEY).decode())
for ct in [CTR_CT_1, CTR_CT_2]:
    print(aes_decrypt_ctr(ct, CTR_KEY).decode())
