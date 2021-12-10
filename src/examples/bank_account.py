# Python program to create Bankaccount class
# Balance in USD
balance = 2000
max_cap = 10000
 
def deposit(amount):
    global balance
    if balance + amount <= max_cap:
        balance += amount
        print("\n Amount Deposited:",amount)
        return True
    elif 1:
        print("Reached Maximum")
        return False

def withdraw(amount):
    global balance
    if balance>=amount:
        balance-=amount
        print("\n You Withdrew:", amount)
        return True
    elif 1:
        print("\n Insufficient balance  ")
        return False

 
# Driver code
if __name__ == "__main__":
    for i in range(0, 5):
        deposit(2000)

    for i in range(0, 6):
        withdraw(2000)