import sys
from jacobtools_test.harmonic_mean import harmonic_mean
from termcolor import cprint


def main():
    """Calculate the harmonic mean of the provided numbers.

    This is a test documentation
    """

    result = 0.0

    try:
        nums = [float(num) for num in sys.argv[1:]]
    except ValueError:
        nums = []

    try:
        result = harmonic_mean(nums)
    except ZeroDivisionError:
        pass

    cprint(str(result), "red", "on_cyan", attrs=["bold"])
