import bs4 as bs
from urllib.request import Request, urlopen

def parseWeapon(URL):
    weaponParseReq = Request(URL, headers = {"User-Agent": "Mozilla/5.0"})
    weaponPage = urlopen(weaponParseReq).read()
    weaponSoup = bs.BeautifulSoup(weaponPage, "lxml")
    tempString = "https://www.realmeye.com/wiki/"
    name = URL
    name = name.replace(tempString, "")
    weaponDict = {"Name": name.replace("-", " "),"Tier": -1, "Shots": -1, "Damage": -1, "Rate of Fire": 1.0}
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
                if (temp["Tier"] is "UT" | temp["Tier"] is "ST"):
                    weapons_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    weapons_dict[j][temp["Tier"]]["Tiered"] = temp
