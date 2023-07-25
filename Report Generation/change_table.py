import pandas as pd
from pathlib import Path

from reportlab.lib import colors
from reportlab.platypus import  Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from ast import literal_eval

from local_settings import html_path,base_path,report_out
from utils import date_scrape
import pdfkit


def change_table(cat, cat_date, cat_first=None,monthly=0):
    content_tmp = []
    month, day = date_scrape(cat_date)
    date_iter = day - 2
    month_iter=int(cat_date.partition("_")[0])
    print(month_iter)
    while cat_first is None and month_iter>4:
        if month_iter>=10:
            month_prefix=f"{month_iter}"
        else:
            month_prefix=f"0{month_iter}"
        if date_iter>=10:
            csv_try_date =  base_path+ r"cat_"  +month_prefix+ f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        else:
            csv_try_date =   base_path+ r"cat_" +month_prefix + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        try:
            cat_first = pd.read_csv(csv_try_date, header=0, index_col=0, converters={"Description": literal_eval})
            cat_first.set_index("Category", drop=True, inplace=True)
        except:
            if date_iter==1:
                date_iter=31
                month_iter-=1
            else:
                date_iter-=1

    table_change_set = cat.index.to_frame()
    change_columns = ["Category", "Avg. Rank Change", "Rank Change", "Avg. Page Length Change", "Page Length Change",
                      "Avg. Price Change", "Lowest Price Change"]
    table_change_set["Avg. Rank Change"] = round(cat["Avg. Sales Rank"]
                                                 - cat_first["Avg. Sales Rank"], 2).astype(str)
    print(table_change_set.head())
    table_change_set = table_change_set.drop(['Category'], axis=1)
    table_change_set["Rank Change"] = (cat["Top Rank"] - cat_first["Top Rank"]).astype(str)
    table_change_set["Avg. Page Length Change"] = round(
        ((cat["Avg. Page Length"] / cat_first["Avg. Page Length"]) -
         1)
        * 100, 2).astype(str) + "%"
    
    table_change_set["Page Length Change"] = round(
        ((cat["Best Page Length"] / cat_first["Best Page Length"]) - 1)
        * 100, 2).astype(str) + "%"
    table_change_set["Avg. Price Change"] = round(((cat["Avg. Price"] / cat_first["Avg. Price"]) - 1)
                                                  * 100, 2).astype(str) + "%"
    table_change_set["Lowest Price Change"] = round(((cat["Lowest Price"] / cat_first["Lowest Price"]) - 1)
                                                    * 100, 2).astype(str) + "%"
    table_change_set.loc[table_change_set["Lowest Price Change"] == "nan%", "Lowest Price Change"] = "0.0%"

    df_html=table_change_set.to_html(index=True)
    table_change_set_list = table_change_set.reset_index().values.tolist()
    table_change_set_list.insert(0, change_columns)

    s1 = getSampleStyleSheet()
    s1 = s1["BodyText"]
    s1.wordWrap = 'CJK'
    data3 = [[Paragraph(cell, s1) for cell in row] for row in table_change_set_list]
    summary_change_table = Table(data3, colWidths=[150, 80, 50, 90, 70, 60, 70])

    
    if monthly==0:
        title_string=f"{cat_date} Weekly Delta Summary"
    else:
        title_string=f"{cat_date} {month} Monthly Average Deltas Summary"
    html_template=f"""
    <!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="{html_path}template.css">
</head>
<body>
    <h1>{title_string}</h1>
    {df_html}
</body>
</html>
    """

    Path(html_path).mkdir(parents=True, exist_ok=True)
    html_file_path=html_path + "template2.html"
    html_file=open(html_file_path, "w", encoding="utf-8")
    html_file.write(html_template)
    html_file.close()

    #This code handles the pdf generation from the html
    
    output_pdf=output_pdf=report_out + cat_date + r"/"+  f'{cat_date}_change_table.pdf'
    with open(html_file_path) as f:
        pdfkit.from_file(f, output_pdf, options={"enable-local-file-access": ""})
    


    # Style the table
    summary_change_table_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey), ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
         ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
         ("FONTSIZE", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
         ("BACKGROUND", (0, 1), (-1, -1), colors.beige), ("GRID", (0, 0), (-1, -1), 1, colors.black)])

    summary_change_table.setStyle(summary_change_table_style)

    # Add the summary statistics table to the report
    content_tmp.append(summary_change_table)
    return content_tmp


