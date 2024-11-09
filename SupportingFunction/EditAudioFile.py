from playsound import playsound
import os
import platform

def multiOsRm(filepath):
    if "mac" in platform.platform():
        os.remove('./'+filepath)
    elif "linux" in platform.platform():
        os.remove('./'+filepath)
    elif "windows" in platform.platform():
        os.remove('./'+filepath)


def windowsPlaysound(filepath, delete=True):
    import winsound
    winsound.PlaySound(filepath)    
    if delete:
        multiOsRm(filepath)    
    # os.system("del  "+filepath)

def macPlaysound(filepath, delete=True):
    playsound(filepath)
    if delete:
        multiOsRm(filepath)   

def LinuxPlaysound(filepath,delete=True):
    playsound(filepath)
    if delete:
        multiOsRm(filepath)   

def multiOsSound(filepath,delete=True):
    if "mac" in platform.platform():
        macPlaysound(filepath,delete)
    elif "linux" in platform.platform():
        LinuxPlaysound(filepath,delete)
        print(platform.platform())
    elif "windows" in platform.platform():
        windowsPlaysound(filepath,delete)
        print(platform.platform())
    else:
        print(platform.platform())



