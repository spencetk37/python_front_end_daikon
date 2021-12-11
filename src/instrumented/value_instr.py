import pickle
v = {}

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
    curr_entry = {'a': val_prep(a), 'b': val_prep(b)}
    if v.get('add()') is None:
        v['add()'] = []
    exit_0 = a + b
    curr_exit = [{'a': val_prep(a), 'b': val_prep(b), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['add()'].append([curr_entry, curr_exit])
    return exit_0

def subtract(num1, num2):
    curr_entry = {'num1': val_prep(num1), 'num2': val_prep(num2)}
    if v.get('subtract()') is None:
        v['subtract()'] = []
    exit_0 = num1 - num2
    curr_exit = [{'num1': val_prep(num1), 'num2': val_prep(num2), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['subtract()'].append([curr_entry, curr_exit])
    return exit_0

def multiply(num1, num2):
    curr_entry = {'num1': val_prep(num1), 'num2': val_prep(num2)}
    if v.get('multiply()') is None:
        v['multiply()'] = []
    exit_0 = num1 * num2
    curr_exit = [{'num1': val_prep(num1), 'num2': val_prep(num2), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['multiply()'].append([curr_entry, curr_exit])
    return exit_0

def divide(num1, num2):
    curr_entry = {'num1': val_prep(num1), 'num2': val_prep(num2)}
    if v.get('divide()') is None:
        v['divide()'] = []
    if num2 == 0:
        exit_0 = -1
        curr_exit = [{'num1': val_prep(num1), 'num2': val_prep(num2), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
        v['divide()'].append([curr_entry, curr_exit])
        return exit_0
    elif 1:
        exit_1 = num1 / num2
        curr_exit = [{'num1': val_prep(num1), 'num2': val_prep(num2), 'exit_1': val_prep(exit_1)}, {'EXIT': 1}]
        v['divide()'].append([curr_entry, curr_exit])
        return exit_1
if __name__ == '__main__':
    x = add(2, 3)
    y = subtract(4, 3)
    z = multiply(2, 3)
    c = divide(3, 3)
    b = divide(-1, 0)
    pickle_values = open('pickled_files/pickled_values', 'wb')
    pickle.dump(v, pickle_values)
    pickle_values.close()