#a version of change_table but for subcategories
def sub_change_table(catname,cat, cat_date, cat_first=None,monthly=0):
    content_tmp = []
    month, day = date_scrape(cat_date)
    date_iter = day - 2
    month_iter=int(cat_date.partition("_")[0])
    print(month_iter)
    while cat_first is None and month_iter>4:
        if month_iter>=10:
            month_prefix=f"{month_iter}"
        else:
            month_prefix=f"0{month_iter}"
        if date_iter>=10:
            csv_try_date =  base_path+ r"cat_"  +month_prefix+ f"_{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        else:
            csv_try_date =   base_path+ r"cat_" +month_prefix + f"_0{str(date_iter)}_" + cat_date.partition("_")[2].partition("_")[2] + ".csv"
        try:
            cat_first = pd.read_csv(csv_try_date, header=0, index_col=0, converters={"Description": literal_eval})
            cat_first.set_index("Category", drop=True, inplace=True)
        except:
            if date_iter==1:
                date_iter=31
                month_iter-=1
            else:
                date_iter-=1

    table_change_set = cat.index.to_frame()
    change_columns = ["Category", "Avg. Rank Change", "Rank Change", "Avg. Page Length Change", "Page Length Change",
                      "Avg. Price Change", "Lowest Price Change"]
    table_change_set["Avg. Rank Change"] = round(cat["Avg. Sales Rank"]
                                                 - cat_first["Avg. Sales Rank"], 2).astype(str)
    print(table_change_set.head())
    table_change_set = table_change_set.drop(['Category'], axis=1)
    table_change_set["Rank Change"] = (cat["Top Rank"] - cat_first["Top Rank"]).astype(str)
    table_change_set["Avg. Page Length Change"] = round(
        ((cat["Avg. Page Length"] / cat_first["Avg. Page Length"]) -
         1)
        * 100, 2).astype(str) + "%"
    
    table_change_set["Page Length Change"] = round(
        ((cat["Best Page Length"] / cat_first["Best Page Length"]) - 1)
        * 100, 2).astype(str) + "%"
    table_change_set["Avg. Price Change"] = round(((cat["Avg. Price"] / cat_first["Avg. Price"]) - 1)
                                                  * 100, 2).astype(str) + "%"
    table_change_set["Lowest Price Change"] = round(((cat["Lowest Price"] / cat_first["Lowest Price"]) - 1)
                                                    * 100, 2).astype(str) + "%"
    table_change_set.loc[table_change_set["Lowest Price Change"] == "nan%", "Lowest Price Change"] = "0.0%"

    table_change_set_list = table_change_set.reset_index().values.tolist()
    table_change_set_list.insert(0, change_columns)
    
    df_html=table_change_set.to_html(index=True)
    
    s1 = getSampleStyleSheet()
    s1 = s1["BodyText"]
    s1.wordWrap = 'CJK'
    data3 = [[Paragraph(cell, s1) for cell in row] for row in table_change_set_list]
    summary_change_table = Table(data3, colWidths=[150, 80, 50, 90, 70, 60, 70])

    
    if monthly==0:
        title_string=f"{cat_date} {catname} Weekly Delta Summary"
    else:
        title_string=f"{cat_date} {month}  {catname} Monthly Average Deltas Summary"
    html_template=f"""
    <!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="{html_path}template.css">
</head>
<body>
    <h1>{title_string}</h1>
    {df_html}
</body>
</html>
    """

    Path(html_path).mkdir(parents=True, exist_ok=True)
    html_file_path=html_path + "template2.html"
    html_file=open(html_file_path, "w", encoding="utf-8")
    html_file.write(html_template)
    html_file.close()

    #This code handles pdf gen
    
    output_pdf=output_pdf=report_out + cat_date + r"/"+  f'{cat_date}_{catname}_change_table.pdf'
    with open(html_file_path) as f:
        pdfkit.from_file(f, output_pdf, options={"enable-local-file-access": ""})
    

    # Style the table
    summary_change_table_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey), ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
         ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
         ("FONTSIZE", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
         ("BACKGROUND", (0, 1), (-1, -1), colors.beige), ("GRID", (0, 0), (-1, -1), 1, colors.black)])

    summary_change_table.setStyle(summary_change_table_style)

    # Add the summary statistics table to the report
    content_tmp.append(summary_change_table)
    return content_tmp