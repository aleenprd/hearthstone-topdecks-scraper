# %%
import sys
from importlib import reload
from utils import scraping as sc
reload(sc)
sys.path.append("../")
# %%
url = "https://www.hearthstonetopdecks.com/cards/ancharrr/"

card = sc.scrape_card(url)
# %%
import urllib.request
urllib.request.urlretrieve(url, "test.png")
# %%
import requests


# %%
https://cdn.hearthstonetopdecks.com/wp-content/uploads/2019/11/Ancharrr-1.png

# %%
import requests

with open('pic1.jpg', 'wb') as handle:
    response = requests.get(url, stream=True)

    if not response.ok:
        print(response)

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)
        
# %%
