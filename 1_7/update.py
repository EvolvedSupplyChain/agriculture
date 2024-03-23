import os
try:
    os.rename('newname.py', 'main2.py')
except:
    print("error")