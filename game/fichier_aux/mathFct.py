def round_up(x,y):
    mod = x//y
    div = x/y
    if mod == div :
        return mod
    else :
        return mod + 1