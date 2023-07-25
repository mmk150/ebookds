import pandas as pd
import matplotlib.pyplot as plt
import math


from reportlab.platypus import Spacer, Image
from local_settings import report_out
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from utils import date_scrape


def label_trunc(label_value):
    # Note that this can be made more general, but at least for now this works
    if label_value < 1000:
        return str(round(label_value))
    elif label_value < 1000000:
        return str(round(label_value/1000))+"k"

def tick_round(top_lim, bot_lim):
    """
    Round up top to nice round number which is no more that 20% larger
    Does something similar for bot, needs to be fine-tuned on a case by case basis
    """

    top_tick = top_lim
    num_digits = round(math.log10(top_lim))
    for i in range(num_digits+1):
        tmp_top = (10 ** i) * math.ceil((top_lim + 10.0 ** (i-1) * 5.0)/(10 ** i))
        if tmp_top < top_lim * 1.2:
            top_tick = tmp_top
    
    # Note that this may have to be fine-tuned a lot
    bot_tick = round(bot_lim - (top_tick-top_lim))

    return top_tick, bot_tick


def invert_bar(cat_sort, title, bar_colors, path, image_name, rot):
    """
    The idea is that this takes a pre-sorted dataframe called cat_sort which consists of
    two columns - the index which gives the categories, and another column to be the heights
    of the bar graph.

    In addition, cat_sort should only include as many rows as will be placed on this specific
    chart.
    """
    max_val = max(cat_sort.iloc[:, 0])
    min_val = min(cat_sort.iloc[:, 0])
    max_tick, min_tick = tick_round(max_val, min_val)
    
    num_x = len(cat_sort.index)
    x_list = []
    for i in range(1, num_x+1):
        x_list.append(i)
    
    plt.ylim(min_tick, max_tick)
    plt.gca().invert_yaxis()
    plt.xticks(x_list, cat_sort.index, rotation=rot, ha='right')
    plt.grid(visible=False)
    for r in range(len(cat_sort)):
        val = cat_sort.iloc[r, 0]
        plt.text(cat_sort.index[r], val+round(max_tick-max_val), label_trunc(val), fontsize=8, color = 'black')
    plt.ylabel('Sales Ranking')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path + image_name+".png")
    plt.close()
    return Image(path + image_name + ".png", width=600, height=400)

def sales_bar(cat, cat_date, monthly=0, avg=0, main_cat=None):
    colors = ['firebrick', 'lime', 'fuchsia', 'moccasin', 'cyan', 'slateblue',
              'greenyellow', 'silver', 'sandybrown', 'chartreuse', 'cadetblue',
              'hotpink', 'gold', 'teal', 'violet']
    chart_dir = report_out + cat_date + r"/"
    rot_var = 45
    title_type = "Top"
    image_type = "top"
    cat_sales = cat.copy(True)
    if avg == 0:
        cat_sales.sort_values(by=["Top Rank"], inplace=True)
        cat_sales.drop(["Avg. Sales Rank"], axis=1, inplace=True)
    else:
        cat_sales.sort_values(by=["Avg. Sales Rank"], inplace=True)
        title_type = "Average"
        image_type = "avg"

    split_list = []
    cat_number = cat_sales.shape[0]

    if cat_number <= 15:
        split_list.append(cat_sales.iloc[0:cat_number])
    else:
        split_start = 0
        split_end = 15
        while split_end < cat_number:
            split_list.append(cat_sales.iloc[split_start:split_end])
            split_start += 15
            split_end = min(split_end+15, cat_number)

    month,day= date_scrape(cat_date)
    bar_title = title_type + " Ranking " + cat_date
    month_titler= main_cat + "_" + month +"_"

    bar_list = []
    index = 1
    for graph_data in split_list:
        bar_list.append(invert_bar(graph_data, month_titler + bar_title,
                           colors, chart_dir, month_titler+bar_title + "_" + image_type + "_rank_plot_image_" + str(index), rot_var))
        index+=1
    
    return bar_list
    


def bar_charts(cat, cat_date, monthly=0, avg_sales=0, top_sales=0, main_cat=""):
    content_tmp = []

    if avg_sales == 1:
        avg_sales_list = sales_bar(cat, cat_date, monthly, 1, main_cat)
        for x in avg_sales_list:
            content_tmp.append(x)

    content_tmp.append(Spacer(1, 24))

    if top_sales == 1:
        top_sales_list = sales_bar(cat, cat_date, monthly, 0, main_cat)
        for y in top_sales_list:
            content_tmp.append(y)
    return content_tmp