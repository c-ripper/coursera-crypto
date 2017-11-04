import os
from Crypto.Hash import SHA256

###################################################
# Programming Assignment for Week 3 - File Hasher #
###################################################
BLOCK_SIZE = 1024
HASH_SIZE = 32
FNAME = '~/dev/coursera/crypto/week_3/6.1.intro.mp4_download'

try:
    f = open(FNAME, 'rb')
    f_size = os.stat(FNAME).st_size
    k = f_size % BLOCK_SIZE
    i = f_size // BLOCK_SIZE
    h = b''
    for j in reversed(range(i + 1)):
        f.seek(j * BLOCK_SIZE)
        is_last_block = i == j
        bytes_to_read = k if is_last_block else BLOCK_SIZE
        read_bytes = f.read(bytes_to_read)
        bytes_to_hash = read_bytes + (b'' if is_last_block else bytes.fromhex(h.hexdigest()))
        h = SHA256.new()
        h.update(bytes_to_hash)
    print(h.hexdigest())
finally:
    f.close()
