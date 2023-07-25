from locvars import base_url, base_dir
import datetime
import random
from time import sleep
from pathlib import Path

import undetected_chromedriver as uc
from bs4 import BeautifulSoup as soup
from main import *

import json
from stem import Signal
from stem.control import Controller
from locvars import hcp,base_dir


#This is mostly a copy of categories_scrape.py but fine tuned for subcategories. Code replicated out of necessity to decouple the functionality from the category scraping.


def init_driver():
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
    driver.set_page_load_timeout(65)
    return driver

def load_cat_page_one(url):
    with Controller.from_port(port=9051) as c:
        c.authenticate(hcp)
        c.signal(Signal.NEWNYM)
        driver = init_driver()
        try:
            driver.get(url)
            waittime=random.random() +.5
            scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.5 + waittime)
            scroll.perform()
            isPage=False
            count=0
            while not isPage:
                if count>3:
                    c.signal(Signal.NEWNYM)
                    sleep(2)
                source=driver.page_source
                html=soup(source,"html.parser").text
                try:
                    if "throttled" in html and "refresh the page" in html:
                        driver.refresh()
                        sleep(1)
                        scroll= uc.selenium.webdriver.ActionChains(driver).pause(5.2).pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                        scroll.perform()
                    else:
                        isPage=True;
                        scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.2).send_keys('\ue010').pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                        scroll.perform()
                except:
                    pass

        
            response = driver.page_source
            paid_book_page_one_soup = soup(response, "html.parser")
        except:
            paid_book_page_one_soup=[]
        driver.quit()
        return paid_book_page_one_soup

def load_cat_page(url):
    # INIT
    driver = init_driver()

   
    try:
        driver.get(url)
        waittime=random.random() +.5
        scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.5 + waittime)
        scroll.perform()
        isPage=False
        count=0
        while not isPage:
            source=driver.page_source
            html=soup(source,"html.parser").text
            print(html)
            print("throttled" in html)
            print("line 109")
            try:
                if "throttled" in html and "refresh the page" in html:
                    driver.refresh()
                    scroll= uc.selenium.webdriver.ActionChains(driver).pause(9.2)
                    scroll.perform()
                    scroll= uc.selenium.webdriver.ActionChains(driver).pause(5.2).pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                    scroll.perform()
                else:
                    isPage=True;
                    scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.2).send_keys('\ue010').pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                    scroll.perform()
            except:
                pass

        response = driver.page_source
        paid_book_page_one_soup = soup(response, "html.parser")
    except:
        paid_book_page_one_soup=[]

    try:
        pg2href=driver.find_element(By.CLASS_NAME,"a-last")
        pg2href=pg2href.find_element(By.XPATH,"./child::*")
        pg2href=pg2href.click()
        waittime=random.random() +.5
        scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.5 + waittime)
        scroll.perform()

        isPage=False
        count=0
        while not isPage and count<5:
            source=driver.page_source
            html=soup(source,"html.parser").text
            print(html)
            print("throttled" in html)
            print("line 109")
            try:
                if "throttled" in html and "refresh the page" in html:
                    driver.refresh()
                    sleep(1)
                    scroll= uc.selenium.webdriver.ActionChains(driver).pause(5.2).pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                    scroll.perform()
                else:
                    isPage=True;
                    scroll= uc.selenium.webdriver.ActionChains(driver).pause(1.2).send_keys('\ue010').pause(waittime+random.random()/2).pause(waittime +random.random()/3).pause(waittime+random.random()/2)
                    scroll.perform()
            except:
                pass

        response = driver.page_source
        paid_book_page_two_soup = soup(response, "html.parser")

    except:
        paid_book_page_two_soup=[]
    
    
    driver.quit()
    return paid_book_page_one_soup, paid_book_page_two_soup




def top100MainQueue(url=base_url, dir=base_dir):
    soupd1=load_cat_page_one(url)
    time = datetime.datetime.now()
    strtime = time.strftime("%m_%d_%Y")
    currdir = dir + "/" + strtime + "b"
    todo_text = currdir + "/todo2.txt"
    Path(currdir).mkdir(parents=True, exist_ok=True)
    main_dir=currdir + "/Main"
    Path(main_dir).mkdir(parents=True, exist_ok=True)
    main_text = main_dir + "/main.txt"
    todo_file = open(todo_text, 'w', encoding="utf-8")
    main_file = open(main_text, 'w', encoding="utf-8")
   
    bestsellers1=bestsellersClean(soupd1)
    arr=[]
    for key,value in bestsellers1.items():
        tup=("Main:Paid",key,value)
        arr.append(tup)
    for items in arr:
        stringified=items[0] +"^^" + items[1] + "^^" + items[2] + "@@"
        todo_file.write(stringified)
        main_file.write(stringified)
    main_file.close()
    todo_file.close()
    cats_n_links=returnCategories()
    for tup in cats_n_links:
        cat=tup[0]
        link=tup[1]
        top100CatQueue(cat,todo_text=todo_text,url=link,dir=currdir)
    return arr
    


