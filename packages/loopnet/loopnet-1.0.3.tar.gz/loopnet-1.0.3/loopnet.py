"""This is the "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""
import sys

def print_ll(l,level=0,indent=False,f=sys.stdout):
    """This function takes a positional argument called "the_list", which
    is any Python list (of - possibly - nested lists). Each data item in the
    provided list is (recursively) printed to the screen on it's own line."""
    for i in l:
        if isinstance(i,list):
            print_ll(i,level+1,indent,f)
        else:
            if indent:
                for tab in range(level):
                    print('\t',end='',file=f)
            print(i,file=f)