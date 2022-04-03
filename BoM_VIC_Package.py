"""BOM DOWNLOADER"""
# BoM Downloader for Kordia
# Version 0.3
# By Jason Armbrecht
# https://github.com/jasonarmbrecht/BoM-Scripts-for-Work

import os
import sys
import shutil
import time
from datetime import datetime
import psutil
import fitz
import wget
from colorama import init
init()

# Defined variables. Change if you need.
bomDir = r'C:\BoMTemp\\'
coastal_vic = 'IDV10200' # Coastal Waters Forcast for Victoria
local_portp = 'IDV10460' # Port Phillip Local Waters
local_wport = 'IDV10461' # Westerport Local Waters
local_gipps = 'IDV19300' # Gippsland Lakes Local Waters

#Define text colours.
txt_grn = "\x1b[1;32;40m"
txt_wht = "\x1b[1;37;40m"
txt_ylo = "\x1b[1;33;40m"
txt_blu = "\x1b[1;34;40m"
txt_red = "\x1b[1;31;40m"
txt_pur = "\x1b[1;35;40m"

# Check if BoMTemp exists. If not, create folder
def checkFolder ():
    print(f"{datetime.now()} {txt_ylo} Checking for BoMTemp folder...{txt_wht}")
    check_folder = os.path.isdir(bomDir)
    if not check_folder: # If folder doesn't exist, then create it.
        os.makedirs(bomDir)
        print(f"{datetime.now()} {txt_grn} created folder : {txt_wht} {bomDir}")
    else:
        print(f"{datetime.now()} {txt_grn} {bomDir} folder already exists.{txt_wht}")

# Delete all files in BoMTemp
def deleteFiles ():
    print(f"{datetime.now()} {txt_ylo} Cleaning BoMTemp folder...{txt_wht}")
    for filename in os.listdir(bomDir):
        file_path = os.path.join(bomDir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"{datetime.now()} {txt_grn} File removed.{txt_wht}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"{datetime.now()} {txt_grn} Directory cleaned.{txt_wht}")
        except Exception as e:
            print(f"{datetime.now()} Failed to delete {file_path}. Reason: {e}")

# Download .txt file to retrive update time
def downloadTxt (bomId):
    print(f"{datetime.now()} {txt_ylo} Requesting forecast issue time...{txt_wht}")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.txt', bomDir)
    print("\n")

# Print the time updated line
def printUpdate (bomId):
    print(f"{txt_blu}")
    file = open(bomDir + bomId + ".txt", encoding="utf8")
    content = file.readlines() # read the content of the file opened
    print(content[4], content[5]) # read the 4th and 5th line from the file

# get the issue time to use for highlighting
def issueTime (bomId):
    file = open(bomDir + bomId + ".txt", encoding="utf8")
    content = file.readlines()
    return str(content[5]) # returns issue time sentence as string

# Asks user to confirm if the FTP has actually been updated yet.
def confirmUpdate ():
    print(f" Confirm the issue times above. {txt_wht}")
    answer = input("Continue with the download? (y/n): ")
    if answer == "y":
        print(f"\n {txt_ylo} Beginning download, highlighting and printing of files:{txt_wht}")
    elif answer == "n":
        sys.exit()
    else:
        print(f"{txt_wht} Please enter y or n.")

# Download pdf files
def downloadPdf (bomId):
    print(f"{datetime.now()} {txt_ylo} Starting download of {bomId}...{txt_wht}")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.pdf', bomDir)
    print(f"\n {datetime.now()} {txt_grn} {bomId} pdf file finished downloading.{txt_wht}")

def highlightDoc (bomId):
    print(f"{datetime.now()} {txt_ylo} Auto-highlighting {bomId}...")
    redColour = [1, 0.2, 0.2] # set colors to use for highlighting
    blueColour = [0.6, 0.6, 1]
    greenColour = [0.6, 1, 0.1]
    yellowColour = [1, 1, 0]
    orangeColour = [1, 0.4, 0.1]
    pinkColour = [1, 0.5, 1]
    aquaColour = [0.3, 1, 1]
    def hl (hlText, hlColour):
        for page in pdf_file:
            text_to_be_highlighted = hlText
            highlight = page.search_for(text_to_be_highlighted)
            for inst in highlight:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke = hlColour)
                highlight.update()
    pdf_file = fitz.open(bomDir + bomId + ".pdf")
    hl(issueTime(bomId), aquaColour) # start highlighting stuff
    hl("Strong Wind Warning", orangeColour)
    hl("Gale Warning", redColour)
    hl("Storm Force Wind Warning", redColour)
    hl("Please be aware", blueColour)
    hl("Weather Situation", pinkColour)
    hl("West Coast: SA-VIC Border to Cape Otway", greenColour)
    hl("Central Coast: Cape Otway to Wilsons Promontory", greenColour)
    hl("Central Gippsland Coast: Wilsons Promontory to Lakes Entrance", greenColour)
    hl("East Gippsland Coast: Lakes Entrance to 60nm east of Gabo Island", greenColour)
    hl("Coastal Waters Forecast for Victoria", yellowColour)
    hl("Local Waters Forecast for Port Phillip", yellowColour)
    hl("Local Waters Forecast for Western Port", yellowColour)
    hl("Local Waters Forecast Gippsland Lakes", yellowColour)
    pdf_file.save(bomDir + bomId + "_hl.pdf", garbage=4, deflate=True, clean=True)
    print(f"{txt_grn} Document succesfully highlighted.{txt_wht}")

# Auto print files, kill adobe afterwards
def printFiles (bomId):
    print(f"{datetime.now()} {txt_ylo} Temporarily opening PDF Reader...{txt_wht}")
    os.startfile(bomDir + bomId + '_hl.pdf', "print")
    time.sleep(8)
    for p in psutil.process_iter(): # Close Acrobat after printing the PDF
        if 'AcroRd' in str(p):
            p.kill()
            print(f"{datetime.now()} {txt_grn} Job sent to printer...{txt_wht}")


# Main program start
print(f"{txt_blu}    ____  ____  __  ___   ____                      __                __")
print("   / __ )/ __ \/  |/  /  / __ \____ _      ______  / /___  ____ _____/ /__  _____")
print("  / __  / / / / /|_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/")
print(" / /_/ / /_/ / /  / /  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /  ")
print("/_____/\____/_/  /_/  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/    ")
print("\n")
print(f"{txt_wht} -------------------------------{txt_wht}")
print(f"{txt_blu} ***BoM Downloader for Kordia***{txt_wht}")
print(f"{txt_wht} -------------------------------{txt_wht}")
print(f"{txt_pur} By Jason Armbrecht{txt_wht}")
print("\n")
checkFolder()
deleteFiles()
print("\n")
downloadTxt(coastal_vic)
downloadTxt(local_portp)
downloadTxt(local_wport)
downloadTxt(local_gipps)
printUpdate(coastal_vic)
printUpdate(local_portp)
printUpdate(local_wport)
printUpdate(local_gipps)
confirmUpdate()
downloadPdf(coastal_vic)
downloadPdf(local_portp)
downloadPdf(local_wport)
downloadPdf(local_gipps)
print("\n")
highlightDoc(coastal_vic)
highlightDoc(local_portp)
highlightDoc(local_wport)
highlightDoc(local_gipps)
print("\n")
printFiles(coastal_vic)
printFiles(local_portp)
printFiles(local_wport)
printFiles(local_gipps)
time.sleep(2)
deleteFiles()
print(f"\n {txt_grn} All tasks completed.{txt_wht}")
