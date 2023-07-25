from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup as soup
from main import *

import csv
from stem import Signal
from stem.control import Controller
from locvars import hcp
import os


dated = "07_05_2023b"
# insert date

path_to_todo = ""
# modify this as necessary

#Quick and slightly modified copy of cleanQ from scrape_todo.py
def cleanQ(date, basedir):

    todopath = basedir + f"/{date}/" + "todo2.txt"
    todofile = open(todopath, 'r', encoding="utf-8")

    everything = todofile.readline()
    everything = everything.split("@@")
    everything = everything[0:len(everything)-1]

    books = dict()
    for i in range(0, len(everything)):
        line = everything[i]
        line = line.split("^^")
        length = len(line)
        category = line[0]
        s = ""
        bookname = [s + elem for elem in line[1:length-1]][0].replace(" ", "")
        urlstub = line[-1]
        bookurl = "https://www.amazon.com" + urlstub
        try:
            bookid = urlstub.split("/dp/")[1].split("/")[0]
        except:
            pass
        catarr = []
        try:
            merp = books[bookid]
            catarr = merp[2]
            catarr.append(category.replace("PAID", ""))
            books.update({bookid: (bookname, bookurl, catarr)})
        except:
            catarr.append(category.replace("PAID", ""))
            books.update({bookid: (bookname, bookurl, catarr)})
    return books



def torScrapeTD(basedir,date):
    browserExe="chrome"
    main_csv_path = basedir + f"{date}/subcatmain.csv"
    dump_path=basedir +f"ScrapeRes/{date}b/"
    dump_path_dir=Path(dump_path)
    dump_path_dir.mkdir(parents=True,exist_ok=True)
    path=Path(main_csv_path)
    todo = cleanQ(date,basedir)
    already_done=[]
    if path.is_file():
        main_csv_file = open(main_csv_path, 'r', newline='', encoding="utf-8")
        reader=csv.reader(main_csv_file)
        for row in reader:
            already_done.append(row[0])
        main_csv_file.close()
    else:
        main_csv_file = open(main_csv_path, 'w', newline='', encoding="utf-8")
        writer = csv.writer(main_csv_file, quoting=csv.QUOTE_ALL)
        fieldname = ["book_id", "book_categories", "book_url", "title", "author",
                    "product details", " rankings", " stars", " reviews", " description", " prices"]
        writer.writerow(fieldname)
        main_csv_file.close()
    main_csv_file = open(main_csv_path, 'a', newline='', encoding="utf-8")
    writer = csv.writer(main_csv_file, quoting=csv.QUOTE_ALL)
    #get list of unprocessed keys
    key_q=[]
    for key in todo:
        if key not in already_done:
            key_q.append(key)
    


    #The following handles making attempts while requesting a new proxy from the controller every so often:
    attempts=0
    with Controller.from_port(port=9051) as c:
        c.authenticate(hcp)
        c.signal(Signal.NEWNYM)
        todonum=0
        while len(key_q)>30 and attempts<3:
            #Prints to console while scraping
            print(todonum)
            print(key_q)
            print("codes to do number as:")
            print(len(key_q))
            req_count=0
            todonum=0
            for key, val in todo.items():
                if key not in key_q:
                    todonum+=1
                    continue
                if req_count %50==0:
                    #sleep statements to not overload proxy list with requests
                    sleep(5)
                    c.signal(Signal.NEWNYM)
                    sleep(2)
                book_id = key
                book_categories = val[-1]
                book_url = val[1]
                try:
                    results_html = load_page(book_url)
                except:
                    os.system("pkill " + browserExe)
                    continue
                req_count+=1

                soup_results = soup(results_html, "html.parser")
                filename = dump_path + f"{book_id}.html"
                html_file = open(filename, 'w', encoding="utf-8")
                html_file.write(results_html)
                html_file.close()
                
                results = scrapePage(soup_results)
                
                book_title = results['title']
                book_author = results['author']
                book_productdet = results['product details']
                book_rankings = results['rankings']
                book_stars = results['stars']
                book_reviews = results['reviews']
                book_description = results['description']
                book_prices = results['prices']

                row = [book_id, book_categories, book_url, book_title, book_author, book_productdet,
                    book_rankings, book_stars, book_reviews, book_description, book_prices]
                
                err_count=0
                print("row is:")
                print(row)
                for i in range(len(row)):
                    if row[i]=="ERROR":
                        err_count+=1
                if err_count<3 or attempts>2:
                    writer.writerow(row)
                    if err_count<3:
                        key_q.remove(book_id)
            attempts+=1
    main_csv_file.close()

