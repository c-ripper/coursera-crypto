from gmpy2 import f_mod, invert, mpz, powmod
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer


###################################################################
# Programming Assignment for Week 5 - Solve DLP for G^X = H mod P #
###################################################################
G = mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')
H = mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')
P = mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')
B = mpz(2 ** 20)


def compute_x1(seq):
    hash_map = {}
    for x1 in seq:
        left = f_mod(H * invert(powmod(G, x1, P), P), P)
        hash_map[left] = x1
    return hash_map


def find_x0(seq):
    for x0 in seq:
        right = powmod(powmod(G, B, P), x0, P)
        if right in lookup_map:
            x1 = lookup_map[right]
            x = f_mod(x0 * B + x1, P)
            print('Found x = {}'.format(x))
            break


# splits a in n ~even subsets
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


print('Pre-computing table [H/(G^x1) mod P, x1]...')
t0 = timer()
with Pool() as pool:
    hash_maps = pool.map(compute_x1, list(split(range(0, B), cpu_count())))
t1 = timer()
print("Time spent: {0:.3f}s".format(t1 - t0))
lookup_map = {}
# merge n hash maps into one
for hm in hash_maps:
    for key in hm.keys():
        lookup_map[key] = hm[key]
print('Searching for x0, so that: H/(G^x1) mod P = (G^B)^x0 mod P')
with Pool() as pool:
    pool.map(find_x0, list(split(range(0, B), cpu_count())))
t2 = timer()
print("Total time spent: {0:.3f}s".format(t2 - t0))
