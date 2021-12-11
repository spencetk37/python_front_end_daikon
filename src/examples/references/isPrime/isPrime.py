def isPrime(num):
    # Program to check if a number is prime or not

    # define a flag variable
    flag = False

    # prime numbers are greater than 1
    
        # check for factors
    for i in range(2, num):
        if (num % i) == 0:
                # if factor is found, set flag to True
            flag = True
                # break out of loop
            break

    # check if flag is True
    if flag:
        print(num, "is not a prime number")
        return False
    elif 1:
        print(num, "is a prime number")
        return True



if __name__ == "__main__":
    for i in range(1, 1000):
        isPrime(i)
