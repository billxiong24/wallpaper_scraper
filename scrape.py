from bs4 import BeautifulSoup
import requests 
from tqdm import tqdm
import sys
import argparse

def check_args(start, end):
    
    if start < 0:
        return False
    if end < 0:
        return False

    if end < start:
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", type=int, default=0, help="Page to start at.")
    parser.add_argument("-e", "--end", type=int, default=394, help="Page to end at.")
    args = parser.parse_args()

    if not check_args(args.start, args.end):
        print "Bad arguments. Exiting..."
        return 1


    print "STARTING PAGE: " + str(args.start)
    print "ENDING PAGE: " + str(args.end)

    BASE_URL="https://interfacelift.com/wallpaper/downloads/date/any/"

    for count in range(args.start, args.end + 1):

        print "------------------------------------------------------------PAGE " + str(count) + "------------------------------------------------------------"
        response = requests.get(BASE_URL + "index" + str(count) + ".html") 
        soup = BeautifulSoup(response.text, 'html.parser')
        previews = soup.findAll("div", {"class": "preview"})

        for prev in previews:
            tag = prev.find("img")
            url = tag['src']
            name=tag['alt']
            name = name.replace(" ", "_") + ".jpg"
            name = name.replace("High-resolution_desktop_wallpaper_", "")
            name = name.replace("//","")
            name = name.replace("/","")
            # make higher resolution
            url = url.replace("672x420", "1920x1080")
            res = requests.get(url, stream=True)
            with open(name, "wb") as handle:
                for data in tqdm(res.iter_content(chunk_size=1024), desc="Downloading: "+url):
                    handle.write(data)

    return 0        


main()
