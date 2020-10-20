import bs4 as bs
from urllib.request import Request, urlopen

def parseWeapon(URL):
    weaponParseReq = Request(URL, headers = {"User-Agent": "Mozilla/5.0"})
    weaponPage = urlopen(weaponParseReq).read()
    weaponSoup = bs.BeautifulSoup(weaponPage, "lxml")

    tempString = "https://www.realmeye.com/wiki/"
    name = URL

    name = name.replace(tempString, "")
    print(name)
    img = weaponSoup.findAll("img")
    imgURL = ""
    for j in range(len(img)):
        if img[j].get("alt").replace(" ", "-").lower() == name:
            imgURL = "https:" + img[j].get("src")
            break
    weaponDict = {"Name": name.replace("-", " "),"Img": imgURL, "Tier": -1, "Shots": -1, "Damage": -1, "Rate of Fire": 1.0}
    weapon = weaponSoup.getText().split("\n")
    for i in range(len(weapon) - 1):
        if weapon[i] == "Tier":
            if (weapon[i+1]).isdigit():
                weaponDict["Tier"] = int (weapon[i+1])
            elif "UT" in weapon[i+1]:
                weaponDict["Tier"] = "UT"
            elif "ST" in weapon[i+1]:
                weaponDict["Tier"] = "ST"
            else:
                raise ValueError
        elif weapon[i] == "Shots":
            if " " in weapon[i+1]:
                shotsParse = weapon[i + 1].split(" ")
            else:
                shotsParse = weapon[i + 1].split(" ")
            if (shotsParse[0].isdigit()):
                weaponDict["Shots"] = int(shotsParse[0])
            else:
                raise ValueError
        elif weapon[i] == "Damage":
            lowHighPull = weapon[i+1].split(" ")
            lowHighPull = lowHighPull[0].split("–")
            lowHigh = [lowHighPull[0], lowHighPull[1]]
            if (lowHigh[0].isdigit() and lowHigh[1].isdigit()):
                weaponDict["Damage"] = lowHigh
            else:
                raise ValueError
        elif weapon[i] == "Rate of Fire":
            if weapon[i+1][-1] == "%":
                rofPull = weapon[i+1][:-1]
                rofPull = float (rofPull)/100
                weaponDict["Rate of Fire"] = rofPull
            else:
                raise ValueError
        elif weapon[i] == "On Equip":
            statsDict = {"HP": 0, "MP": 0, "ATT": 0, "DEF": 0, "DEX": 0, "SPD": 0, "WIS": 0, "VIT": 0}
            stats = weapon[i + 1].split(",")
            for j in range(len(stats)):
                if "HP" in stats[j]:
                    statsDict["HP"] = float(stats[j].replace(" HP", ""))
                elif "MP" in stats[j]:
                    statsDict["MP"] = float(stats[j].replace(" MP", ""))
                elif "ATT" in stats[j]:
                    statsDict["ATT"] = float(stats[j].replace(" ATT", ""))
                elif "DEF" in stats[j]:
                    statsDict["DEF"] = float(stats[j].replace(" DEF", ""))
                elif "DEX" in stats[j]:
                    statsDict["DEX"] = float(stats[j].replace(" DEX", ""))
                elif "SPD" in stats[j]:
                    statsDict["SPD"] = float(stats[j].replace(" SPD", ""))
                elif "WIS" in stats[j]:
                    statsDict["WIS"] = float(stats[j].replace(" WIS", ""))
                elif "VIT" in stats[j]:
                    statsDict["VIT"] = float(stats[j].replace(" VIT", ""))
            weaponDict["Stats"] = statsDict
    print(weaponDict)
    return weaponDict

