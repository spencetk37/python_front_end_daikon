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

def add(a, b):
    if d.get('add():::ENTER') is None:
        d['add():::ENTER'] = {}
    d['add():::ENTER']['b'] = type_prep(b)
    d['add():::ENTER']['a'] = type_prep(a)
    if d.get('add():::EXIT0') is None:
        d['add():::EXIT0'] = {}
    d['add():::EXIT0']['a'] = type_prep(a)
    d['add():::EXIT0']['b'] = type_prep(b)
    exit_0 = a + b
    d['add():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0

def subtract(num1, num2):
    if d.get('subtract():::ENTER') is None:
        d['subtract():::ENTER'] = {}
    d['subtract():::ENTER']['num2'] = type_prep(num2)
    d['subtract():::ENTER']['num1'] = type_prep(num1)
    if d.get('subtract():::EXIT0') is None:
        d['subtract():::EXIT0'] = {}
    d['subtract():::EXIT0']['num1'] = type_prep(num1)
    d['subtract():::EXIT0']['num2'] = type_prep(num2)
    exit_0 = num1 - num2
    d['subtract():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0

def multiply(num1, num2):
    if d.get('multiply():::ENTER') is None:
        d['multiply():::ENTER'] = {}
    d['multiply():::ENTER']['num2'] = type_prep(num2)
    d['multiply():::ENTER']['num1'] = type_prep(num1)
    if d.get('multiply():::EXIT0') is None:
        d['multiply():::EXIT0'] = {}
    d['multiply():::EXIT0']['num1'] = type_prep(num1)
    d['multiply():::EXIT0']['num2'] = type_prep(num2)
    exit_0 = num1 * num2
    d['multiply():::EXIT0']['exit_0'] = type_prep(exit_0)
    return exit_0

def divide(num1, num2):
    if d.get('divide():::ENTER') is None:
        d['divide():::ENTER'] = {}
    d['divide():::ENTER']['num2'] = type_prep(num2)
    d['divide():::ENTER']['num1'] = type_prep(num1)
    if num2 == 0:
        if d.get('divide():::EXIT0') is None:
            d['divide():::EXIT0'] = {}
        d['divide():::EXIT0']['num1'] = type_prep(num1)
        d['divide():::EXIT0']['num2'] = type_prep(num2)
        exit_0 = -1
        d['divide():::EXIT0']['exit_0'] = type_prep(exit_0)
        return exit_0
    elif 1:
        if d.get('divide():::EXIT1') is None:
            d['divide():::EXIT1'] = {}
        d['divide():::EXIT1']['num1'] = type_prep(num1)
        d['divide():::EXIT1']['num2'] = type_prep(num2)
        exit_1 = num1 / num2
        d['divide():::EXIT1']['exit_1'] = type_prep(exit_1)
        return exit_1
if __name__ == '__main__':
    x = add(2, 3)
    y = subtract(4, 3)
    z = multiply(2, 3)
    c = divide(3, 3)
    b = divide(-1, 0)
    pickle_types = open('pickled_files/pickled_types', 'wb')
    pickle.dump(d, pickle_types)
    pickle_types.close()