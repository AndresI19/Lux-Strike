from random import randint

def generate_Xdegit_seed(X):
    #returns a string for seed of size X
    final_seed = ''
    for i in range(X):
        seed = str(randint(0,9))
        final_seed = final_seed + seed
    return final_seed

def seed_random_choice(seed,register,instance):
    #takes arguments seed: str, register: list, instance: int
    """Uses the seed passed to it to make a random choice from a list, 
    an instance is used to determain at what value the seed is evaluated at,
    different instances create different results per same seed. 
    This allows a user to pull different choices from the same seed, using the same instance value.

    ie: for i in range(10):
        seed_random_choice(seed,register,i)
        <<will produce the same 10 different choices, per seed>>"""
    if type(register) == list:
        if len(register) >= 2:
            if instance < len(seed):

                #------------------------------------------------------
                RNG = float(seed[instance:])
                order = pow(10,(-len(seed[instance:])))
                RNG = RNG*order
                for i in range(len(register)):
                    partition = (i+1) * (1/len(register))
                    if RNG < partition:
                        return register[i]
                #------------------------------------------------------
            else:
                print('Seed is too small for the instance size')
        else: 
            print('Error, list passed is too short, must contain 2 or more elements')
    else:
        print('Error, passed variabled must be of the list class')

def seed_random_bound_int(seed,bounds,instance):
    #takes arguments seed: str, register: list, instance: int
    """Uses the seed passed to it to make a random choice of a number between, 
    two bounds given, different instances create different results per same seed.""" 
    if type(bounds) == tuple:
        if len(bounds) == 2:
            if bounds[1] > bounds[0]:
                if instance < len(seed):
                    length = abs(bounds[1]-bounds[0])
                    register = []
                    for i in range(length+1):
                        register.append(bounds[0]+i)
                    #------------------------------------------------------
                    RNG = float(seed[instance:])
                    order = pow(10,(-len(seed[instance:])))
                    RNG = RNG*order
                    for i in range(len(register)):
                        partition = (i+1) * (1/len(register))
                        if RNG < partition:
                            return register[i]
                #------------------------------------------------------
                else:
                    print('Seed is too small for the instance size')
            else:
                print('Second bound arguement must be larger than the first')
        else: 
            print('Error, tuple passed is must contain 2 elements')
    else:
        print('Error, passed variabled must be of the tuple class')

def seed_weighted_bound_int(seed,bounds,instance,weights):
    #takes arguments seed: str, register: list, instance: int
    """Uses the seed passed to it to make a random choice of a number between, 
    two bounds given, different instances create different results per same seed
    However with given weights."""
##
    SUM = 0
    for i in range(len(weights)):
        SUM += weights[i]
    if SUM == 1:
        if type(bounds) == tuple:
            if len(bounds) == 2:
                if bounds[1] > bounds[0]:
                    if instance < len(seed):
##
                        length = abs(bounds[1]-bounds[0])
                        register = []
                        for i in range(length+1):
                            register.append(bounds[0]+i)
                        #------------------------------------------------------
                        RNG = float(seed[instance:])
                        order = pow(10,(-len(seed[instance:])))
                        RNG = RNG*order
                        partition = 0
                        for i in range(len(weights)):
                            partition += weights[i]
                            if RNG < partition:
                                return register[i]
                    #------------------------------------------------------
##
                    else:
                        print('Seed is too small for the instance size')
                else:
                    print('Second bound arguement must be larger than the first')
            else: 
                print('Error, tuple passed is must contain 2 elements')
        else:
            print('Error, passed variabled must be of the tuple class')
    else:
        print('Error, weights dont add to one')

def generate_seed_from_seed(seed,instance):
    #shuffles the numbers around in the seed to create a different seed for operations
    if not instance == 0:
        final_seed = ''
        factor = (19/7)
        for i in range(len(seed)):
            Seed = ((int(seed[i])+instance)*factor)
            Seed = str(round(Seed))
            final_seed = final_seed + Seed[-1]
    return final_seed