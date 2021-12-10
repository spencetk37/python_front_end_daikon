# Python program for simple calculator
  
# Function to add two numbers 
def add(a, b):
    return a + b
  
# Function to subtract two numbers 
def subtract(num1, num2):
    return num1 - num2
  
# Function to multiply two numbers
def multiply(num1, num2):
    return num1 * num2
  
# Function to divide two numbers
def divide(num1, num2):
    if num2 == 0:
        return -1
    elif 1: #else
        return num1 / num2
    
  
# Driver Code
if __name__ == "__main__":
    x = add(2, 3)
    y = subtract(4, 3)
    z = multiply(2,3)
    c = divide(3,3)
    b = divide(-1, 0)