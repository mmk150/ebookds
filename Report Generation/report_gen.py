import pandas as pd
import seaborn as sns
import os
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape,letter
from ast import literal_eval

from charts_stuff import chart_pdf
from cloud import week_cloud
from week_table import week_table
from change_table import change_table
from trends import month_trend

from local_settings import base_path, report_out
from utils import date_scrape



def getInterList(cat_var):
    index_dict = {}
    ind = 0
    for cat in cat_var["Category"].tolist():
        index_dict.update({cat:ind})
        ind += 1
    return index_dict

# Takes date as input, gives csv with date title (or error) as output
def date_catching():
    date_var = input("What is the date that you wish to investigate? (MM_DD_YYYY format): ")
    csv_var =base_path + "cat_" + date_var + ".csv"
    cat_var = None
    intersection_list=[]
    try:
        cat_var = pd.read_csv(csv_var, header=0, index_col=0, converters={"Description": literal_eval})
        # here we populate intersection_list
        intersection_list=getInterList(cat_var)
    except:
        print("I apologize, but I do not recognize this date.")
        return 0, date_var, csv_var, cat_var, intersection_list
    return 1, date_var, csv_var, cat_var, intersection_list


    

# Gets date as input, gives csv
# Ran this way with date_catching method for error catching purposes
check_var = 0
while check_var == 0:
    check_var, date_input, date_csv, cat_data, inter_list = date_catching()
cat_data['Intersection Counts'] = cat_data['Intersection Counts'].apply(literal_eval)

# Scrapes month and day from input date
date_month, date_day = date_scrape(date_input)

# CLI prints which asks users which modules they want added to the pdf
# If date is at the end of the month, also gives the option for monthly report
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
        if mod_id == 4:
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

#Helps computing the intersection counts
def inter_adder(inter, temp_int):
    for x in range(0, len(inter)):
        inter[x] = inter[x] + float(temp_int[x])
    return inter

# Creates module_list, the list of modules to be added to this pdf
# module_list is saved as 0 means don't add that module, 1 means add it
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
    date_report = "report_" + date_month + " - " + date_input + ".pdf"
else:
    date_report = "report_" + date_input + ".pdf"




def end_month(cat, cat_date, mod_list):
    # Create cat_avg
    # Call other functions according to module_list
    content_tmp = []

    month, day = date_scrape(cat_date)
    cat_list = []
    int_dict = {}
    for cag in cat.index:
        int_dict.update({cag:np.zeros(len(cat.index)).tolist()})

    dates = []
    for date_iter in range(1, 31):
        if date_iter>=10:
            date = "05" + f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2]
            csv_try_date =base_path + "cat_" + "05" + f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        else:
            date = "05" + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2]
            csv_try_date =base_path + "cat_" + "05" + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        try:
            temp=pd.read_csv(csv_try_date, header=0, index_col=0, converters={"Description": literal_eval, "Intersection Counts": literal_eval})
            temp.set_index("Category", drop=True, inplace=True)
            temp["Avg. Sales Rank"].astype(float)
            temp["Top Rank"].astype(float)
            temp["Avg. Page Length"].astype(float)
            temp["Best Page Length"].astype(float)
            temp["Avg. Price"].astype(float)
            temp["Lowest Price"].astype(float)
            temp_dict = temp["Intersection Counts"].to_dict()
            for ind in cat.index:
                int_dict.update({ind: inter_adder(int_dict[ind], temp_dict[ind])})
            temp = temp.drop(["Intersection Counts"], axis=1)
            cat_list.append(temp)
            dates.append(date)
        except:
            None
    for date_iter in range(1, day+1):
        if date_iter>=10:
            date = cat_date.partition("_")[0] + f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2]
            csv_try_date =base_path + "cat_" + cat_date.partition("_")[0] + f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        else:
            date = cat_date.partition("_")[0] + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2]
            csv_try_date =base_path + "cat_" + cat_date.partition("_")[0] + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        try:
            temp=pd.read_csv(csv_try_date, header=0, index_col=0, converters={"Description": literal_eval, "Intersection Counts": literal_eval})
            temp.set_index("Category", drop=True, inplace=True)
            temp["Avg. Sales Rank"].astype(float)
            temp["Top Rank"].astype(float)
            temp["Avg. Page Length"].astype(float)
            temp["Best Page Length"].astype(float)
            temp["Avg. Price"].astype(float)
            temp["Lowest Price"].astype(float)
            temp_dict = temp["Intersection Counts"].to_dict()
            for ind in cat.index:
                int_dict.update({ind: inter_adder(int_dict[ind], temp_dict[ind])})
            temp = temp.drop(["Intersection Counts"], axis=1)
            cat_list.append(temp)
            dates.append(date)
        except:
            None
    day_num = len(cat_list)
    cat_data_avg = cat_list[0]

    
    #Averages over all category dataframes
    for x in range(1, day_num):
        cat_data_avg = cat_data_avg + cat_list[x]
    cat_data_avg["Intersection Counts"] = pd.Series(int_dict)

    cat_data_avg["Avg. Sales Rank"] = (cat_data_avg["Avg. Sales Rank"]).astype(float) / day_num
    cat_data_avg["Top Rank"] = (cat_data_avg["Top Rank"]).astype(float) / 5
    cat_data_avg["Avg. Page Length"] = (cat_data_avg["Avg. Page Length"]).astype(float) / day_num
    cat_data_avg["Best Page Length"] = (cat_data_avg["Best Page Length"]).astype(float) / day_num
    cat_data_avg["Avg. Price"] = (cat_data_avg["Avg. Price"]).astype(float) / day_num
    cat_data_avg["Lowest Price"] = (cat_data_avg["Lowest Price"]).astype(float) / day_num

    if mod_list[1] == "1":
        content_tmp = content_tmp + change_table(cat_list[-1], cat_date, cat_list[0])
    if mod_list[2] == "1":
        content_tmp = content_tmp + week_cloud(cat_data_avg, cat_date, monthly=1)
    if mod_list[3] == "1":
        content_tmp = content_tmp + chart_pdf(cat_data_avg, cat_date, inter_list, 1)
        content_tmp = content_tmp + month_trend(cat_list, dates)
    return content_tmp



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

cat_data.set_index("Category", drop=True, inplace=True)


#This creates and appends report components to the final pdf document.
if module_list[0] == "1":
    content = content + week_table(cat_data, date_input)
if module_list[1] == "1":
    content = content + change_table(cat_data, date_input)
if module_list[2] == "1":
    content = content + week_cloud(cat_data, date_input)
if module_list[3] == "1":
    content = content + chart_pdf(cat_data, date_input, inter_list)
if module_list[4] == "1":
    content = content + end_month(cat_data, date_input, module_list)

# Add a spacer
content.append(Spacer(1, 24))
doc.build(content)
