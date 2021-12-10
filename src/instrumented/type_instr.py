import pickle
d = {}

def type_prep(atype):
    tp = str(type(atype))
    tp = tp.replace("<type '", '').replace("'>", '').lower()
    if tp == 'bool':
        tp = 'boolean'
    elif tp == 'list':
        if type(atype[0]) == int:
            tp = 'int[]'
        elif type(atype[0]) == float:
            tp = 'float[]'
        else:
            tp = 'char[]'
    elif tp == 'str':
        tp = 'java.lang.String'
    return tp

def val_prep(val):
    if type(val) == bool:
        val = str(val).lower()
    elif type(val) == str:
        val = '"' + val + '"'
    elif type(val) == list:
        val = '[' + ' '.join(map(str, val)) + ']'
    return val

def push(stack, item):
    if d.get('push():::ENTER') is None:
        d['push():::ENTER'] = {}
    d['push():::ENTER']['item'] = type_prep(item)
    d['push():::ENTER']['stack'] = type_prep(stack)
    if not isCap(stack):
        stack.append(item)
        if d.get('push():::EXIT0') is None:
            d['push():::EXIT0'] = {}
        d['push():::EXIT0']['stack'] = type_prep(stack)
        d['push():::EXIT0']['item'] = type_prep(item)
        exit_0 = True
        d['push():::EXIT0']['exit_0'] = type_prep(exit_0)
        return exit_0
    elif 1:
        print('It is full')
        if d.get('push():::EXIT1') is None:
            d['push():::EXIT1'] = {}
        d['push():::EXIT1']['stack'] = type_prep(stack)
        d['push():::EXIT1']['item'] = type_prep(item)
        exit_1 = False
        d['push():::EXIT1']['exit_1'] = type_prep(exit_1)
        return exit_1

def pop(stack):
    if d.get('pop():::ENTER') is None:
        d['pop():::ENTER'] = {}
    d['pop():::ENTER']['stack'] = type_prep(stack)
    if not isEmpty(stack):
        stack.pop()
        if d.get('pop():::EXIT0') is None:
            d['pop():::EXIT0'] = {}
        d['pop():::EXIT0']['stack'] = type_prep(stack)
        exit_0 = True
        d['pop():::EXIT0']['exit_0'] = type_prep(exit_0)
        return exit_0
    elif 1:
        print('It is empty')
        if d.get('pop():::EXIT1') is None:
            d['pop():::EXIT1'] = {}
        d['pop():::EXIT1']['stack'] = type_prep(stack)
        exit_1 = False
        d['pop():::EXIT1']['exit_1'] = type_prep(exit_1)
        return exit_1

def peek(stack):
    if d.get('peek():::ENTER') is None:
        d['peek():::ENTER'] = {}
    d['peek():::ENTER']['stack'] = type_prep(stack)
    if not isEmpty(stack):
        if d.get('peek():::EXIT0') is None:
            d['peek():::EXIT0'] = {}
        d['peek():::EXIT0']['stack'] = type_prep(stack)
        exit_0 = stack[0]
        d['peek():::EXIT0']['exit_0'] = type_prep(exit_0)
        return exit_0
    elif 1:
        if d.get('peek():::EXIT1') is None:
            d['peek():::EXIT1'] = {}
        d['peek():::EXIT1']['stack'] = type_prep(stack)
        exit_1 = -1
        d['peek():::EXIT1']['exit_1'] = type_prep(exit_1)
        return exit_1

def size(stack):
    if d.get('size():::ENTER') is None:
        d['size():::ENTER'] = {}
    d['size():::ENTER']['stack'] = type_prep(stack)
    if d.get('size():::EXIT0') is None:
        d['size():::EXIT0'] = {}
    d['size():::EXIT0']['stack'] = type_prep(stack)
    exit_0 = len(stack)
    d['size():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0

def isEmpty(stack):
    if d.get('isEmpty():::ENTER') is None:
        d['isEmpty():::ENTER'] = {}
    d['isEmpty():::ENTER']['stack'] = type_prep(stack)
    if d.get('isEmpty():::EXIT0') is None:
        d['isEmpty():::EXIT0'] = {}
    d['isEmpty():::EXIT0']['stack'] = type_prep(stack)
    exit_0 = size(stack) == 0
    d['isEmpty():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0

def isCap(stack):
    if d.get('isCap():::ENTER') is None:
        d['isCap():::ENTER'] = {}
    d['isCap():::ENTER']['stack'] = type_prep(stack)
    if d.get('isCap():::EXIT0') is None:
        d['isCap():::EXIT0'] = {}
    d['isCap():::EXIT0']['stack'] = type_prep(stack)
    exit_0 = size(stack) == 10
    d['isCap():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0
if __name__ == '__main__':
    my_stack = [0]
    isEmpty(my_stack)
    for i in range(0, 20):
        push(my_stack, i)
    isCap(my_stack)
    for i in range(0, 9):
        peek(my_stack)
        pop(my_stack)
    pickle_types = open('pickled_files/pickled_types', 'wb')
    pickle.dump(d, pickle_types)
    pickle_types.close()