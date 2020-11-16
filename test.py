
def add(args):
    x,y = args
    print(x+y)

def function(fargs,f=add):
    for i in range(3):
        f(fargs)

function([3,4])