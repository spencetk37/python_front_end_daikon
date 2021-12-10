def push(stack, item):
    if not isCap(stack):
        stack.append(item)
        return True
    elif 1:
        print("It is full")
        return False

def pop(stack):
    if not isEmpty(stack):
        stack.pop()
        return True
    elif 1:
        print("It is empty")
        return False


def peek(stack):
    if not isEmpty(stack):
        return stack[0]
    elif 1:
        return -1
    

def size(stack):
    return len(stack)


def isEmpty(stack):
    return size(stack) == 0


def isCap(stack):
    return size(stack) == 10


if __name__ == "__main__":
    #issue here where type_prep will check first element's type in empty list....could not fix this in time :(
    my_stack = [0]

    isEmpty(my_stack)

    for i in range(0, 20):
        push(my_stack, i)

    isCap(my_stack)

    for i in range(0, 9):
        peek(my_stack)
        pop(my_stack)
    
