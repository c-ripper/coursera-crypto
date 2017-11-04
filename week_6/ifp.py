from gmpy2 import invert, mpz, isqrt, mul, is_square, gcd, powmod


#########################################################
# Programming Assignment for Week 6 - Solve IFP for RSA #
#########################################################
N1 = mpz('179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581')
N2 = mpz('648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877')
N3 = mpz('720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929')
C4 = mpz('22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540');


def factor(n, k=1):
    nk_sqrt = isqrt(n * k)
    for i in range(1, 2 ** 20):
        a = nk_sqrt + i
        t = a * a - n * k
        if is_square(t):
            x = isqrt(t)
            p = gcd(n, a - x)
            q = gcd(n, a + x)
            if mul(p, q) == n:
                return [p, q]


p1, q1 = factor(N1)
print("Challenge 1: ", p1 if p1 < q1 else q1)
p2, q2 = factor(N2)
print("Challenge 2: ", p2 if p2 < q2 else q2)
p3, q3 = factor(N3, 24)
print("Challenge 3: ", p3 if p3 < q3 else q3)
d = invert(65537, N1 - p1 - q1 + 1)
m4 = '{0:x}'.format(powmod(C4, d, N1))
print("Challenge 4: ", bytes.fromhex(m4[m4.rfind('00') + 2:]).decode())