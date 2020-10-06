"""
Author: Evan Putnam
Description: Web scrapes XKCD for their web comics.
Language: Python 3
Dependencies: Beautiful Soup, Requests, lxml
"""

from bs4 import BeautifulSoup
import requests
import urllib

# constant for the web url
MAIN_URL = "xkcd.com/"

# Debug constant
DEBUG = True

def searchWebSite(staringNum, endingNum, indiv = True):
    '''
    Searches the website and downloads the comics to the current directory.
    :param staringNum number to start scrape: 
    :param endingNum number to end scrape: 
    :param indiv if you want an individual text file for each: 
    :return lst of alt-text/description info: 
    '''
    # Array for holding the text information on each comic like alt-txt, description, etc.
    lst = []
    for i in range(staringNum, endingNum):
        try:
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
                # Download the image
                urllib.request.urlretrieve("https://"+comicURL,ext)

        except Exception as e:
            if DEBUG:
                print (e)
            print("Error Page: ", i)

    # Return list object for master census.
    return lst



def makeCensus(lst):
    '''
    Makes a text file with all descriptions and alt-text
    :param lst: 
    :return: 
    '''
    file = open("Master.txt", "w")
    for elem in lst:
        file.write("Image: "+elem[0]+"\n")
        file.write("Alt: "+elem[1]+"\n")
        file.write("Title: "+elem[2]+"\n")
        file.write("\n")
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
