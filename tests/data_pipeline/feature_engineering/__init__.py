import os
import sys
import inspect

borala = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(
    os.path.abspath(borala))
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(currentdir)))
sys.path.insert(0, f'{parentdir}/src')