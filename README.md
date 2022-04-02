# BoM Scripts

A soon-to-be collection of scripts to interact with BoM products. Motivation is to practice and improve with Python.

VIC_BoM_Package.py downloads, highlights and prints a package of Victorian coastal and local marine forecasts.
It is a messy but functional script. It uses Adobe Acrobat for pdf print. If it is the first time using the script, it may fail due to trying to open the file in an  untrusted manner. If so, add the BoMTemps folder to the priveleged/trusted folders in Adobe Reader security preferences menu. Due to workplace constraints, I am unable to use GhostScript for more transparent print operation, unfortunately. But I hope to incorporate it in the future.

# General Instructions: 

1. Install python via Microsoft Store
2. Update PIP via command prompt
3. Also via command prompt, install the following dependencies:
wget, PyMuPDF, colorama.
4. Place VIC_BoM_Package.py in your Z:drive
5. Create cmd.exe shortcut. 
6.            Target = C:\WINDOWS\system32\cmd.exe /k python VIC_BoM_Package.py
7.            Start in = Z:\
8. Open Adobe Reader DC.
9. Navigate to File > Edit > Preferences > Security (Enchanced)
10. Click 'Add Folder Path'
11. Add 'C:\BoMTemp\' as a privilaged/trusted location, press OK and exit.
12. Run script.


I may create an actual distributable at some point.
