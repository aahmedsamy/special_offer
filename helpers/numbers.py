from random import randint


def gen_rand_number(length):
    """
    generates random number with desired length
    """
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return randint(range_start, range_end)
