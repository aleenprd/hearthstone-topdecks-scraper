"""Methods related to scraping."""


# IMPORTING PACKAGES
# -------------------------------------- #
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from typing import Dict, List
import numpy as np
from tqdm import tqdm
from time import sleep
import traceback 


def make_soup(url: str) -> str:
    """Return an HTML body from an URL."""
    html = urlopen(url).read()

    return BeautifulSoup(html, 'lxml')


def clean_text(txt: str) -> str:
    """Clean the text and return a readable format."""
    # Remove text formatting
    txt = txt.replace("\n", " ")
    txt = txt.replace("\r", " ")
    txt = txt.replace(u"\xa0", " ")
    # Remove excess whitespace
    txt = re.sub("\s\s+", " ", txt)
    # Remove trailing whitespaces
    txt = txt.strip()

    return txt


def get_class(details: Dict) -> List:
    """Deal with special case of dual-class cards."""
    if "Class" in details.keys():
        card_class = [details["Class"]]
    else:
        card_class = details["Classes"]
        card_class = card_class.replace(" ", "")
        card_class = card_class.split(",")

    return card_class


def get_common_card_info(details: Dict) -> List:
    """Gets the common field which all cards have."""
    # Common information about all cards
    card_type = details["Type"]
    mana_cost = details["Mana Cost"]
    rarity = details["Rarity"]
    card_class = get_class(details)
    card_set = details["Set"]
    if "Mechanics" in details.keys():
        mechanics = details["Mechanics"].split(", ")
    else:
        mechanics = []

    return [card_type, mana_cost, rarity, card_class, card_set, mechanics]


def get_common_card_info_specify_type(details: Dict, card_type: str) -> List:
    """
    Gets the common field which all cards have, but specify type.

    This is due to the fact that some cards are lacking this field.
    """
    # Common information about all cards
    card_type = card_type
    mana_cost = details["Mana Cost"]
    rarity = details["Rarity"]
    card_class = get_class(details)
    card_set = details["Set"]
    if "Mechanics" in details.keys():
        mechanics = details["Mechanics"].split(", ")
    else:
        mechanics = []

    return [card_type, mana_cost, rarity, card_class, card_set, mechanics]


def get_card_rating(soup: BeautifulSoup) -> str:
    """Get the rating of the card."""
    # Not all cards have a rating
    if soup.find("div", {"class": "gdrts-rating-text"}) is not None:
        rating = soup.find("div", {"class": "gdrts-rating-text"}).text
        # The actual rating is hiding in unformatted text
        rating = rating.split("/")
        rating = rating[0].split("Rating: ")
        rating = rating[1]
        rating = float(rating)
    else:
        rating = np.nan

    return rating


def get_num_comments(soup: BeautifulSoup) -> float:
    """Get the number of comments left on a card."""
    # Not all cards have comments
    if soup.find("div", {"class": "comments-title-wrap"}) is not None:
        # Number is hiding in unformatted text
        num_comments = soup.find("div", {"class": "comments-title-wrap"}).text
        num_comments = clean_text(num_comments)
        num_comments = num_comments.split(" ")
        num_comments = num_comments[0]
        if num_comments == "One":  # Ugly fix :(
            num_comments = 1
    else:
        num_comments = 0

    return num_comments


def get_info_by_type(card_type: str, details: Dict) -> List:
    """Gets fields relevant to the type of card or initializes missing."""
    # Based on the type of card, we need to extract
    # some different type of fields
    if card_type == "Minion":
        attack = details["Attack"]
        health = details["Health"]
        school = ""
        durability = np.nan
    elif card_type == "Spell":
        attack = np.nan
        health = np.nan
        if "School" in details.keys():  # Some spells have no type
            school = details["School"]
        else:
            school = "No spell type"
        durability = np.nan
    elif card_type == "Hero":
        attack = np.nan
        health = np.nan
        school = ""
        durability = np.nan
    elif card_type == "Weapon":
        attack = details["Attack"]
        health = np.nan
        school = ""
        durability = details["Durability"]
    else:  # Technically shouldn't get these
        attack = np.nan
        health = np.nan
        school = ""
        durability = np.nan

    return [attack, health, school, durability]


