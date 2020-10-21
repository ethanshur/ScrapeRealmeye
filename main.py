import bs4 as bs
from urllib.request import Request, urlopen


def parse_weapon(url):
    weapon_parse_req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    weapon_page = urlopen(weapon_parse_req).read()
    weapon_soup = bs.BeautifulSoup(weapon_page, "lxml")

    temp_string = "https://www.realmeye.com/wiki/"
    name = url

    name = name.replace(temp_string, "")
    print(name)
    img = weapon_soup.findAll("img")
    img_url = ""
    for j in range(len(img)):
        if img[j].get("alt").replace(" ", "-").lower() is name:
            img_url = "https:" + img[j].get("src")
            break
    weapon_dict = {"Name": name.replace("-", " "), "Img": img_url,
                   "Tier": -1, "Shots": -1, "Damage": -1, "Rate of Fire": 1.0}
    weapon = weapon_soup.getText().split("\n")
    for i in range(len(weapon) - 1):
        if weapon[i] is "Tier":
            if (weapon[i+1]).isdigit():
                weapon_dict["Tier"] = int(weapon[i+1])
            elif "UT" in weapon[i+1]:
                weapon_dict["Tier"] = "UT"
            elif "ST" in weapon[i+1]:
                weapon_dict["Tier"] = "ST"
            else:
                raise ValueError
        elif weapon[i] is "Shots":
            if " " in weapon[i+1]:
                shots_parse = weapon[i + 1].split(" ")
            else:
                shots_parse = weapon[i + 1].split(" ")
            if shots_parse[0].isdigit():
                weapon_dict["Shots"] = int(shots_parse[0])
            else:
                raise ValueError
        elif weapon[i] is "Damage":
            low_high_pull = weapon[i+1].split(" ")
            low_high_pull = low_high_pull[0].split("–")
            low_high = [low_high_pull[0], low_high_pull[1]]
            if low_high[0].isdigit() and low_high[1].isdigit():
                weapon_dict["Damage"] = low_high
            else:
                raise ValueError
        elif weapon[i] is "Rate of Fire":
            if weapon[i+1][-1] is "%":
                rof_pull = weapon[i+1][:-1]
                rof_pull = float(rof_pull)/100
                weapon_dict["Rate of Fire"] = rof_pull
            else:
                raise ValueError
        elif weapon[i] is "On Equip":
            stats_dict = {"HP": 0, "MP": 0, "ATT": 0, "DEF": 0, "DEX": 0, "SPD": 0, "WIS": 0, "VIT": 0}
            stats = weapon[i + 1].split(",")
            for j in range(len(stats)):
                arr = stats[j].split
                stats_dict[arr[1]] = float(arr[0])

                # if "HP" in stats[j]:
                #     statsDict["HP"] = float(stats[j].replace(" HP", ""))
                # elif "MP" in stats[j]:
                #     statsDict["MP"] = float(stats[j].replace(" MP", ""))
                # elif "ATT" in stats[j]:
                #     statsDict["ATT"] = float(stats[j].replace(" ATT", ""))
                # elif "DEF" in stats[j]:
                #     statsDict["DEF"] = float(stats[j].replace(" DEF", ""))
                # elif "DEX" in stats[j]:
                #     statsDict["DEX"] = float(stats[j].replace(" DEX", ""))
                # elif "SPD" in stats[j]:
                #     statsDict["SPD"] = float(stats[j].replace(" SPD", ""))
                # elif "WIS" in stats[j]:
                #     statsDict["WIS"] = float(stats[j].replace(" WIS", ""))
                # elif "VIT" in stats[j]:
                #     statsDict["VIT"] = float(stats[j].replace(" VIT", ""))

            weapon_dict["Stats"] = stats_dict
    print(weapon_dict)
    return weapon_dict


