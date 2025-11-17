import os
import sys

# ensure the repository root is on sys.path for imports like 'src'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

print('Test Root:', ROOT)
