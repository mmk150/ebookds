import pandas as pd
import numpy as np
from ast import literal_eval

from local_settings import base_path

book_columns = ["book_id", "book_categories", "book_url", "title", "author", "product details", "rankings", "stars",
                "reviews", " description", "prices"]
#What is the date you wish to investigate? (MM_DD_YYYY format):
date_input = ""


#Main Categories or Subcategories? ("0" for main, "1" for sub)
sub_check = "0"

if sub_check == '0':
    date_csv =  base_path + date_input + ".csv"
    date_csv_cat =  base_path + "cat_" + date_input + ".csv"
elif sub_check == '1':
    date_csv =  base_path + "sub_" + date_input + ".csv"
    date_csv_cat =  base_path + "subcat_" + date_input + ".csv"    

cat_columns = ["Category", "Avg. Sales Rank", "Top Rank", "Description", "Avg. Page Length", "Best Page Length",
               "Avg. Price", "Lowest Price"]

book_data = pd.read_csv(date_csv, header=0,
                        converters={'book_categories': literal_eval,
                        # bizarre error only for the week of 5_28_23: 'author': literal_eval,
                        'product_details': literal_eval})

# This collects the overall ranking as an integer
rank_dict = {}
for i in range(book_data.shape[0]):
    # This line collects the overall ranking of the book from the " rankings" string
    overall_ranking = book_data.loc[i, " rankings"][18:].partition("'")[0]
    overall_ranking = overall_ranking.partition(" ")[0]
    if overall_ranking == "":
        overall_ranking = '100000'
    rank_dict[i] = int(overall_ranking.replace(',', ''))

main_rank = pd.Series(rank_dict)
book_data["main_rank"] = main_rank

# This collects the page length as an integer
page_dict = {}
for i in range(book_data.shape[0]):
    page_len = book_data.loc[i, "product details"].partition("length:': '")[2].partition(" ")[0]
    if page_len == "":
        page_len = "0"
    page_dict[i] = int(page_len.replace(',', ''))

main_page = pd.Series(page_dict)
book_data["Page Length"] = main_page

# This collects the price as an integer
price_dict = {}
for i in range(book_data.shape[0]):
    try:
        price = book_data.loc[i, " prices"].partition("$")[2]
    except:
        price = ""
    if (price=="Error" or price == ""):
        price_dict[i] = float(0.00)
    else:
        j = 0
        while (price[j].isnumeric() or price[j] == "."):
            j += 1
        price = price[:j]
        if price == '0.00':
            price = book_data.loc[i, " prices"].partition("$")[2].partition("$")[2]
            if price == "":
                price = "0.00"
            else:
                k = 0
                while (price[k].isnumeric() or price[k] == "."):
                    k += 1
                price = price[:k]
        price_dict[i] = float(price.replace(',', ''))

main_price = pd.Series(price_dict)
book_data["Pricing"] = main_price

book_data_explode = book_data.explode("book_categories")
book_data_explode.reset_index(drop=True, inplace=True)
if sub_check == '1': 
    drop_dict = {}
    for j in book_data_explode.index:
        drop_dict.update({j:book_data_explode.iloc[j, 1].partition(" - ")[2]})
    book_data_explode["Sub Category"] = pd.Series(drop_dict)
    book_data_explode = book_data_explode.drop(book_data_explode[book_data_explode["Sub Category"] == ""].index)
    book_data_explode.reset_index(drop=True, inplace=True)


book_data_explode.sort_values(by=["book_categories"], inplace=True)
book_data_explode.reset_index(drop=True, inplace=True)


# Note that this is the point where the category order is set
categories = pd.unique(book_data_explode["book_categories"])
cat_data = pd.DataFrame(columns=cat_columns)

index_dict = {}
ind = 0
for category in categories:
    index_dict.update({category:ind})
    ind += 1

def intersect_counts(book, cats):
    # So book should be the list of categories that a given ebook is in
    # cats should be the specific category we are comparing against
    sparse_mat = np.zeros((len(categories)))
    if cats in book:
        for cat in categories:
            if cat in book:
                sparse_mat[index_dict[cat]] = 1
    return sparse_mat

int_counts = {}
for cat in categories:
    inter_array = np.zeros((len(categories)))
    for r in range(book_data.shape[0]):
        inter_array += intersect_counts(book_data.iloc[r, 1], cat)
    int_counts.update({cat: inter_array})

def cat_collapse(single_cat, word):
    token = []
    for desc in single_cat[" description"]:
        desc_words = desc.split()
        token.extend(desc_words)

    org_cat = single_cat.sort_values(by=["main_rank"]).reset_index()

    low_prix = 100.0
    for prix in single_cat["Pricing"]:
        if low_prix > prix:
            if prix > 0.0:
                low_prix = prix

    sale_avg = single_cat["main_rank"].mean()
    sale_var = single_cat["main_rank"].std()

    data = {"Category": word, "Avg. Sales Rank": sale_avg,
            "Top Rank": single_cat["main_rank"].min(), "Description": token,
            "Avg. Page Length": single_cat["Page Length"].mean(), "Best Page Length": org_cat["Page Length"][0],
            "Avg. Price": single_cat["Pricing"].mean(), "Lowest Price": low_prix, "Intersection Counts": int_counts[word].tolist(),
            "Avg. Sales Deviation": sale_var}
    return pd.Series(data)

for word in categories:
    word_test = 'book_categories == "' + word + '"'
    cat_data = cat_data.append(cat_collapse(book_data_explode.query(word_test), word),
                               ignore_index=True)
    
# Let's change the name of the "Main:Paid" category to something like "Top 100"
if sub_check == '0':
    name_dict = {}
    for ind in cat_data.index:
        temp_cat = cat_data.iloc[ind, 0]
        if temp_cat == "Main:Paid":
            temp_cat = "Top 100"
        name_dict.update({x:temp_cat})
    cat_data["Category"] = pd.Series(name_dict)
else:
    # Here we want to split categories into main and sub categories, and filter out non-sub values
    main_dict = {}
    sub_dict = {}
    for ind in cat_data.index:
        main_dict.update({ind:cat_data.iloc[ind, 0].partition(" - ")[0]})
        sub_dict.update({ind:cat_data.iloc[ind, 0].partition(" - ")[2]})
    cat_data["Category"] = pd.Series(main_dict)
    cat_data["Sub Category"] = pd.Series(sub_dict)
    cat_data.groupby(["Category"])


cat_data.to_csv(date_csv_cat)
test_data = cat_data.drop(['Description'], axis=1)
test_data.to_csv("test.csv")
