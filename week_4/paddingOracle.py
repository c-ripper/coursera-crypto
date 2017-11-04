from Crypto.Cipher import XOR
from urllib3 import HTTPConnectionPool
from timeit import default_timer as timer
from multiprocessing import Pool


#########################################################################################
# Programming Assignment for Week 4 - Crack CBC cipher text using padding oracle attack #
#########################################################################################
HOST = 'crypto-class.appspot.com'
CIPHER_TEXT = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
DICTIONARY = b' eothasinrdluymwfgcbpkvjqxzEOTHASINRDLUYMWFGCBPKVJQXZ,.;:-?'
BLOCK_SIZE = 16
TOTAL_BLOCKS = len(CIPHER_TEXT) // (BLOCK_SIZE * 2) - 1


def zero_pad(val, size):
    return '\x00' * (size - len(val)) + val


def xor(s1, s2):
    return XOR.new(s1).encrypt(s2)


class PaddingOracle:
    def __init__(self, er_value):
        self.conn_pool = HTTPConnectionPool(HOST)
        self.pad = [chr(i) * i for i in range(BLOCK_SIZE + 1)]
        self.pad_align = [zero_pad(chr(i) * i, BLOCK_SIZE) for i in range(BLOCK_SIZE + 1)]
        self.iv = bytes.fromhex(er_value[: 2 * BLOCK_SIZE])
        self.cipher = bytes.fromhex(er_value[2 * BLOCK_SIZE:])

    def get_block(self, index):
        return self.cipher[BLOCK_SIZE * index: BLOCK_SIZE * (index + 1)]

    def replace_block(self, index, new_block):
        before = self.cipher[:BLOCK_SIZE * index]
        after = self.cipher[BLOCK_SIZE * (index + 1):]
        return before + new_block + after

    def query(self, cipher_text):
        response = self.conn_pool.request('GET', '/po?er=' + cipher_text)
        return response.status


def solve_block(block_idx):
    oracle = PaddingOracle(CIPHER_TEXT[: 32 * (block_idx + 3)])
    plain = ''
    for i in reversed(range(BLOCK_SIZE)):
        for g in derive_dict(block_idx, plain):
            if should_use_known_pad(block_idx, plain):
                plain = plain[0] + plain
                print('M{0}[{1}]: {2}'.format(block_idx + 1, i, plain[-1]))
                break
            pad_mask = oracle.pad_align[BLOCK_SIZE - i]
            xored_padded_mask = xor(zero_pad(chr(g) + plain, BLOCK_SIZE), pad_mask)
            if block_idx == -1:
                new_iv = xor(xored_padded_mask, oracle.iv)
                query_str = new_iv + oracle.cipher
            else:
                new_cipher_block = xor(xored_padded_mask, oracle.get_block(block_idx))
                query_str = oracle.iv + oracle.replace_block(block_idx, new_cipher_block)
            status = oracle.query(query_str.hex())
            if status == 404 or status == 200:
                plain = chr(g) + plain
                print('M{0}[{1}]: {2}'.format(block_idx + 1, i, chr(g)))
                break
            if g == 255:
                print('error: could not guess a char. Try using another dictionary.')
                sys.exit()
    print("Solved block {0}: ".format(block_idx + 1), plain)
    return plain


def is_last_block(idx):
    return idx == TOTAL_BLOCKS - 2


def should_use_known_pad(block_idx, known_plain):
    return is_last_block(block_idx) and known_plain != '' and len(known_plain) < ord(known_plain[-1])


# mapping function which will set special dictionary for last block, so that padding bytes are tried first
def derive_dict(block_idx, known_plain):
    if is_last_block(block_idx):
        if known_plain == '' or len(known_plain) < ord(known_plain[-1]):
            return bytearray(range(2, BLOCK_SIZE + 1)) + DICTIONARY
    return DICTIONARY


# using multiple threads to solve all blocks in parallel
print("Started padding oracle attack...")
t0 = timer()
with Pool() as p:
    block_solutions = p.map(solve_block, list(range(-1, TOTAL_BLOCKS - 1)))
t1 = timer()
print()
print("Found solution: {0}".format(''.join(block_solutions)))
print("Total time spent:\t\t {0:.2f}s".format(t1 - t0))
