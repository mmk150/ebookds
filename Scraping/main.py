import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc
import bs4
import re
from locvars import binpath


#inits the webdriver instance
def main_init_driver():
    proxy_out_port = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
    dcap=DesiredCapabilities.CHROME
    dcap["pageLoadStrategy"]="eager"
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--proxy-server=%s" % proxy_out_port)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=chrome_options,desired_capabilities=dcap,
                       driver_executable_path=binpath, version_main=112)
    driver.set_page_load_timeout(35)
    return driver

#loads page from url and scrolls down
def load_page(url):
    driver = main_init_driver()
    driver.get(url)
    response = driver.page_source
    waittime = random.random() + .5
    scroll = uc.selenium.webdriver.ActionChains(driver).pause(1.5 + waittime)
    scroll.perform()
    scroll = uc.selenium.webdriver.ActionChains(driver).pause(waittime+random.random()/2).send_keys('\ue010').pause(
        waittime+random.random()/2)
    scroll.perform()
    driver.quit()
    return response


def get_title_tag(soup):
    #Extracts the title tag from the soup object.
    titletag = "Error : Unknown Title : Unknown Author : Unknown Store"
    try:
        titles = soup.find_all("span", attrs={"id": "productTitle"})
        for t in titles:
            if t.text != "":
                titletag = t.text
                break
    except:
        titletag = "ERROR"
    return titletag


def get_author(soup):
    #Extracts the author from the title tag.
    author = []
    try:
        tags = soup.find_all("span", attrs={"class": "author notFaded"})
        print(tags)
        print(tags[0])
        for subtags in tags:
            author = subtags.find_all("a", attrs={"class": "a-link-normal"})[0]
            if author.text != "":
                author.append(y.text.strip())
    except:
        author = "ERROR"
    return author


def get_title(soup):
    #Extracts the title from the title tag.
    title = get_title_tag(soup)
    return title


def get_product_details(soup):
    #Extracts the product details from the soup object.
    try:
        bullets_div = soup.find(id="detailBullets_feature_div")
        ul = bullets_div.find("ul")
        list_items = ul.find_all("li")
        product_details = {}
        for li in list_items:
            try:
                key = (
                    li.find("span", class_="a-text-bold")
                    .decode_contents()
                    .split("\n")[0]
                    .strip()
                ) + ":"
                spans = li.find_next("span").decode_contents().split("<span>")
                value = spans[-1].split("<")[0].strip()
                if key not in product_details:
                    product_details[key] = value
            except Exception as e:
                print(e)
    except:
        product_details = "ERROR"
    return product_details


def get_rankings(soup):
    #Extracts the rankings from the soup object.
    try:
        spans = soup.find_all("span")
        rankings_list_alpha = ["No Rankings"]
        for span in spans:
            if "Best Sellers Rank:" in span.text and "a-text-bold" in span["class"]:
                rankings_list_alpha = span.parent.contents
        for i in range(len(rankings_list_alpha)):
            if (
                rankings_list_alpha[i].__class__ == bs4.element.Tag
                or rankings_list_alpha[i].__class__ == bs4.element.NavigableString
            ):
                rankings_list_alpha[i] = rankings_list_alpha[i].text
        for i in rankings_list_alpha:
            if not re.search(r"\w", i):
                rankings_list_alpha.remove(i)
                continue
            else:
                i = i.strip()
        rankings_list_beta = []
        for i in rankings_list_alpha:
            if "#" in i:
                if i.count("#") == 1:
                    rankings_list_beta.append(i.strip())
                else:
                    sub_list = i.split("#")
                    for sub_item in sub_list:
                        rankings_list_beta.append(sub_item.strip())
        for i in rankings_list_beta:
            if not re.search(r"\d", i):
                rankings_list_beta.remove(i)
        rankings_dictionary = {}
        for i in rankings_list_beta:
            rankings_dictionary[i.split(" in ")[1].strip()] = i.split(" in ")[
                0].strip("# ")
        rank_list=[]
        for i in rankings_dictionary:
            rank_list.append(f"{i}: {rankings_dictionary[i]}")
    except:
        rank_list = "ERROR"
    return rank_list


def get_stars(soup):
    #Extracts the average star rating from the soup object.
    try:
        stars = soup.find("span", id="acrPopover")["title"].split()[0]
    except:
        stars = "ERROR"
    return stars


def get_reviews(soup):
    #Extracts the number of reviews from the soup object.
    try:
        reviews = soup.find("span", id="acrCustomerReviewText").text.split()[
            0].replace(",", "")
    except:
        reviews = "ERROR"
    return reviews


def get_description(soup):
    #Extracts the item description from the soup object.
    try:
        desc = soup.find("div", class_="a-expander-content")
        true_description = ""
        for item in desc:
            true_description += item.text
    except:
        true_description = "ERROR"
    return true_description


def get_prices(soup):
    #Attempts to extract a small set of prices from the soup object.
    try:
        tags = soup.find("div", attrs={"id": "tmmSwatches"}).text.replace(
            " ", "").replace("\n", "")
        prices = tags
    except:
        prices = "ERROR"
    return prices



def results(soup):
    #Runs the above functions on a BS4 obj and returns the resulting dictionary
    dicty = {}
    dicty.update({"title": get_title(soup)})
    dicty.update({"author": get_author(soup)})
    dicty.update({"product details": get_product_details(soup)})
    dicty.update({"rankings": get_rankings(soup)})
    dicty.update({"stars": get_stars(soup)})
    dicty.update({"reviews": get_reviews(soup)})
    dicty.update({"description": get_description(soup)})
    dicty.update({"prices": get_prices(soup)})
    return dicty


def scrapePage(soupd):
    #Function to actually be exported and called
    rez = results(soupd)
    return rez
