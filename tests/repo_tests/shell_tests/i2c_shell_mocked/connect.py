
import subprocess
import os

with open(os.devnull, 'w') as devnull:
    res = subprocess.run(
        ["../../../build/zephyr/zephyr.exe"],
        stdout=devnull,
        stderr=devnull
    )
print("Vystup z pytestu!")