import random
import time

random.seed(67)

def binpower(base,e,mod) :
    result = 1
    base %= mod
    while e:
        if e & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        e >>= 1
    return result

def check_composite(n, a, d, s):
    x = binpower(a, d, n)
    if x == 1 or x == n-1:
        return False
    for r in range(1,s):
        x = (x * x) % n
        if x == n-1 :
            return False
    return True


def MillerRabin_prime_check(n, iter = 5):
    if n < 4:
        return n == 2 or n == 3
    s = 0
    d = n-1
    while d & 1 == 0 :
        d >>= 1
        s += 1
    for i in range(iter) :
        a = 2 + random.randint(0,n-3)
        if check_composite(n, a, d, s):
            return False
    return True

def get_prime(k) :
    while True :
        q = random.getrandbits(k)
        p = 2 * q + 1
        if MillerRabin_prime_check(p, 10) and MillerRabin_prime_check(q, 10) :
            return p

def get_primitive_root(min, max, p):
    while True :
        g = random.randint(min, max)
        if binpower(g, (p-1) // 2, p) != 1 and binpower(g, 2, p) != 1:
            return g
        

if __name__ == '__main__':
    start = 128
    stop = 320
    for prime_len in range(start, stop, 64):
        p_start = time.time()
        p = get_prime(prime_len)
        p_end = time.time()

        g_start = time.time()
        g = get_primitive_root(2, p-2, p)
        g_end = time.time()

        a_start = time.time()
        a = get_prime(prime_len // 2)
        a_end = time.time()

        b_start = time.time()
        b = get_prime(prime_len // 2)
        b_end = time.time()

        A_start = time.time()
        A = binpower(g, a, p)
        A_end = time.time()
        
        B_start = time.time()
        B = binpower(g, b, p)
        B_end = time.time()


        Ab_start = time.time()
        Ab = binpower(A, b, p)
        Ab_end = time.time()

        Ba_start = time.time()
        Ba = binpower(B, a, p)
        Ba_end = time.time()

        print("for k = ", str(prime_len) + ", computation time for p:", p_end - p_start, "g:", g_end - g_start, "a or b:", (a_end - a_start + b_end - b_start) / 2, "A or B:", 
              (A_end - A_start + B_end - B_start) / 2, "shared key:", (Ab_end - Ab_start + Ba_end - Ba_start) / 2)
        
        if Ab == Ba :
            print("Key Exchange Successful")