"""
<<<<<References>>>>>
https://sites.psu.edu/gottiparthyanirudh/writing-sample-3/
https://gist.github.com/djego/97db0d1bc3d16a9dcb9bab0930d277ff
https://brilliant.org/problems/factoring-a-large-number/
https://brilliant.org/wiki/modular-arithmetic/#modular-arithmetic-multiplicative-inverses
https://brilliant.org/wiki/euclidean-algorithm/
https://www.geeksforgeeks.org/rsa-algorithm-cryptography/
https://www.educative.io/edpresso/what-is-the-rsa-algorithm
https://www.youtube.com/watch?v=shaQZg8bqUM
https://www.sciencedirect.com/topics/computer-science/public-key-algorithm

"""

import random

'''Euclid Algorithm for determining the greatest common factor'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''Extended Euclidean Algorithm for finding the modulo inverse'''
def egcd(exp, phi):
    x,y, u,v = 0,1, 1,0
    while exp != 0:
        q, r = phi//exp, phi%exp
        m, n = x-u*q, y-v*q
        phi, exp, x,y, u,v = exp,r, u,v, m,n
    gcd = phi
    return gcd, x, y

def modinv(exp, phi):
    gcd, x, y = egcd(exp, phi)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % phi

'''Tests to see if a number is prime'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

"""************Key generation part*************"""

def generate_keypair(p, q):
    # confirm the pairs of numbers are prime
    if not( is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # calculate the product of the two prime numbers
    n = p * q
    #print(n.bit_length())

    # calculate the totient function, phi(n)
    phi = (p-1) * (q-1)

    # Choose an integer exp such that exp and phi(n) are coprime
    exp = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are co-prime
    g = gcd(exp, phi)
    while g!= 1:
        e = random.randrange(1, phi)
        g = gcd(exp, phi)

    # Use the extended Euclid's Algorithm to generate the private key
    #print(phi, g)
    d = modinv(exp, phi)

    # Return public and private keypair
    #Public key is (exp, n) and private key is (d, n)
    return ((exp, n), (d, n))

"""***************RSA Encryption***************"""
def encrypt(keypair, plaintext):
    # Upack the key into it's components
    key, n = keypair
    # Represent the plain text (P) as number using P^key mod n
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


"""***************RSA Decryption***************"""
def decrypt(keypair, ciphertext):
    # Unpack the key into its components
    key, n = keypair
    # Generate the plaintext based on the ciphertext 
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("RSA Encrypter/Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public ," . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))




    



