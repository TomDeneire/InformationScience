"""
Publish to GitHub
"""

import os
import sys

print("Type your commit message (or q: to quit): ")
message = input()

if message == "q:":
    sys.exit(0)
else:
    os.system('git add .')
    os.system(f'git commit . -m "{message}"')
    os.system('git push')
