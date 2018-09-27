# Script to download wallpapers from Interfacelift.com
# There are currently 395 pages of wallpapers. 
# Downloads wallpapers in 1920x1080 resolution.

from bs4 import BeautifulSoup
import requests 
from tqdm import tqdm
import base64

def check_args(start, end):
    if start < 0:
        return False
    if end < 0:
        return False

    if end < start:
        return False
    
    return True

def scrape(start, end):

    if start is None:
        start = ['0']
    if end is None:
        end = ['395']

    print("STARTING PAGE: " + start[0])
    print("ENDING PAGE: " + end[0])

    #TODO ERROR HANDLING
    start = int(start[0])
    end = int(end[0])

    BASE_URL="https://interfacelift.com/wallpaper/downloads/date/any/"

    file_list = []

    for count in range(start, end + 1):
        print( "------------------------------------------------------------PAGE " + str(count) + "------------------------------------------------------------")
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
            ret_data=""
            # write image to file
            for data in tqdm(res.iter_content(chunk_size=1024), desc="Downloading: "+url):
                # handle.write(data)
                ret_data += data


            # need to encode binary to base64 so json can serialize it
            # JSON can't serialize raw binary cuz not unicode
            file_list.append({
                'name' : name,
                'data' : base64.encodestring(bytes(ret_data))
                })

    return file_list


# if __name__ == "__main__":
    # main()
