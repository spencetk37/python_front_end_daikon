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

#val_prep = lambda x: str(x).lower() if type(x) == bool else x
def val_prep(val):

    if type(val) == bool:
        val = str(val).lower()    
    elif type(val) == str:
        val = "\""+val+"\""
    elif type(val) == list:
        val = "[" + " ".join(map(str,val)) + "]"
    
    return val