def parse_weapons():
    url_list = ["daggers", "bows", "staves", "wands", "swords", "katanas"]
    weapons_dict = {}
    for i in url_list:
        weapons_dict[i] = {}
    for j in url_list:
        req = Request('https://www.realmeye.com/wiki/' + j, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        this_url = "https://www.realmeye.com"
        for i in test:
            if i.text is "":
                this_url = this_url + i.get("href")
                temp = parse_weapon(this_url)
                # noinspection PyTypeChecker
                if temp["Tier"] is "UT" | temp["Tier"] is "ST":
                    weapons_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    weapons_dict[j][temp["Tier"]]["Tiered"] = temp

    return weapons_dict


def parse_armor(url):
    armor_parse_req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    armor_page = urlopen(armor_parse_req).read()
    armor_soup = bs.BeautifulSoup(armor_page, "lxml")

    temp_string = "https://www.realmeye.com/wiki/"
    name = url
    name = name.replace(temp_string, "")

    img = armor_soup.findAll("img")
    img_url = ""
    for j in range(len(img)):
        if img[j].get("alt").replace(" ", "-").lower() is name:
            img_url = "https:" + img[j].get("src")
            break
    armor_dict = {"Name": name, "Img": img_url, "Tier": -1, "Stats": -1}
    armor = armor_soup.getText().split("\n")
    for i in range(len(armor)):
        if armor[i] is "Tier":
            if (armor[i + 1]).isdigit():
                armor_dict["Tier"] = int(armor[i + 1])
            elif "UT" in armor[i + 1]:
                armor_dict["Tier"] = "UT"
            elif "ST" in armor[i + 1]:
                armor_dict["Tier"] = "ST"
            else:
                raise ValueError
        elif armor[i] is "On Equip":
            stats_dict = {"HP": 0, "MP": 0, "ATT": 0, "DEF": 0, "DEX": 0, "SPD": 0, "WIS": 0, "VIT": 0}
            stats = armor[i+1].split(",")
            for j in range(len(stats)):
                arr = stats[j].split
                stats_dict[arr[1]] = float(arr[0])
                #
                # if "HP" in stats[j]:
                #     stats_dict["HP"] = float(stats[j].replace(" HP", ""))
                # elif "MP" in stats[j]:
                #     stats_dict["MP"] = float(stats[j].replace(" MP", ""))
                # elif "ATT" in stats[j]:
                #     stats_dict["ATT"] = float(stats[j].replace(" ATT", ""))
                # elif "DEF" in stats[j]:
                #     stats_dict["DEF"] = float(stats[j].replace(" DEF", ""))
                # elif "DEX" in stats[j]:
                #     stats_dict["DEX"] = float(stats[j].replace(" DEX", ""))
                # elif "SPD" in stats[j]:
                #     stats_dict["SPD"] = float(stats[j].replace(" SPD", ""))
                # elif "WIS" in stats[j]:
                #     stats_dict["WIS"] = float(stats[j].replace(" WIS", ""))
                # elif "VIT" in stats[j]:
                #     stats_dict["VIT"] = float(stats[j].replace(" VIT", ""))
            armor_dict["Stats"] = stats_dict
    print(armor_dict)
    return armor_dict


def parse_armors():
    url_array = ["leather-armors", "robes", "heavy-armors"]
    armors_dict = {}
    for i in url_array:
        armors_dict[i] = {}
    for j in url_array:
        req = Request("https://www.realmeye.com/wiki/" + j, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        this_url = "https://www.realmeye.com"
        for i in test:
            if i.text is "":
                this_url = this_url + i.get("href")
                temp = parse_armor(this_url)
                if temp["Tier"] is "UT" or temp["Tier"] is "ST":
                    armors_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    armors_dict[j][temp["Tier"]]["Tiered"] = temp
    return armors_dict


def parse_abilities():
    url_array = ["cloaks", "quivers", "spells", "tomes", "helms", "shields", "seals", "poisons", "skulls", "traps",
                 "orbs", "prisms", "scepters", "stars", "wakizashi", "lutes"]
    abilities_dict = {}
    for i in url_array:
        abilities_dict[i] = {}
    for j in url_array:
        req = Request("https://www.realmeye.com/wiki/" + j, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = bs.BeautifulSoup(webpage, "lxml")
        test = soup.findAll("a")
        this_url = "https://www.realmeye.com"
        for i in test:
            if i.text is "":
                this_url = this_url + i.get("href")
                temp = parse_armor(this_url)
                if temp["Tier"] is "UT" or temp["Tier"] is "ST":
                    abilities_dict[j][temp["Tier"]][temp["Name"]] = temp
                else:
                    abilities_dict[j][temp["Tier"]]["Tiered"] = temp
    return abilities_dict


def parse_rings():
    url_array = [["health", "magic", "attack", "defense", "speed", "dexterity", "vitality", "wisdom"],
                 "untiered", "limited"]
    rings_dict = []
    for i in range(len(url_array)):
        if i is 0:
            rings_dict.append({"tiered": {}})
        else:
            rings_dict.append({url_array[i]: {}})
    for j in range(len(url_array) + 8):
        if j < 8:
            val = "tiered"
            temp1 = url_array[0][j]
        elif j is 8:
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
        this_url = "https://www.realmeye.com"
        for i in test:
            if i.text is "":
                this_url = this_url + i.get("href")
                temp = parse_armor(this_url)
                if temp["Tier"] is "UT" or temp["Tier"] is "ST":
                    # noinspection PyTypeChecker
                    rings_dict[val][temp["Tier"]][temp["Name"]] = temp
                else:
                    # noinspection PyTypeChecker
                    rings_dict[val][temp["Tier"]]["Tiered"] = temp
    return rings_dict


def calculate_dps(weapon, ring, armor, ability, stats):
    player_stats = stats
    for i in stats:
        player_stats[i] = player_stats[i] + ring[i] + ability[i] + armor[i] + weapon["Stats"][i]


def parse_all():
    all_equipables = {}
    types = ["Weapons", "Armors", "Abilities", "Rings"]
    for i in types:
        all_equipables[i] = {}

    all_equipables["Weapons"] = parse_weapons()
    all_equipables["Armors"] = parse_armors()
    all_equipables["Abilities"] = parse_abilities()
    all_equipables["Rings"] = parse_rings()


parse_weapon("https://www.realmeye.com/wiki/steel-dagger")