def get_info_by_type_manually(
    card_type: str,
    details: Dict,
    attack: int,
    health: int
) -> List:
    """Gets fields relevant to the type of card or initializes missing."""
    # Based on the type of card, we need to extract
    # some different type of fields
    if card_type == "Minion":
        attack = attack
        health = health
        school = ""
        durability = np.nan
    elif card_type == "Spell":
        attack = np.nan
        health = np.nan
        if "School" in details.keys():  # Some spells have no type
            school = details["School"]
        else:
            school = "No spell type"
        durability = np.nan
    elif card_type == "Hero":
        attack = np.nan
        health = np.nan
        school = ""
        durability = np.nan
    elif card_type == "Weapon":
        attack = attack
        health = np.nan
        school = ""
        durability = details["Durability"]
    else:  # Technically shouldn't get these
        attack = np.nan
        health = np.nan
        school = ""
        durability = np.nan

    return [attack, health, school, durability]


def get_comments(soup: BeautifulSoup) -> List:
    """Get the comment section as a list of strings."""
    # Not all cards have a comment section
    if soup.find_all("li", {"itemtype": "//schema.org/Comment"}) is not None:
        # Initialize empty list for comments
        comments = []

        # Retrieve the comment section
        comment_section = soup.find_all(
            "li", {"itemtype": "//schema.org/Comment"})

        # Parse each comment div tag
        for row in comment_section:
            # Extract the full text from the HTML of each comment
            comment = row.text
            # The comment is split into sections
            # using newline, which is very unstructured
            comment = comment.split("\n\n")
            # Out of these sections, we need the ante-penultimate
            comment = comment[5]
            # Finally apply cleaning to the comment
            comment = clean_text(comment)
            # Append the comment to the comment list
            comments.append(comment)

        # Remove duplicate comments
        if len(comments) > 0:
            comments = list(set(comments))
        else:
            comments = []
    else:
        comments = []

    return comments


def scrape_card(url: str) -> Dict:
    """
    Scrape a Hearthstone card of card information.

    # Example: Spell
    url = "https://www.hearthstonetopdecks.com/cards/bloodlust/"
    scr.scrape_card(url)

    # Example: Minion
    url = "https://www.hearthstonetopdecks.com/cards/hollow-abomination/"
    scr.scrape_card(url)

    # Example: Hero
    url = "https://www.hearthstonetopdecks.com/cards/dreadlich-tamsin/"
    scr.scrape_card(url)

    # Example: Weapon
    url = "https://www.hearthstonetopdecks.com/cards/runed-mithril-rod/"
    scr.scrape_card(url)
    """
    # Fetch HTML
    soup = make_soup(url)

    # Fetch card title
    title = soup.find("h1", {"class": "entry-title"}).text

    # Retrieve general card info
    general = soup.find("div", {"class": "card-content"}).text
    general = general.split("Card Text")
    summary = clean_text(general[0])
    if len(general) > 1:  # Sometimes missing
        text = clean_text(general[1])
    else:
        text = ""

    # Retrieve card details
    specific = soup.find_all("div", {"class": "col-md-14"})

    # Get the text from the table
    for row in specific:
        cells = [i.text for i in row.find_all('li')]

    # We will store fields in a dictionary
    details = {}

    # Parse the cells
    for cell in cells:
        detail = cell.split(": ")
        details[detail[0]] = detail[1]

    # Get the common fields
    card_type, mana_cost, rarity, card_class, card_set, \
        mechanics = get_common_card_info(details)

    # Get card rating
    rating = get_card_rating(soup)

    # Get number of comments
    num_comments = get_num_comments(soup)

    # Get comment section
    comments = get_comments(soup)

    # Get different fields according to the type of the card
    attack, health, school, durability = get_info_by_type(card_type, details)

    # The output will be given in this format
    card = {
        # Common features
        "title": title,
        "summary": summary,
        "text": text,
        "type": card_type,
        "cost": float(mana_cost),
        "rarity": rarity,
        "class": card_class,
        "set": card_set,
        "mechanics": mechanics,
        "rating": float(rating),
        "num_comments": float(num_comments),
        "comments": comments,
        # Minion specific features
        "attack": float(attack),
        "health": float(health),
        # Spell specific features
        "school": school,
        # Weapon specific features
        "durability": float(durability)
    }

    return card


