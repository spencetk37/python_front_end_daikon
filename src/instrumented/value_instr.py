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

def push(stack, item):
    curr_entry = {'stack': val_prep(stack), 'item': val_prep(item)}
    if v.get('push()') is None:
        v['push()'] = []
    if not isCap(stack):
        stack.append(item)
        exit_0 = True
        curr_exit = [{'stack': val_prep(stack), 'item': val_prep(item), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
        v['push()'].append([curr_entry, curr_exit])
        return exit_0
    elif 1:
        print('It is full')
        exit_1 = False
        curr_exit = [{'stack': val_prep(stack), 'item': val_prep(item), 'exit_1': val_prep(exit_1)}, {'EXIT': 1}]
        v['push()'].append([curr_entry, curr_exit])
        return exit_1

def pop(stack):
    curr_entry = {'stack': val_prep(stack)}
    if v.get('pop()') is None:
        v['pop()'] = []
    if not isEmpty(stack):
        stack.pop()
        exit_0 = True
        curr_exit = [{'stack': val_prep(stack), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
        v['pop()'].append([curr_entry, curr_exit])
        return exit_0
    elif 1:
        print('It is empty')
        exit_1 = False
        curr_exit = [{'stack': val_prep(stack), 'exit_1': val_prep(exit_1)}, {'EXIT': 1}]
        v['pop()'].append([curr_entry, curr_exit])
        return exit_1

def peek(stack):
    curr_entry = {'stack': val_prep(stack)}
    if v.get('peek()') is None:
        v['peek()'] = []
    if not isEmpty(stack):
        exit_0 = stack[0]
        curr_exit = [{'stack': val_prep(stack), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
        v['peek()'].append([curr_entry, curr_exit])
        return exit_0
    elif 1:
        exit_1 = -1
        curr_exit = [{'stack': val_prep(stack), 'exit_1': val_prep(exit_1)}, {'EXIT': 1}]
        v['peek()'].append([curr_entry, curr_exit])
        return exit_1

def size(stack):
    curr_entry = {'stack': val_prep(stack)}
    if v.get('size()') is None:
        v['size()'] = []
    exit_0 = len(stack)
    curr_exit = [{'stack': val_prep(stack), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['size()'].append([curr_entry, curr_exit])
    return exit_0

def isEmpty(stack):
    curr_entry = {'stack': val_prep(stack)}
    if v.get('isEmpty()') is None:
        v['isEmpty()'] = []
    exit_0 = size(stack) == 0
    curr_exit = [{'stack': val_prep(stack), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['isEmpty()'].append([curr_entry, curr_exit])
    return exit_0

def isCap(stack):
    curr_entry = {'stack': val_prep(stack)}
    if v.get('isCap()') is None:
        v['isCap()'] = []
    exit_0 = size(stack) == 10
    curr_exit = [{'stack': val_prep(stack), 'exit_0': val_prep(exit_0)}, {'EXIT': 0}]
    v['isCap()'].append([curr_entry, curr_exit])
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
    pickle_values = open('pickled_files/pickled_values', 'wb')
    pickle.dump(v, pickle_values)
    pickle_values.close()