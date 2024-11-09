from playsound import playsound
import os
import platform
import time

def multiOsRm(filepath):
    if "mac" in platform.platform():
        os.remove('./'+filepath)
    elif "linux" in platform.platform():
        os.remove('./'+filepath)
    elif "Windows" in platform.platform():
        os.remove('./'+filepath)
 
def multiOsSound(filepath,delete=True):
    playsound(filepath)
    if delete:
        multiOsRm(filepath)



