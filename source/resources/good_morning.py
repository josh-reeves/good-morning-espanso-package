import random
import datetime
import os
import shutil
import json
from urllib import request, response
from linked_list import LinkedList

# Load config:
scriptDir = os.path.dirname(__file__)
config = json.loads(open(file=os.path.join(scriptDir, "config.json"), encoding="utf-8-sig").read())

tagChar: str = config["tagChar"]

personalGreetings = config["personalGreetings"]
weekdayGreetings = config["weekdayGreetings"]
mondayGreetings = config["mondayGreetings"]
fridayGreetings = config["fridayGreetings"]

# For each name in the names file, check to see if the name includes tagChar. If the name is tagged, add it to the tagged list in the 
# order it appears in the original file. Otherwise, either append or prepend the name to the shuffle list depending on whether a 
# random value between 0 and 99 is even or odd. This builds the list in a semi-random order and prevents the need to shuffle the 
# values later on:
namesFile = open(file=os.path.join(scriptDir, "names.txt"), encoding="utf-8-sig")

tagged: LinkedList = LinkedList()
shuffle: LinkedList = LinkedList()

for name in namesFile:
    if (name.__contains__(tagChar)):
        tagged.append(name[name.index(tagChar)+ 1:].rstrip())
    elif (random.randint(0, 99) % 2 == 0):
        shuffle.append(name.rstrip())
    else:
        shuffle.prepend(name.rstrip())

namesFile.close()

# Output list of names, prepending each with a random value from the personalGreetings array:
for name in (tagged + shuffle):
    print(f"{random.choice(personalGreetings)} {name}!")

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
        listURL =  "https://api.github.com/repos/" + config['repo'] + "/contents" + f"/{config['path']}" if config['path'] != "" else "" + f"?ref={config['branch']}" if config['branch'] != "" else ""
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