def scrape_card_manually(
    url: str,
    card_type: str,
    attack: int,
    health: int
) -> Dict:
    """
    Scrape a Hearthstone card specifying its type manually.

    A few cards have no specified type and attack/health and
    they are of multiple actual types. Hence, if we want to
    include everything we need to do so manually.

    # Examples:
    "https://www.hearthstonetopdecks.com/cards/siegebreaker/"
    "https://www.hearthstonetopdecks.com/cards/subject-9/"
    "https://www.hearthstonetopdecks.com/cards/breath-of-the-infinite/"

    """
    # Fetch HTML
    soup = make_soup(url)

    # Fetch card title
    title = soup.find("h1", {"class": "entry-title"}).text

    # Retrieve general card info
    general = soup.find("div", {"class": "card-content"}).text
    general = general.split("Card Text")
    summary = clean_text(general[0])
    if len(general) > 1:  # Sometimes missing
        text = clean_text(general[1])
    else:
        text = ""

    # Retrieve card details
    specific = soup.find_all("div", {"class": "col-md-14"})

    # Get the text from the table
    for row in specific:
        cells = [i.text for i in row.find_all('li')]

    # We will store fields in a dictionary
    details = {}

    # Parse the cells
    for cell in cells:
        detail = cell.split(": ")
        details[detail[0]] = detail[1]

    # Get the common fields
    card_type, mana_cost, rarity, card_class, card_set, \
        mechanics = get_common_card_info_specify_type(details, card_type)

    # Get card rating
    rating = get_card_rating(soup)

    # Get number of comments
    num_comments = get_num_comments(soup)

    # Get comment section
    comments = get_comments(soup)

    # Get different fields according to the type of the card
    attack, health, school, durability = get_info_by_type_manually(
        card_type,
        details,
        attack,
        health)

    # The output will be given in this format
    card = {
        # Common features
        "title": title,
        "summary": summary,
        "text": text,
        "type": card_type,
        "cost": float(mana_cost),
        "rarity": rarity,
        "class": card_class,
        "set": card_set,
        "mechanics": mechanics,
        "rating": float(rating),
        "num_comments": float(num_comments),
        "comments": comments,
        # Minion specific features
        "attack": float(attack),
        "health": float(health),
        # Spell specific features
        "school": school,
        # Weapon specific features
        "durability": float(durability)
    }

    return card


def get_num_query_pages(url: str) -> int:
    """Get the number of result pages from a query."""
    # Get html
    soup = make_soup(url)

    # Fetch html tag
    num_pages = soup.find("span", {"class": "page-link"}).text
    num_pages = num_pages.split(" ")
    num_pages = int(num_pages[2])

    return num_pages


def get_url_at_page_number(url: str, counter: int) -> str:
    """Retrieves the link to the next result page of a query."""
    # All result pages will start out like this
    root_url = "https://www.hearthstonetopdecks.com/cards/"

    # Fhe first page of the query is followed by a string
    # describing your query options, like this
    query_url = url.split(root_url)[1]

    # But subsequent pages have text describing the page number
    # in between the rool url and the query text, as such:
    next_url = f"page/{counter}/"

    # Finally, reconstruct the next URL
    return root_url + next_url + query_url


def get_page_card_urls(url: str) -> List:
    """
    Parse the website and fetch all card URLs
    from a given query, on a single page.

    ATTENTION: Must select query to be displayed
    as a table. This is in order to show more cards
    on a single page, and also, for easier URL fetching.
    """
    # Initialize output
    card_url_list = []

    # Get html
    soup = make_soup(url)

    # Parse the HTML a tag and fetch the hrefs
    page_links = soup.find_all("a", {"class": "card-link"})
    for link in page_links:
        card_url_list.append(str(link["href"]))

    return card_url_list


def parse_query_and_fetch_links(url: str, sleep_time: int) -> List:
    """
    Parse all pages in a filtered query on
    HSTD and retrieves links to cards.

    ATTENTION: Must select query to be displayed
    as a table. This is in order to show more cards
    on a single page, and also, for easier URL fetching.
    """
    # Initialize output
    complete_url_list = []

    # Find out number of result pages to parse
    num_pages = get_num_query_pages(url)

    # Parse the pages from beginning to end
    for i in tqdm(range(1, num_pages+1)):
        current_page = get_url_at_page_number(url, i)

        current_url_list = get_page_card_urls(current_page)

        for element in current_url_list:
            complete_url_list.append(element)

        # Optional, if we want to be ethical
        # and not overload the targeted server
        sleep(sleep_time)

    # Just in case we have duplicates
    complete_url_list = list(set(complete_url_list))

    return complete_url_list


def scrape_multiple_cards(url_list: List, sleep_time: int) -> List:
    """Scrape a list of URLs corresponding to cards."""
    # Initialize output
    card_list = []

    # Initialize list of failed scrapes 
    # for later debugging 
    failed_card_list = []

    # Parse list of links
    for url in tqdm(url_list):
        try:
            card = scrape_card(url)
            card_list.append(card)
            sleep(sleep_time)
        except Exception:
            print(f"\nScript failed at URL {url}")
            print(traceback.format_exc())
            failed_card_list.append(url)
            pass  # Not actually bad practice if we know the errors. ;)

    return card_list, failed_card_list
