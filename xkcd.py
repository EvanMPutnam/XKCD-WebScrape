"""
Author: Evan Putnam
Description: Web scrapes XKCD for their web comics.
Language: Python 3
Dependencies: Beautiful Soup, Requests, lxml

TODO: Use PIL to include alt-text and title on image itself.
TODO: Make a way to download only a single image if desired.
"""

from bs4 import BeautifulSoup
import requests
import urllib
import os

# constant for the web url
MAIN_URL = "xkcd.com/"

# Sub-folder to save content into.
SAVE_FOLDER = os.getcwd() + "/downloads"

# Debug constant
DEBUG = True

def gatherImage(i, lst, indiv = True):
    # Get html data
    url = MAIN_URL + str(i) + "/"
    r = requests.get("http://"+url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    # Get image data
    comicImage = soup.find('div',{"id":"comic"})
    comicImageTag = comicImage.find("img")

    # Make into acceptable url
    comicURL = comicImageTag['src']
    comicURL = comicURL[2:]

    # Comic title + alt text info.
    comicAlt = comicImageTag['alt']
    comicTitle = comicImageTag['title']

    # Add data to structure.
    lst.append([str(i),comicAlt, comicTitle])

    # Generate individual text file of alt texts for each item.
    pathVal = str(i)+'txt'
    if(indiv == True):
        file = open(pathVal, "w")
        file.write("Alt: "+comicAlt+"\n")
        file.write("Title: "+comicTitle)
        file.close()

    # Some debug info.
    print(i,":",comicURL)
    print()

    # Extension name and type
    ext = str(i)+"."+comicURL[-3:]
    fileEx = comicURL[-3:]

    # Limit filetype to images + download.
    if fileEx in ["jpg", "gif", "png"]:
        # Download the image and relocate it to downloads folder.
        urllib.request.urlretrieve("https://"+comicURL,ext)
    
    




def searchWebSite(staringNum, endingNum, indiv = True):
    '''
    Searches the website and downloads the comics to the current directory.
    :param staringNum number to start scrape: 
    :param endingNum number to end scrape: 
    :param indiv if you want an individual text file for each: 
    :return lst of alt-text/description info: 
    '''
    # Create the download folder if it does not exist.
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    
    # Change directory over to the save folder.
    currDir = os.getcwd()
    os.chdir(SAVE_FOLDER)
    
    # Array for holding the text information on each comic like alt-txt, description, etc.
    lst = []
    for i in range(staringNum, endingNum):
        try:
            gatherImage(i, lst, indiv)
        except Exception as e:
            if DEBUG:
                print (e)
            print("Error Page: ", i)

    # Swap to original directory.
    os.chdir(currDir)

    # Return list object for master census.
    return lst



def makeCensus(lst):
    '''
    Makes a text file with all descriptions and alt-text
    :param lst: 
    :return: 
    '''
    file = open(SAVE_FOLDER + "/Master.txt", "w")
    for elem in lst:
        try:
            file.write("Image: "+elem[0]+"\n")
            file.write("Alt: "+elem[1]+"\n")
            file.write("Title: "+elem[2]+"\n")
            file.write("\n")
        except Exception as e:
            if DEBUG:
                print (e)
            print ('Error in writing ' + str(elem) + ' to doc.')
    file.close()



def getImages(imgNum):
    '''
    Main function to call to download images and get the alt text
    :param imgNum what image number to go up to 1-whatever num they are at: 
    :return: 
    '''
    lstPics = searchWebSite(1,imgNum+1, False)
    makeCensus(lstPics)



if __name__ == '__main__':
    # Gets the images from 1 to input num
    getImages(int(input("Enter Max Comic Num: ")))
