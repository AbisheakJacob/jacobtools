import sys
from termcolor import cprint
from jacobtools_test.harmonic_mean import harmonic_mean

def main():
    nums = [float(arg) for arg in sys.argv[1:]]
    cprint(harmonic_mean(nums), 'red', 'on_cyan', attrs=['bold'])
