import subprocess
import os

from dandori_apps import start_dandori_mngmnt
from dandori_apps import start_dandori_sound

if __name__ == '__main__':
    process1 = subprocess.Popen(
        "python start_dandori_mngmnt.py",
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    process2 = subprocess.Popen(
        "python start_dandori_sound.py",
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )