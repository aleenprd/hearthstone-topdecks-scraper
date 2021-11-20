# HearthStoneTopDecks Scraper
This repo was designed to scrape information from the website [Hearthstone Top Decks](https://www.hearthstonetopdecks.com/). 

## Background
[Hearthstone](https://playhearthstone.com/) is an online card game designed and published by Activision Blizzard. The game has been around since 2004 and has managed to grow its collection to over 3000 cards. Generally, cards are released at least 3 times a year and everytime they are revealed, the fan community will generally rate and discuss them. One such platform where rating can happen is Hearthstone Top Decks. They have on their website a massive ammount of interesting data including details about each card, comments from the community and ratings. I would like to access all of this data in order to later analyze it.

## How to use
The project is composed of different scripts, relying on utility functions, found in the folder `utils` and on configuration options, found in the folder `config` (modify them for your desired purpose). The different scripts can be run from a CLI i.e.: `python(3) <script-name.py>`.

- Firstly, `get_card_urls.py` will provide you with a way to extract the links to all the cards you want, starting from a query result. For example, you can search for all cards in the 'Standard' set, which belong to the class 'Paladin', like [this](https://www.hearthstonetopdecks.com/cards/?st=&manaCost=&format=standard&rarity=&type=&class=47&set=&mechanic=&race=&orderby=ASC-name&view=table). <b>Important:</b> Make sure to select presenting the results in a table instead of a gallery. Otherwise, the script won't work. This will output a binary file to the `data` folder. It will be containing a list of all the URLs which will be parsed in the next step.
- Secondly, `get_card_info.py` will parse that list and for each URL it will fetch text information on the card including name, summary, card set, cost, card type, review score, comments, etc. All of this information will be structured into a Pandas Dataframe, and then saved in `data` as a CSV file.

<b>Observation:</b> When testing the script out, I opted for scraping the entire website of all cards (excluding generated 'token' cards). I found it to be working almost 100% perfectly, except for 3 cards. The reason is that the wardens of the website ommitted some essential information on those cards, which prevented automated scraping. Consequently, I also scraped those more manually in the `get_card_info_manually.py`. I then merged those cards with the main dataset, using the `merge_datasets.py` script.

## Notes from developer
- The project is public and free to use. Please feel free to contribute to maintaining and expanding this project. If you would like to do so, give me a heads up by sending me a message or an e-mail.
- I will also upload the data I have so you can play around with it. Please let me know what kind of interesting things you can do with it. :) 
