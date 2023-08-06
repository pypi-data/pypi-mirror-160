import random
import hashlib

def MachineCode(number):
    random.seed(number)
    return hashlib.md5(str(random.random()).encode()).hexdigest()