def hasPerm(perm, int):
    return (perm & int) != 0

def isInt(check, erroring = False):
    try:
        int(check)
    except TypeError:
        if erroring:
            raise TypeError
        else:
            return False
    return True
