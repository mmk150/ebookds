import pandas as pd
import seaborn as sns
import os
import numpy as np


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape,letter
from ast import literal_eval

#Moved main module functions to charts.py,week_cloud.py,change_table.py,week_table.py
#imported relevant functions
from charts_stuff import chart_pdf
from cloud import week_cloud
from week_table import sub_week_table
from change_table import sub_change_table
from local_settings import base_path, report_out
import warnings
warnings.filterwarnings("ignore")
from utils import date_scrape

# Takes date as input, gives csv with date title (or error) as output
def date_catching():
    date_var = input("What is the date that you wish to investigate? (MM_DD_YYYY format): ")
    csv_var =base_path + "subcat_" + date_var + ".csv"
    cat_var = None
    try:
        cat_var = pd.read_csv(csv_var, header=0, index_col=0, converters={"Description": literal_eval})
    except:
        print("I apologize, but I do not recognize this date.")
        return 0, date_var, csv_var, cat_var #, intersection_list
    return 1, date_var, csv_var, cat_var #, intersection_list



# Gets date as input, gives csv
# Ran this way with date_catching method for error catching purposes
check_var = 0
while check_var == 0:
    check_var, date_input, date_csv, cat_data = date_catching()

cat_data['Intersection Counts'] = cat_data['Intersection Counts'].apply(literal_eval)
date_month, date_day = date_scrape(date_input)


# Interface which asks users which modules they want added to the pdf
# At end of month, gives option for monthly report
def mod_catching(mod_id, mod_date):
    if mod_id == 0:
        mod_out = input(
            "Do you wish to see the summarized weekly table data for " + mod_date + "? (0 for no, 1 for yes):")
    elif mod_id == 1:
        mod_out = input(
            "Do you wish to see the summarized table of changes for " + mod_date + "? (0 for no, 1 for yes):")
    elif mod_id == 2:
        mod_out = input("Do you wish to see the generated tag cloud for " + mod_date + "? (0 for no, 1 for yes):")
    elif mod_id == 3:
        mod_out = input("Do you wish to see the ranking charts for " + mod_date + "? (0 for no, 1 for yes):")
    else:
        month, day = date_scrape(mod_date)
        if (30 - day) < 7 and mod_id == 4:
            mod_out = input(
                "Do you wish to see the end of month report for " + month + "? (0 for no, 1 for yes):"
            )
        else:
            return "1", 0

    if mod_out == "0":
        return 1, mod_out
    elif mod_out == "1":
        return 1, mod_out
    else:
        return 0, mod_out


def inter_adder(zers, new):
    for x in range(0, len(zers)):
        zers[x] = zers[x] + float(new[x])
    return zers

def indexMatch(cat, categories, subcategories, category):
    comp_list = []
    for i in range(0, len(categories)):
        if (i < len(subcategories) and categories[i]==subcategories[i]):
            comp_list.append(1)
        else:
            comp_list.append(2)
    sub_zeros = np.zeros(len(comp_list))

    another_dict = {}
    for j in range(0, len(categories)):
        if comp_list[j] == 1:
            another_dict.update({(category, categories[j]):inter_adder(cat.loc[(category, categories[j]),"Intersection Counts"], comp_list)})
        else:
            another_dict.update({(category, categories[j]): sub_zeros.tolist()})
            blank_row = pd.DataFrame(columns=["Avg. Sales Rank", "Top Rank", "Description", "Avg. Page Length",
                                                  "Best Page Length", "Avg. Price", "Lowest Price", "Intersection Counts", "Category", "Sub Category"])
            blank_row.loc[0] = [0.0, 0.0, [""], 0.0, 0.0, 0.00, 0.00, [0], mast, categories[j]]
            blank_row.set_index(["Category", "Sub Category"], drop=True, inplace=True)
            cat=cat.append(blank_row)

    return cat

# Creates module_list, the list of modules to be added to this pdf
# module_list = [week_table, change_table, week_cloud, charts, end_month]
check_mod = 0
module_list = []
for i in range(5):
    while check_mod == 0:
        check_mod, mod_ans = mod_catching(i, date_input)
    module_list.append(mod_ans)
    check_mod = 0

# Titles pdf based on date and whether it is a monthly report
if module_list[4] == "1":
    date_report = "report_subcat_" + date_month + " - " + date_input + ".pdf"
else:
    date_report = "report_subcat_" + date_input + ".pdf"
    
sns.set(style="whitegrid")

# Set up the document
report_dir = report_out + date_input
report_path = report_dir + r"/" + date_report
try:
    os.mkdir(report_dir)
except:
    None

doc = SimpleDocTemplate(report_path, pagesize=landscape(letter),pageCompression=1)

# Set up the content list
content = []

# Set up the styles
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
subtitle_style = styles["Heading2"]
text_style = styles["BodyText"]

# Add the title
title = Paragraph("Analyzing Genre Data to Improve Market Penetration: " + date_input, title_style)
content.append(title)
# Add a spacer
content.append(Spacer(1, 12))

# Add the subtitle
subtitle = Paragraph("A Summary of Important Genre Statistics for Top Selling eBooks by Category", subtitle_style)
content.append(subtitle)

# Add some introductory text
intro = Paragraph(
    "In this report, we present the results of our analysis on the genre dataset. We have performed basic data "
    "analysis and created some visualizations to better understand the dataset.",
    text_style)
content.append(intro)

# Add a spacer
content.append(Spacer(1, 12))

