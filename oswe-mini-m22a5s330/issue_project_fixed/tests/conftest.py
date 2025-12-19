import os
import sys

# Ensure project root (one level up) is on sys.path so `import src` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
