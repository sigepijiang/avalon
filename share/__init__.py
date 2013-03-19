import os
import sys


path = os.path.join(os.getcwd(), os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)
