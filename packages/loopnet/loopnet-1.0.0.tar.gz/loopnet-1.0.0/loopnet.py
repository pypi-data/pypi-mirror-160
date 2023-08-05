"""This is the "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""

def print_ll(l,level=0):
    """This function takes a positional argument called "the_list", which
    is any Python list (of - possibly - nested lists). Each data item in the
    provided list is (recursively) printed to the screen on it's own line."""
    for i in l:
        if isinstance(i,list):
            print_ll(i,level+1)
        else:
            for tab in range(level):
                print('\t',end='')
            print(i)