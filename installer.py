"""SETUP FOR BOM DOWNLOADER"""
import subprocess
import sys

print("This tool will install required dependecies for BOM DOWNLOADER")
print("Please make sure you have, or will have, downloaded Adobe Acrobat DC.")
answer = input("Continue with the dependencie install? (y/n): ")
if answer == "y":
    print("Beginning download and installation...")
elif answer == "n":
    sys.exit()
else:
    print("Please enter y or n.")

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("\n")
print("Installation has completed. Please check for any errors above.")
print("Now, open Adobe Acrobat DC (if already installed) and navigate to:")
print("File > Edit > Preferences > Security (Enchanced).")
print("Click 'Add New Folder' and add 'C:\BoMTemp' to the list of privelaged paths. Then click OK.")
print("If you dont see the folder in the menu tree, click 'New Folder' in C:\ drive.")
print("You can then close Adobe.")
answer1 = input("After reading and actioning the above message, you can close this installer by typing 'exit': ")
if answer1 == "exit":
    print("Exiting.")
    sys.exit()
elif answer1 == "Exit":
    sys.exit()
else:
    print("Please enter 'exit'")
