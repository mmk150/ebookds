import matplotlib.pyplot as plt


from reportlab.platypus import  Spacer, Image
from matplotlib_venn import venn2
from bar_charts import bar_charts
from donut import donut
from local_settings import report_out
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from utils import date_scrape


def label_trunc(label_val):
    if label_val < 1000:
        return str(round(label_val))
    elif label_val < 1000000:
        return str(round(label_val/1000))+"k"

def donut_chart(cat, cat_date, index_dict, monthly=0):
    category_list = cat.index.tolist()
    category_sizes = []
    for cat in category_list:
        category_sizes.append(cat.loc["Top 100", "Intersection Counts"][index_dict[cat]])
    return donut(category_sizes, category_list, cat_date)


def venn_chart(cat, cat_date, index_dict, monthly=0, thresh=5, main_cat=None):
    chart_list = []
    chart_dir = report_out + cat_date + r"/"
    month, day = date_scrape(cat_date)
    if monthly == 0:
        month_title = main_cat + ": "
        month_image = main_cat + "_"
    elif monthly == 1:
        month_title = main_cat + ": " + month + " "
        month_image = main_cat + "_" + month + "_"   

    if monthly == 1:
        thresh = thresh * 5

    for ind1 in cat.index:
        for ind2 in cat.index:
            group_1 = index_dict[ind1]
            group_2 = index_dict[ind2]
            size_1 = cat.loc[ind1, "Intersection Counts"][group_1]
            size_2 = cat.loc[ind2, "Intersection Counts"][group_2]
            inter = cat.loc[ind1, "Intersection Counts"][group_2]

            if (int(inter) > thresh) and (group_1 < group_2):
                venn2(subsets = (size_1, size_2, inter), set_labels = (ind1, ind2))
                plt.title(month_title + "Profitable Category Synergy: " + ind1 + " and " + ind2)
                plt.tight_layout()
                image_name = month_image + "venn_" + ind1 + "_" + ind2 + ".png"
                plt.savefig(chart_dir + image_name)
                plt.close()
                chart_list.append(Image(chart_dir + image_name, width=600, height=400))
    return chart_list
    


def over_chart(cat, cat_date, index_dict, monthly=0, thresh=5, main_cat=None):
    chart_list = []
    chart_dir = report_out + cat_date + r"/"
    month, day = date_scrape(cat_date)
    if monthly == 0:
        month_title = main_cat + ": "
        month_image = main_cat + "_"
    elif monthly == 1:
        month_title = main_cat + ": " + month + " "
        month_image = main_cat + "_" + month + "_"   

    if monthly == 1:
        thresh = thresh * 5

    for ind1 in cat.index:
        for ind2 in cat.index:
            group_1 = index_dict[ind1]
            group_2 = index_dict[ind2]
            size_1 = cat.loc[ind1, "Intersection Counts"][group_1]
            size_2 = cat.loc[ind2, "Intersection Counts"][group_2]
            inter = cat.loc[ind1, "Intersection Counts"][group_2]

            if (int(inter) > thresh) and (group_1 < group_2):
                ldict = {size_1: ind1, size_2: ind2, inter:f"{(inter/max(size_1, size_2)):1.0%}"}
                venn2(subsets = (size_1, size_2, inter), set_labels = (ind1, ind2))#,
                      #subset_label_formatter=lambda r: ldict[r])
                plt.title("Percentage Overlap: " + str(max(size_1, size_2)) + " Units")
                plt.tight_layout()
                image_name = month_image + "venn_" + ind1 + "_" + ind2 + ".png"
                plt.savefig(chart_dir + main_cat + image_name)
                plt.close()
                chart_list.append(Image(chart_dir + main_cat + image_name, width=600, height=400))
    return chart_list
    

def chart_pdf(cat, cat_date, inter_list=None, monthly=0, main_cat="Top 100"):
    content_tmp = []
    bar_list = []

    if inter_list == None:
        inter_list = {}
        ind = 0
        for z in cat.index.tolist():
            inter_list.update({z:ind})
            ind += 1
    
    bar_list = bar_charts(cat, cat_date, monthly, 1, 1, main_cat)
    for graph in bar_list:
        content_tmp.append(graph)
    
    content_tmp.append(Spacer(1, 24))

    venn_list = []
    venn_list = over_chart(cat, cat_date, inter_list, monthly, 5, main_cat)

    for graph in venn_list:
        content_tmp.append(graph)

    content_tmp.append(Spacer(1, 24))

    return content_tmp