# Script to download wallpapers from Interfacelift.com
# There are currently 395 pages of wallpapers. 
# Downloads wallpapers in 1920x1080 resolution.

from bs4 import BeautifulSoup
import requests 
from tqdm import tqdm
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
    parser.add_argument("-s", "--start", type=int, default=1, help="Page to start at.")
    parser.add_argument("-e", "--end", type=int, default=395, help="Page to end at.")
    args = parser.parse_args()

    if not check_args(args.start, args.end):
        print "Bad arguments. Exiting..."
        return 1

    print "STARTING PAGE: " + str(args.start)
    print "ENDING PAGE: " + str(args.end)

    BASE_URL="https://interfacelift.com/wallpaper/downloads/date/any/"

    for count in range(args.start, args.end + 1):
        print "------------------------------------------------------------PAGE " + str(count) + "------------------------------------------------------------"
        # fetch html with wallpaper links
        response = requests.get(BASE_URL + "index" + str(count) + ".html") 
        soup = BeautifulSoup(response.text, 'html.parser')
        previews = soup.findAll("div", {"class": "preview"})

        for prev in previews:
            # search for wallpaper links
            tag = prev.find("img")
            url = tag['src']
            name=tag['alt']
            # Don't want spaces in file names
            name = name.replace(" ", "_") + ".jpg"
            name = name.replace("High-resolution_desktop_wallpaper_", "")
            # Some file names include // or /, which is problematic
            name = name.replace("//","")
            name = name.replace("/","")
            # make higher resolution
            url = url.replace("672x420", "1920x1080")
            # streaming request to download image
            res = requests.get(url, stream=True)
            # write image to file
            with open(name, "wb") as handle:
                for data in tqdm(res.iter_content(chunk_size=1024), desc="Downloading: "+url):
                    handle.write(data)

    return 0

if __name__ == "__main__":
    main()