def top100CatQueue(category,todo_text,url, dir):
    if category not in ["Literature & Fiction","Romance","Mystery, Thriller, & Suspense","Science Fiction & Fantasy","Teen & Young Adult","LGBTQ+ eBooks"]:
        return
    soupd1=load_cat_page_one(url)
    print(soupd1)
    if soupd1 is []:
        pg1e=False
    else:
        pg1e=True
    currdir = dir + "/" + category
    Path(currdir).mkdir(parents=True, exist_ok=True)
    todo_file = open(todo_text, 'a', encoding="utf-8")
    cat_top100_path=currdir + "/" + "top50.txt"
    top100_file=open(cat_top100_path,'w',encoding='utf-8')
    arr=[]
    if pg1e:
        bestsellers1=bestsellersClean(soupd1)
        for key,value in bestsellers1.items():
            tup=(category+"PAID",key,value)
            arr.append(tup)
    for items in arr:
        stringified=items[0] +"^^" + items[1] + "^^" + items[2] + "@@"
        todo_file.write(stringified)
        top100_file.write(stringified)
    top100_file.close()
    todo_file.close()
    subcats_n_links=returnSubCategories(category)
    for tup in subcats_n_links:
        subcat=tup[0]
        link=tup[1]
        top100SubCatQueue(category,subcat,currdir,link,todo_text)
    return arr



def top100SubCatQueue(category,subcategory,dir,url,todo):
    soupd1=load_cat_page_one(url)
    if soupd1 is []:
        pg1e=False
    else:
        pg1e=True
    if category not in ["Literature & Fiction","Romance","Mystery, Thriller, & Suspense","Science Fiction & Fantasy","Teen & Young Adult","LGBTQ+ eBooks"]:
        return
    currdir = dir + "/" + subcategory
    Path(currdir).mkdir(parents=True, exist_ok=True)
    todo_file = open(todo, 'a', encoding="utf-8")
    subcat_top100_path=currdir + "/" + "top50.txt"
    top100_file=open(subcat_top100_path,'w',encoding='utf-8')
    arr=[]
    if pg1e:
        bestsellers1=bestsellersClean(soupd1)
        for key,value in bestsellers1.items():
            tup=(subcategory+"PAID",key,value)
            arr.append(tup)
    for items in arr:
        stringified=items[0] +"^^" + items[1] + "^^" + items[2] + "@@"
        todo_file.write(stringified)
        top100_file.write(stringified)
    top100_file.close()
    todo_file.close()
    



# HELPER FUNCTIONS START:

# clean html for bestsellers, save in todo

def bestsellersClean(soupz:soup):
    dictionary=dict()
    if type(soupz) is list:
        return dictionary
    relevant_links = soupz.find_all("a",attrs={"class": "a-link-normal","role": "link"})
    for link in relevant_links:
        href = link.get('href')
        inner_html = link.get_text(strip=True)
        if inner_html!="" and "$" not in inner_html:
            dictionary.update({inner_html: href})
    return dictionary



def sidebarClean(soupz:soup):
    category_html = soupz.find_all("div", {'role': 'treeitem'})
    dictionary=dict()
    for tag in category_html:
        try:
            child_tag=tag.findChildren("a",recursive=False)[0]
            href = child_tag.get('href')
            inner_html = child_tag.text
            if inner_html not in ["Kindle Store", "Any Department"]:
                dictionary.update({inner_html:href})
        except:
           pass
    
    return dictionary


def categories2JSON(dictionary, target_json):
    with open(target_json,'w') as json_file:
        json.dump(dictionary,json_file,indent=4)
    json_file.close()



def returnCategories():
    file_name='categories.json'
    with open(file_name, 'r') as file:
        data = json.load(file)
    cats=data['Categories']
    cats_arr=[]
    for key,val in cats.items():
        cats_arr.append((key,val))
    return cats_arr



def returnSubCategories(category):
    file_name='subcategories.json'
    with open(file_name, 'r') as file:
        data = json.load(file)
    cat_data=data[category]
    subcats_arr=[]
    for item in cat_data:
        full=category + " - " + item['Title'] 
        link=item['Link']
        tup=(full,link)
        subcats_arr.append(tup)
    return subcats_arr

