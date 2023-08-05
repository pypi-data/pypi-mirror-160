import random


def isPrime(n):
    """Checks for Prime numbers"""
    # Corner case
    if n <= 1:
        return False

    # check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False

    return True


# Function to print primes
def printPrime(n):
    """Shows all Prime numbers before a given value printPrime(value)"""
    previous_primes_nb = []
    for i in range(2, n + 1):
        if isPrime(i):
            previous_primes_nb.append(i)
    return previous_primes_nb


def Prime():
    """Will show all Prime numbers from a generated value (2, 100)"""
    n = random.randint(2, 100)
    Prime = str(printPrime(n))[1:-1]
    print(Prime)


if __name__ == "__main__":
    Prime()