# Sorts and trims intersection counts per main category
# Also handles modules per main category
monthly=0
if module_list[4] == "1":
    monthly=1
    # Create cat_avg
    # Call other functions according to module_list
    content_tmp = []
    x, y = date_scrape(date_input)
    cat_list = []
    
    for date_iter in range(0, y):
        try:
            if date_iter>=10:
                csv_try_date =base_path + "subcat_" + date_input.partition("_")[0] + f"_{str(date_iter)}_" + date_input.partition("_")[2].partition("_")[2] + ".csv"
            else:
                csv_try_date =base_path + "subcat_" + date_input.partition("_")[0] + f"_0{str(date_iter)}_" + date_input.partition("_")[2].partition("_")[2] + ".csv"
            
            temp=pd.read_csv(csv_try_date, header=0, index_col=0, converters={"Description": literal_eval, "Intersection Counts": literal_eval})
            temp.set_index(["Category", "Sub Category"], drop=True, inplace=True)
            temp["Avg. Sales Rank"].astype(float)
            temp["Top Rank"].astype(float)
            temp["Avg. Page Length"].astype(float)
            temp["Best Page Length"].astype(float)
            temp["Avg. Price"].astype(float)
            temp["Lowest Price"].astype(float)
            cat_list.append(temp)
        except:
            None
    day_num = len(cat_list)

    cat_series = pd.Series()
    for tab in cat_list:
        cat_series = cat_series.append(pd.Series(tab.index.get_level_values("Category")))
    cat_series.sort_values(inplace=True)
    master_category = cat_series.unique()

    subcat_dict = {}
    for super in master_category:
        subcat_series = pd.Series()
        for tab in cat_list:
            subcat_series = subcat_series.append(pd.Series(tab.loc[(super),:].index.get_level_values("Sub Category")))
        subcat_series.sort_values(inplace=True)
        subcat_dict.update({super: subcat_series.unique()})


    int_series = {}
    for mast in master_category:
        for sub in subcat_dict[mast]:
            zeros_list = np.zeros(cat_list[0].shape[0]).tolist()
            for ind in range(0, day_num):
                zeros_list = inter_adder(zeros_list, cat_list[ind].loc[(mast, sub), "Intersection Counts"])
            int_series.update({(mast, sub):zeros_list})


    cat_data_avg = cat_list[0]
    cat_data_avg = cat_data_avg.drop(["Intersection Counts"], axis=1)
    
    for i in range(1, day_num):
        cat_data_avg.sort_values(by=["Category", "Sub Category"], inplace=True)
        cat_data_avg = cat_data_avg + cat_list[q].drop(["Intersection Counts"], axis=1)

    cat_data_avg["Intersection Counts"] = pd.Series(int_series)


    # cat_columns = ["Category", "Avg. Sales Rank", "Top Rank", "Description", "Avg. Page Length", "Best Page Length",
    #               "Avg. Price", "Lowest Price"]
   
    cat_data_avg["Avg. Sales Rank"] = (cat_data_avg["Avg. Sales Rank"]).astype(float) / day_num
   
    cat_data_avg["Top Rank"] = (cat_data_avg["Top Rank"]).astype(float) / 5
    cat_data_avg["Avg. Page Length"] = (cat_data_avg["Avg. Page Length"]).astype(float) / day_num
    cat_data_avg["Best Page Length"] = (cat_data_avg["Best Page Length"]).astype(float) / day_num
    cat_data_avg["Avg. Price"] = (cat_data_avg["Avg. Price"]).astype(float) / day_num
    cat_data_avg["Lowest Price"] = (cat_data_avg["Lowest Price"]).astype(float) / day_num
    cat_data = cat_data_avg
    cat_data.drop(["Description"], axis=1).to_csv("test.csv")
else:
    cat_data.set_index(["Category", "Sub Category"], drop=True, inplace=True)

total_cat_num = cat_data.shape[0]
running_total = 0

for main_cat in cat_data.index.get_level_values("Category").unique():
    temp_cat = cat_data.loc[(main_cat), :].copy(True)
    cat_len = temp_cat.shape[0]
    temp_dict = temp_cat["Intersection Counts"].to_dict()
    if running_total > 0:
        for sub_cat in temp_cat.index:
            del temp_dict[sub_cat][:running_total]
    if cat_len + running_total < total_cat_num:
        for sub_cat in temp_cat.index:
            del temp_dict[sub_cat][cat_len:]
    temp_cat["Intersection Counts"] = pd.Series(temp_dict)

    temp_cat.index.names = ["Category"]

    running_total += cat_len
    sub_cat_title = Paragraph(
        "The following is the breakdown for the " + main_cat + " category:",
        subtitle_style)
    content.append(sub_cat_title)

    
    test_temp = temp_cat.drop(["Description"], axis=1)
    test_temp.to_csv(main_cat + "_test.csv")

    # Add a spacer
    content.append(Spacer(1, 12))
    if module_list[0] == "1":
        content = content + sub_week_table(main_cat,temp_cat, date_input,monthly=monthly)
    if module_list[1] == "1":
        content = content + sub_change_table(main_cat,temp_cat, date_input,monthly=monthly)
    if module_list[2] == "1":
        content = content + week_cloud(temp_cat, date_input, main_cat)
    if module_list[3] == "1":
        content = content + chart_pdf(temp_cat, date_input, None, 0, main_cat)


# Add a spacer
content.append(Spacer(1, 24))
doc.build(content)
