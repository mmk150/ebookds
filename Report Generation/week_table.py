from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from local_settings import html_path,report_out

# NEW IMPORTS:

import pdfkit

# This method handles the module for the table of summarized stats for the week
# cat is the organized csv, cat_date is the input date (which is not stored in the dataframe)

def week_table(cat, cat_date,monthly=0):
  
    content_tmp = []    
    table_set = cat.copy(True)
    table_set.sort_values(by=["Avg. Sales Rank"], inplace=True)

    table_set["Avg. Sales Rank"] = round(table_set["Avg. Sales Rank"], 2).astype(str)
    table_set["Top Rank"] = round(table_set["Top Rank"],2).astype(str)
    table_set["Avg. Page Length"] = round(table_set["Avg. Page Length"], 2).astype(str)
    table_set["Best Page Length"] = round(table_set["Best Page Length"],2).astype(str)
    table_set["Avg. Price"] = round(table_set["Avg. Price"], 2).astype(str)
    table_set["Lowest Price"] = round(table_set["Lowest Price"],2).astype(str)
    cat_columns = ["Category", "Avg. Sales Rank", "Top Rank", "Avg. Page Length", "Best Page Length", "Avg. Price",
                   "Lowest Price"]

    table_set = table_set.drop(['Description'], axis=1)
    table_set = table_set.drop(['Intersection Counts'], axis=1)
    table_set=table_set.drop(['Avg. Sales Deviation'],axis=1)
    
    table_set_list = table_set.reset_index().values.tolist()
    table_set_list.insert(0, cat_columns)

    # Style the table
    summary_table_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey), ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
         ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
         ("FONTSIZE", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
         ("BACKGROUND", (0, 1), (-1, -1), colors.beige), ("GRID", (0, 0), (-1, -1), 1, colors.black)])

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'

    df_html=table_set.to_html(index=True)

    if monthly==0:
        title_string=f"{cat_date} Weekly Summary"
    else:
        title_string=f"{cat_date} Monthly Average Summary"
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
    html_file_path=html_path + "template.html"
    html_file=open(html_file_path, "w", encoding="utf-8")
    html_file.write(html_template)
    html_file.close()


    #This handles the pdf generation from the stylized html file

    output_pdf=report_out + cat_date + r"/"+ f'{cat_date}_week_table.pdf'
    with open(html_file_path) as f:
        pdfkit.from_file(f, output_pdf, options={"enable-local-file-access": ""})
    
    return content_tmp


def sub_week_table(catname,cat, cat_date,monthly=0):

    content_tmp = [] 
    table_set = cat.copy(True)
    table_set.sort_values(by=["Avg. Sales Rank"], inplace=True)

    table_set["Avg. Sales Rank"] = round(table_set["Avg. Sales Rank"], 2).astype(str)
    table_set["Top Rank"] = round(table_set["Top Rank"],2).astype(str)
    table_set["Avg. Page Length"] = round(table_set["Avg. Page Length"], 2).astype(str)
    table_set["Best Page Length"] = round(table_set["Best Page Length"],2).astype(str)
    table_set["Avg. Price"] = round(table_set["Avg. Price"], 2).astype(str)
    table_set["Lowest Price"] = round(table_set["Lowest Price"],2).astype(str)
    cat_columns = ["Subcategory", "Avg. Sales Rank", "Top Rank", "Avg. Page Length", "Best Page Length", "Avg. Price",
                   "Lowest Price"]

    table_set = table_set.drop(['Description'], axis=1)
    table_set = table_set.drop(['Intersection Counts'], axis=1)
    table_set=table_set.drop(['Avg. Sales Deviation'],axis=1) 
    
    table_set_list = table_set.reset_index().values.tolist()
    table_set_list.insert(0, cat_columns)
    
    if monthly==1:
        table_set.rename(columns={'Avg. Sales Rank':'Monthly Avg. Sales Rank',
                                'Top Rank':'Monthly Avg. Top Rank',
                                'Avg. Page Length':'Monthly Avg. Page Length',
                                'Best Page Length': 'Monthly Avg. Top Page Length',
                                'Avg. Price': 'Monthly Avg. Price',
                                'Lowest Price': 'Monthly Avg. Lowest Price'
                                },inplace=True)
        
    df_html=table_set.to_html(index=True)

    # Style the table
    summary_table_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey), ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
         ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
         ("FONTSIZE", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
         ("BACKGROUND", (0, 1), (-1, -1), colors.beige), ("GRID", (0, 0), (-1, -1), 1, colors.black)])

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'

    df_html=table_set.to_html(index=True)

    if monthly==0:
        title_string=f"{cat_date} {catname} Weekly Summary"
    else:
        title_string=f"{cat_date} {catname} Monthly Average Summary"
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
    html_file_path=html_path + "template.html"
    html_file=open(html_file_path, "w", encoding="utf-8")
    html_file.write(html_template)
    html_file.close()


    #This handles the pdf generation from the stylized html file

    output_pdf=report_out + cat_date + r"/"+ f'{cat_date}_{catname}_week_table.pdf'
    with open(html_file_path) as f:
        pdfkit.from_file(f, output_pdf, options={"enable-local-file-access": ""})
    
    return content_tmp