def parseWeapons():
    URLarray = ["daggers", "bows", "staves", "wands", "swords", "katanas"]
    weapons_dict = {}
    for i in URLarray :
        weapons_dict.add({i: {}})
    for j in URLarray:
        req = Request('https://www.realmeye.com/wiki/' + j, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        thisURL = "https://www.realmeye.com"
        for i in test:
            if (i.text == ""):
                thisURL = thisURL + i.get("href")
                temp = parseWeapon(thisURL)
                if (temp["Tier"] == "UT" | temp["Tier"] == "ST"):
                    weapons_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    weapons_dict[j][temp["Tier"]]["Tiered"] = temp
    return weapons_dict

def parseArmor(URL):
    armorParseReq = Request(URL, headers = {"User-Agent": "Mozilla/5.0"})
    armorPage = urlopen(armorParseReq).read()
    armorSoup = bs.BeautifulSoup(armorPage, "lxml")

    tempString = "https://www.realmeye.com/wiki/"
    name = URL
    name = name.replace(tempString, "")

    img = armorSoup.findAll("img")
    imgURL = ""
    for j in range(len(img)):
        if img[j].get("alt").replace(" ", "-").lower() == name:
            imgURL = "https:" + img[j].get("src")
            break
    armorDict = {"Name": name, "Img": imgURL, "Tier": -1, "Stats": -1}
    armor = armorSoup.getText().split("\n")
    for i in range(len(armor)):
        if armor[i] == "Tier":
            if (armor[i + 1]).isdigit():
                armorDict["Tier"] = int(armor[i + 1])
            elif "UT" in armor[i + 1]:
                armorDict["Tier"] = "UT"
            elif "ST" in armor[i + 1]:
                armorDict["Tier"] = "ST"
            else:
                raise ValueError
        elif armor[i] == "On Equip":
            statsDict = {"HP": 0, "MP": 0, "ATT": 0, "DEF": 0, "DEX": 0, "SPD": 0, "WIS": 0, "VIT": 0}
            stats = armor[i+1].split(",")
            for j in range(len(stats)):
                if "HP" in stats[j]:
                    statsDict["HP"] = float(stats[j].replace(" HP", ""))
                elif "MP" in stats[j]:
                    statsDict["MP"] = float(stats[j].replace(" MP", ""))
                elif "ATT" in stats[j]:
                    statsDict["ATT"] = float(stats[j].replace(" ATT", ""))
                elif "DEF" in stats[j]:
                    statsDict["DEF"] = float(stats[j].replace(" DEF", ""))
                elif "DEX" in stats[j]:
                    statsDict["DEX"] = float(stats[j].replace(" DEX", ""))
                elif "SPD" in stats[j]:
                    statsDict["SPD"] = float(stats[j].replace(" SPD", ""))
                elif "WIS" in stats[j]:
                    statsDict["WIS"] = float(stats[j].replace(" WIS", ""))
                elif "VIT" in stats[j]:
                    statsDict["VIT"] = float(stats[j].replace(" VIT", ""))
            armorDict["Stats"] = statsDict
    print(armorDict)
    return armorDict

def parseArmors():
    url_array = ["leather-armors", "robes", "heavy-armors"]
    armors_dict = {}
    for i in url_array:
        armors_dict.add({i: {}})
    for j in url_array:
        req = Request("https://www.realmeye.com/wiki/" + j, headers = {"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        thisURL = "https://www.realmeye.com"
        for i in test:
            if (i.text == ""):
                thisURL = thisURL + i.get("href")
                temp = parseArmor(thisURL)
                if (temp["Tier"] == "UT" or temp["Tier"] == "ST"):
                    armors_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    armors_dict[j][temp["Tier"]]["Tiered"] = temp
    return armors_dict

def parseAbilities():
    url_array = ["cloaks", "quivers", "spells", "tomes", "helms", "shields", "seals", "poisons", "skulls", "traps",
                 "orbs", "prisms", "scepters", "stars", "wakizashi", "lutes"]
    abilities_dict = {}
    for i in url_array:
        abilities_dict.add({i: {}})
    for j in url_array:
        req = Request("https://www.realmeye.com/wiki/" + j, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        thisURL = "https://www.realmeye.com"
        for i in test:
            if (i.text == ""):
                thisURL = thisURL + i.get("href")
                temp = parseArmor(thisURL)
                if (temp["Tier"] == "UT" or temp["Tier"] == "ST"):
                    abilities_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    abilities_dict[j][temp["Tier"]]["Tiered"] = temp
    return abilities_dict

def parseRings():
    url_array = [["health", "magic", "attack", "defense", "speed", "dexterity", "vitality", "wisdom"], "untiered", "limited"]
    rings_dict = []
    for i in range(len(url_array)):
        if i == 0:
            rings_dict.add({"tiered":{}})
        else:
            rings_dict.add({url_array[i]:{}})
    for j in range(len(url_array) + 8):
        temp1 = ""
        if (j < 8):
            val = "tiered"
            temp1 = url_array[0][j]
        elif j == 8:
            val = "untiered"
            temp1 = url_array[1]
        else:
            val = "limited"
            temp1 = url_array[2]
        temp1 = temp1 + "-rings"
        req = Request("https://www.realmeye.com/wiki/" + temp1, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        thisURL = "https://www.realmeye.com"
        for i in test:
            if (i.text == ""):
                thisURL = thisURL + i.get("href")
                temp = parseArmor(thisURL)
                if (temp["Tier"] == "UT" or temp["Tier"] == "ST"):
                    rings_dict[val][temp["Tier"]][temp["Name"]] = temp
                else:
                    rings_dict[val][temp["Tier"]]["Tiered"] = temp
    return rings_dict

def calculateDPS(weapon, ring, armor, ability, stats):
    player_stats = stats
    for i in stats:
        player_stats[i] = player_stats[i] + ring[i] + ability[i] + armor[i] + weapon["Stats"][i]

def parseAll():
    all_equipables = {}
    types = ["Weapons", "Armors", "Abilities", "Rings"]
    for i in types:
        all_equipables.add({i:{}})
    all_equipables["Weapons"] = parseWeapons()
    all_equipables["Armors"] = parseArmors()
    all_equipables["Abilities"] = parseAbilities()
    all_equipables["Rings"] = parseRings()
