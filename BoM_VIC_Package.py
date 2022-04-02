# BoM Downloader for Kordia MSCS
# Version 0.2
# By Jason Armbrecht

import wget, os, shutil, time, psutil, sys, fitz
from datetime import datetime
from txtmarker.factory import Factory
from colorama import init
init()

# Defined variables. Change if you need.
bomDir = r'C:\BoMTemp\\'
coastal_vic = 'IDV10200' # Coastal Waters Forcast for Victoria
local_portp = 'IDV10460' # Port Phillip Local Waters
local_wport = 'IDV10461' # Westerport Local Waters
local_gipps = 'IDV19300' # Gippsland Lakes Local Waters
now = datetime.now()

# Check if BoMTemp exists. If not, create folder
def checkFolder ():
    print(now, "\x1b[1;33;40m Checking for BoMTemp folder...\x1b[1;37;40m")
    CHECK_FOLDER = os.path.isdir(bomDir)
    if not CHECK_FOLDER: # If folder doesn't exist, then create it.
        os.makedirs(bomDir)
        print(now, "\x1b[1;32;40m created folder : \x1b[1;37;40m", bomDir)
    else:
        print(now, "\x1b[1;32;40m", "", bomDir, "folder already exists.\x1b[1;37;40m")

# Delete all files in BoMTemp
def deleteFiles ():
    print(now, "\x1b[1;33;40m Cleaning BoMTemp folder...\x1b[1;37;40m")
    for filename in os.listdir(bomDir):
        file_path = os.path.join(bomDir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(now, "\x1b[1;32;40m File removed.\x1b[1;37;40m")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(now, "\x1b[1;32;40m Directory cleaned.\x1b[1;37;40m")
        except Exception as e:
            print(now, 'Failed to delete %s. Reason: %s' % (file_path, e))

# Download .txt file to retrive update time
def downloadTxt (bomId):
    print("\n", now, "\x1b[1;33;40m Requesting forecast issue time...\x1b[1;37;40m", "\n")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.txt', bomDir)

# Print the time updated line
def printUpdate (bomId):
    print("\x1b[1;34;40m")
    file = open(bomDir + bomId + ".txt")
    content = file.readlines() # read the content of the file opened
    #print(" ")
    print(content[4], content[5]) # read the 4th and 5th line from the file

# Asks user to confirm if the FTP has actually been updated yet.
def confirmUpdate ():
    print("\x1b[1;31;40m Confirm the issue times above. \x1b[1;37;40m")
    answer = input("Continue with the download? (y/n): ") 
    if answer == "y": 
        print("\x1b[1;33;40m Beginning download, highlighting and printing of files:\x1b[1;37;40m") 
    elif answer == "n": 
        sys.exit() 
    else: 
        print("\x1b[1;37;40m Please enter y or n.")

# Download pdf files
def downloadPdf (bomId):
    print(now, "\x1b[1;33;40m Starting download of", bomId, "...\x1b[1;37;40m", "\n")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.pdf', bomDir)
    print("\n", "\x1b[1;32;40m", now, bomId, "pdf file finished downloading.\x1b[1;37;40m", "\n")

def highlightDoc (bomId):
    print("\x1b[1;33;40m Auto-highlighting", bomId, "...\n")
    redColour = [0.8, 0.1, 0.1]
    blueColour = [0.1, 0.9, 1]
    greenColour = [0.6, 1, 0.1]
    purpleColour = [0.6, 0.3, 1]
    orangeColour = [1, 0.4, 0.1]
    def hl (hlText, hlColour):
        for page in pdf_file:
            text_to_be_highlighted = hlText
            highlight = page.search_for(text_to_be_highlighted)
            for inst in highlight:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke = hlColour)
                highlight.update()
    pdf_file = fitz.open(bomDir + bomId + ".pdf")
    hl("Strong Wind Warning", orangeColour)
    hl("Gale Warning", redColour)
    hl("Storm Force Wind Warning", redColour)
    hl("Please be aware", blueColour)
    hl("West Coast: SA-VIC Border to Cape Otway", greenColour)
    hl("Central Coast: Cape Otway to Wilsons Promontory", greenColour)
    hl("Central Gippsland Coast: Wilsons Promontory to Lakes Entrance", greenColour)
    hl("East Gippsland Coast: Lakes Entrance to 60nm east of Gabo Island", greenColour)
    hl("Coastal Waters Forecast for Victoria", purpleColour)
    hl("Local Waters Forecast for Port Phillip", purpleColour)
    hl("Local Waters Forecast for Western Port", purpleColour)
    hl("Local Waters Forecast Gippsland Lakes", purpleColour)
    pdf_file.save(bomDir + bomId + "_hl.pdf", garbage=4, deflate=True, clean=True)
    print("\x1b[1;32;40m Document succesfully highlighted. \n")

# Auto print files, kill adobe afterwards
def printFiles (bomId):
    print(now, "\x1b[1;33;40m Temporarily opening PDF Reader...\x1b[1;37;40m")
    os.startfile(bomDir + bomId + '_hl.pdf', "print")
    time.sleep(8)
    for p in psutil.process_iter(): # Close Acrobat after printing the PDF
        if 'AcroRd' in str(p):
            p.kill()
            print(now, "\x1b[1;32;40m Job sent to printer...\x1b[1;37;40m")


# Main program start
print("\x1b[1;34;40m    ____  ____  __  ___   ____                      __                __")         
print("   / __ )/ __ \/  |/  /  / __ \____ _      ______  / /___  ____ _____/ /__  _____")
print("  / __  / / / / /|_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/")
print(" / /_/ / /_/ / /  / /  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /  ")  
print("/_____/\____/_/  /_/  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/    ") 
print("\n")                                                                               
print("\x1b[1;37;40m -------------------------------\x1b[1;37;40m")
print("\x1b[1;34;40m ***BoM Downloader for Kordia***\x1b[1;37;40m")
print("\x1b[1;37;40m -------------------------------\x1b[1;37;40m")
print("\x1b[1;35;40m By Jason Armbrecht\x1b[1;37;40m")
print("\n")
checkFolder()
deleteFiles()
downloadTxt(coastal_vic)
downloadTxt(local_portp)
downloadTxt(local_wport)
downloadTxt(local_gipps)
print("\n")
printUpdate(coastal_vic)
printUpdate(local_portp)
printUpdate(local_wport)
printUpdate(local_gipps)
confirmUpdate()
print("\n")
downloadPdf(coastal_vic)
downloadPdf(local_portp)
downloadPdf(local_wport)
downloadPdf(local_gipps)
print("\n")
highlightDoc(coastal_vic)
highlightDoc(local_portp)
highlightDoc(local_wport)
highlightDoc(local_gipps)
#printFiles(coastal_vic)
#printFiles(local_portp)
#printFiles(local_wport)
#printFiles(local_gipps)
sleep(3)
deleteFiles()
print("\n", "\x1b[1;32;40m All tasks completed.\x1b[1;37;40m")
