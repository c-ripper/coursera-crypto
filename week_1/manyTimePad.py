from itertools import permutations
from collections import Counter


############################################################################
# Programming Assignment for Week 1 - Crack encryption using many time pad #
############################################################################
def is_alpha(b):
    return b | 32 in range(ord('a'), ord('z'))


cipher_texts = [bytes.fromhex(s.strip()) for s in open('ciphers.txt')]
key = bytearray()
for i in range(len(cipher_texts[-1])):
    key_i_probe = list(c1[i] ^ 32 for c1, c2 in permutations(cipher_texts, 2) if is_alpha(c1[i] ^ c2[i]))
    key.append(Counter(key_i_probe).most_common(1)[0][0])
print(''.join(chr(cipher_texts[-1][i] ^ key[i]) for i in range(len(cipher_texts[-1]))))