""" Creates a webcrawler that scraps all the info that i need from and exports to a CSV File """

import urllib.request

import bs4 as bs

my_Url = 'https://myanimelist.net/character.php?letter=A'

whole_Website = urllib.request.urlopen(my_Url).read()  ##Finds Website
soup = bs.BeautifulSoup(whole_Website, "html.parser")  ## turns it into a BS object

# TODO: Fix error that occurs here when parsing Japanese language data
# 'https://myanimelist.net/character/138415/Grace_Aihara'
"""
## Create CSV
filename = "The Game2.csv "
f = open(filename, "w")git remote add origin https://github.com/bengals59/AnimeGame.git
headers = "Character_Name, Favorites, image link\n"
f.write(headers)"""

table_rows_container = soup.find_all('tr')  ##Kind of finds the the bbest option.

for containers in table_rows_container[1:]:  ## makes all the containers into links
    link = containers.td.a.get('href')  ##gets links to characters

    # TODO: Fix UnicodeEncodeError that occurs here, immediately after character 'Miguel, Aiman'
    # UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 43: ordinal not in range(128)
    # See docs here => https://docs.python.org/2.7/howto/unicode.html#the-unicode-type
    character_Page = urllib.request.urlopen(link).read()  ##finds character page
    character_Soup = bs.BeautifulSoup(character_Page, "html.parser")  ## turns it into a bs object

    find_Name = character_Soup.findAll("h1", {"class", "h1"})  ##locates character name
    real_Name = find_Name[0].text  ##outputs character name

    find_Show = character_Soup.findAll('div', {'class': 'normal_header'})
    real_Show = find_Show[1].text

    # TODO: If character is in ONLY Manga, we can just skip over it (Joe 'reeeaally doesn't give a fuck...')
    # Otherwise pull name of show (only first show is needed) and whether character is main or supporting.
    # i.e. skip over => 'https://myanimelist.net/character/86811/Leos_Alloy'
    # i.e. don't skip => 'https://myanimelist.net/character/135321/Alice_Alligator'
    ###print(show_Manga_Container)
    show_Manga_Container = character_Soup.findAll("tr")

    for info in show_Manga_Container[0:1]:  ##finds link
        showlink = info.td.a.find()  ## gets pitcutre characterlink
        character_Img = str(showlink.get('src'))  ## saves just character link

    ##Turn the Website into text
    textWebsite = character_Soup.get_text()

    ##Find the index of number of favorites

    position_of_Text = textWebsite.index('Member Favorites:')

    ## Finds number of Number of favorites
    character_Favorites = textWebsite[position_of_Text + 17:position_of_Text + 24]
    stall_Character_favorites = character_Favorites.replace(",", "")
    final_Character_Favortites = str(stall_Character_favorites)

    ##print(link)
    print(real_Name)  ## prints name of character
    ##print(real_Show)
    print(character_Img)  ##gives link to character image

    print(final_Character_Favortites.replace("\n", ""))  ##print number of favorites

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
