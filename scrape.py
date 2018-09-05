from bs4 import BeautifulSoup
import requests 
from tqdm import tqdm

BASE_URL="https://interfacelift.com/wallpaper/downloads/date/any/"
for count in range(301, 394):

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

