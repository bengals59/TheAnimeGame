""" Creates a webcrawler that scraps all the info that i need from and exports to a CSV File """

import sys
import bs4 as bs
import requests
import re
import time


#Using these to count run count and current sleep time every 20 successful runs we will set it back down to 0
timeToSleep = 0.1
runCount = 0


my_Url = 'https://myanimelist.net/character.php?letter=A'

whole_Website = requests.get(my_Url).text  ##Finds Website
soup = bs.BeautifulSoup(whole_Website, "html.parser")  ## turns it into a BS object

# Create CSV
filename = "The Game2.csv "
f = open(filename, mode="w",encoding='utf-8') #git remote add origin https://github.com/bengals59/AnimeGame.git
headers = "Character_Name, Favorites, image link\n"
f.write(headers)

table_rows_container = soup.find_all('tr')  ##Kind of finds the the bbest option.

for containers in table_rows_container[1:]:  ## makes all the containers into links

    link = containers.td.a.get('href')  ##gets links to characters
    #Getting request
    request = requests.get(link)

    #Handling response codes
    while not request.ok:
        timeToSleep += 1
        print("ERROR: Response code: " + str(request.status_code) + " waiting " + str(timeToSleep) + " seconds.")
        time.sleep(timeToSleep)
        request = requests.get(link)


    character_Page = request.text ##finds character page
    character_Soup = bs.BeautifulSoup(character_Page, "html.parser")  ## turns it into a bs object

    #Checks if character is in an anime
    #Probably can do better pattern matching, but this should get you started.
    bAnimeography = ('Animeography</div>\n\t\t<table border="0" cellpadding="0" cellspacing="0" width="100%">None').encode(request.encoding)
    if request.content.find(bAnimeography) != -1:
        print("Character not in an anime, skipping")
        continue

    find_Name = character_Soup.findAll("h1", {"class", "h1"})  ##locates character name

    #outputs character name. Has space at start sometimes. Regex to remove
    real_Name = re.sub('^\s', '', find_Name[0].text)
    #Removing double spaces
    real_Name = re.sub('\s\s+', ' ', find_Name[0].text)
    find_Show = character_Soup.findAll('div', {'class': 'normal_header'})
    real_Show = find_Show[1].text

    ###print(show_Manga_Container)
    show_Manga_Container = character_Soup.findAll("tr")

    for info in show_Manga_Container[0:1]:  ##finds link
        showlink = info.td.a.find()  ## gets pitcutre characterlink
        character_Img = str(showlink.get('src'))  ## saves just character link

    ##Turn the Website into text
    textWebsite = character_Soup.get_text()

    ##Find the index of number of favorites
    position_of_Text = textWebsite.index('Member Favorites:')

    #Finds number of Number of favorites
    character_Favorites = textWebsite[position_of_Text + 17:position_of_Text + 24]
    favCount = re.sub('[^0-9]', '',character_Favorites)

    #Printing Char Name, Image Link, Fav Count
    sys.stdout.buffer.write((real_Name + '\n').encode('utf-8'))
    sys.stdout.buffer.write((real_Show + '\n').encode('utf-8'))
    sys.stdout.buffer.write((character_Img + '\n').encode('utf-8'))
    print(favCount)

    if runCount > 10:
        runCount = 0
        timeToSleep = 0.1
    #Sleeping on completion so we don't get locked out.
    time.sleep(timeToSleep)
    runCount += 1

    """f.write(real_Name.replace(",", "") + ", " + character_Img + ", " + final_Character_Favortites.replace("\n", '') + "\n")

f.close()"""

"""1
 'my_Url = 'https://myanimelist.net/character.php'

whole_Website = urllib.request.urlopen(my_Url).read()  ##Finds Website
soup = bs.BeautifulSoup(whole_Website,"html.parser") ## turns it into a BS object

containers = soup.findAll('tr', {"class": "ranking-list"}) ##Finds each name on the page
##print(len(containers))

##print(containers[0])
filename = "The Game.csv "
f = open(filename, "w")
headers = "Character_Name, Name_of_Show, Favorites\n"

f.write(headers)
for container in containers:
    find_Name = container.findAll("a", {"class": "fs14 fw-b"}) ##Finds the HTML NAME
    real_Name = find_Name[0].text ##returns the Name

    find_Favorites = container.findAll("td", {"class": "favorites"}) ##Finds the html Favorites
    real_Favorites = find_Favorites[0].text.strip()  ##prints the number of favorite

    find_Show = container.findAll("div", {"class": "title"}) ##Finds the html name of show
    real_Show = find_Show[0].text ##prints the name of the show

    find_Link = container.findAll("div", {"class": "information"})
    real_Link = find_Link[0].link

    print(real_Name)
    print(real_Favorites)
    print(real_Show)
    print(find_Link)

    f.write(real_Name.replace(",", "") + "," + real_Show + "," + real_Favorites.replace(",", "") + "\n")

f.close()"""

"""
This works
##print(soup)

##Turn the Website into text
textWebsite = soup.get_text()

##Find the index of number of favorites

position_of_Text = textWebsite.index('Member Favorites:')

## Prints Number of favorites
print(textWebsite[position_of_Text+17:position_of_Text+26])"""
