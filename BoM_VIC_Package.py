# BoM Downloader for Kordia MSCS
# Version 0.1
# By Jason Armbrecht

import wget, os, shutil, time, psutil, sys
from datetime import datetime
from txtmarker.factory import Factory

# Defined variables. Change if you need.
bomDir = r'C:\BoMTemp\\'
coastal_vic = 'IDV10200' # Coastal Waters Forcast for Victoria
local_portp = 'IDV10460' # Port Phillip Local Waters
local_wport = 'IDV10461' # Westerport Local Waters
local_gipps = 'IDV19300' # Gippsland Lakes Local Waters
now = datetime.now()

# Check if BoMTemp exists. If not, create folder
def checkFolder ():
    print(now, "Checking for BoMTemp folder...")
    CHECK_FOLDER = os.path.isdir(bomDir)
    if not CHECK_FOLDER: # If folder doesn't exist, then create it.
        os.makedirs(bomDir)
        print(now, "created folder : ", bomDir)
    else:
        print(now, bomDir, "folder already exists.")

# Delete all files in BoMTemp
def deleteFiles ():
    print(now, "Cleaning BoMTemp folder.")
    for filename in os.listdir(bomDir):
        file_path = os.path.join(bomDir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(now, "Cleaning directory...")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(now, "Directory cleaned.")
        except Exception as e:
            print(now, 'Failed to delete %s. Reason: %s' % (file_path, e))

# Download .txt file to retrive update time
def downloadTxt (bomId):
    print(now, "Requesting forcast issue time...")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.txt', bomDir)

# Print the time updated line
def printUpdate (bomId):
    file = open(bomDir + bomId + ".txt")
    content = file.readlines() # read the content of the file opened
    print(" ")
    print(content[4], content[5]) # read 10th line from the file

# Asks user to confirm if the FTP has actually been updated yet.
def confirmUpdate ():
    answer = input("Check issue time above. Continue with the download? (y/n): ") 
    if answer == "y": 
        print("Beginning download and printing of files:") 
    elif answer == "n": 
        sys.exit() 
    else: 
        print("Please enter y or n.")

# Download pdf files
def downloadPdf (bomId):
    print(now, "Starting download of ", bomId, "...")
    wget.download('ftp://ftp2.bom.gov.au/anon/gen/fwo/' + bomId + '.pdf', bomDir)
    print(now, bomId, "pdf file finished downloading.")

# Create highlighted annotations
def highlightDoc (bomId):
    highlights = [
        ("Wind Warning", "Strong Wind Warning"),
        ("Wind Warning", "Gale Warning"),
        (None, "Issued at"),
        (None, "Forecast issued at"),
        (None, "Please be aware"),
        (None, "Weather Situation"),
        (None, "West Coast: SA-VIC Border to Cape Otway"),
        (None, "Central Coast: Cape Otway to Wilsons Promontory"),
        (None, "Central Gippsland Coast: Wilsons Promontory to Lakes Entrance"),
        (None, "East Gippsland Coast: Lakes Entrance to 60nm east of Gabo Island"),
    ]
    highlighter = Factory.create("pdf")
    highlighter.highlight(bomDir + bomId + ".pdf", bomDir + bomId + "_anno.pdf", highlights)

# Auto print files, kill adobe afterwards
def printFiles (bomId):
    print(now, "Temporarily opening PDF Reader...")
    os.startfile(bomDir + bomId + '_anno.pdf', "print")
    time.sleep(12)
    for p in psutil.process_iter(): # Close Acrobat after printing the PDF
        if 'AcroRd' in str(p):
            p.kill()
            print(now, "Job sent to printer...")


# Main program start
print("-------------------------------")
print("***BoM Downloader for Kordia***")
print("-------------------------------")
print(" ")
print("By Jason Armbrecht")
print(" ")
checkFolder()
deleteFiles()
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
highlightDoc(coastal_vic)
highlightDoc(local_portp)
highlightDoc(local_wport)
highlightDoc(local_gipps)
printFiles(coastal_vic)
printFiles(local_portp)
printFiles(local_wport)
printFiles(local_gipps)
print("All tasks completed.")
