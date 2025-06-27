import random
import datetime
import os
import shutil
import json
import csv
import re
from urllib import request, response
from linked_list import LinkedList

# Load config:
scriptDir = os.path.dirname(__file__)

configFile = open(file=os.path.join(scriptDir, "config.json"), encoding="utf-8-sig")
config = json.loads(configFile.read())
configFile.close()

personalGreetings = config["personalGreetings"]
birthdayGreetings = config["birthdayGreetings"]
weekdayGreetings = config["weekdayGreetings"]
mondayGreetings = config["mondayGreetings"]
fridayGreetings = config["fridayGreetings"]

# For each name in the names file, check to see if tagged is set to true. If the name is tagged, add it to the tagged list
# along with its birthday in the order it appears in the original file. Otherwise, either append or prepend the name and birthday
# to the shuffle list depending on whether a random value between 0 and 99999 is even or odd. This builds the list in a 
# semi-random order and prevents the need to shuffle the values later on:
namesFile = open(file=os.path.join(scriptDir, "names.csv"), newline="", encoding="utf-8-sig")

tagged: LinkedList = LinkedList()
shuffle: LinkedList = LinkedList()

reader = csv.DictReader(namesFile)

for row in reader:
    if (row["tagged"].lower() == "true"):
        tagged.append({"name": row["name"], "birthday": row["birthday"]})

    elif (random.randint(0, 999999) % 2 == 0):
        shuffle.append({"name": row["name"], "birthday": row["birthday"]})
    
    else:
        shuffle.prepend({"name": row["name"], "birthday": row["birthday"]})

namesFile.close()

# Output each name in the tagged and shuffle lists. Check to see if the birth day and month match today. If they do,
# prepend the name with a greeting from birthdayGreetings. Otherwise, prepend each name with a random value from personalGreetings:
for name in (tagged + shuffle):
        sep = re.search(r"[\\\/,\- ]", name["birthday"]).group() if (re.search(r"[\\\/,\- ]", name["birthday"]) != None) else ""

        if (name["birthday"] == datetime.datetime.now().strftime(f"%m{sep}%d") or 
            name["birthday"] == datetime.datetime.now().strftime(f"%m{sep}%d").replace('0', '')):
            print(f"{random.choice(birthdayGreetings)} {name['name']}!")

        else:
            print(f"{random.choice(personalGreetings)} {name['name']}!")

# Append a message from the weekdayGreetings, mondayGreetings or fridayGreetings array depending on the current day of the week, where
# 0 = Monday and 6 = Sunday.
if (datetime.date.today().weekday() == 0):
    print(f"\n{random.choice(mondayGreetings)}")

elif (datetime.date.today().weekday() == 4):
    print(f"\n{random.choice(fridayGreetings)}")    

else:
    print(f"\n{random.choice(weekdayGreetings)}")

# If downloadImage from config is set to true, attempts to download a value from the specified repository and path:
if (config["downloadImage"]):
    # Uses GitHub API to pull list of images in gif directory of repository. This can be used to dynamically obtain the total number of
    # images in the directory and obtain a download URL for the selected image.
    try:
        branch = (f"?ref={config['branch']}" if config["branch"] != "" else "")

        listURL = "https://api.github.com/repos/" \
            + config['repo'] \
            + "/contents/" \
            + config["path"] \
            + branch
        
        req = request.Request(url=listURL, headers={"Accept": "application/json"}, method="GET")

        with request.urlopen(req) as response:
            gifList = json.loads(response.read().decode("utf-8"))
    
    except Exception as ex:
        print(f"Failed to download list of repository content. Check \"repo\" and \"path\" values in config.json:\n{ex}")

    # Attempt to curl a random gif from the gif directory using the download URL pulled above:
    try:
        downloadURL = random.choice(gifList)["download_url"] 
        req = request.Request(url=downloadURL, headers={"Accept": "image/*"}, method="GET")
        imageFile = open(file=os.path.join(scriptDir, "tmp.gif"), mode="wb+")

        with request.urlopen(req) as response:
            shutil.copyfileobj(response, imageFile)

        imageFile.close()

    except Exception as ex:
        print(f"Failed to download GIF image:\n{ex}")
