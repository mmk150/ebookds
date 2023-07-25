import matplotlib.pyplot as plt
import pandas as pd


from reportlab.platypus import Spacer, Image
from local_settings import report_out
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from utils import date_scrape




def ebars(x_val, data):
    y_val = data.loc[data["Date"]==x_val, "Avg. Sales Rank"]
    dev = data.loc[data["Date"]==x_val, "Sales Rank Std. Variation"]
    return (y_val-dev, y_val+dev)

def invert_line(data, cat, month):
    rot = 45
    num_x = len(data.index)
    plt.errorbar(data.iloc[:, 0], data.iloc[:, 1], yerr=data.iloc[:, 2], ecolor='red', lw=2, capsize=5, capthick=2)
    # 100 to 200
    # 200 to 500
    # 500 to 1000
    # 1000 to 2500
    # 2500 to 5000
    # 5000 to 10000
    # 10000 to 20000
    # 20000 to 40000
    # 40000 to 100000
    # 100000 to 200000
    # 200000 to 500000
    # 500000 to 1000000
    y_set = data.iloc[:, 1].max()
    if y_set < 100:
        plt.ylim(-1, 200)
    elif y_set < 200:    
        plt.ylim(-1, 500)
    elif y_set < 500:    
        plt.ylim(-1, 1000)
    elif y_set < 1000:    
        plt.ylim(-1, 2500)    
    elif y_set <2500:
        plt.ylim(-10, 5000)
    elif y_set <5000:
        plt.ylim(-10, 10000)
    elif y_set <10000:
        plt.ylim(-10, 20000)
    elif y_set <20000:
        plt.ylim(-10, 40000)
    elif y_set <40000:
        plt.ylim(-10, 100000)
    else:
        plt.ylim(-100, 200000)
    plt.gca().invert_yaxis()
    plt.xticks(data.index, data.iloc[:, 0], rotation=rot)
    plt.grid(visible=False)
    plt.ylabel('Average Sales Ranking')
    plt.title("Average Sales Trends: " + cat)
    plt.tight_layout()
    plt.savefig(report_out + r"/" + month +"_"+cat +"_trends.png")
    plt.close()
    return Image(report_out + r"/" + month +"_"+cat +"_trends.png", width=600, height=400)

def month_trend(frame_list, date_list):
    content = []
    month, day = date_scrape(date_list[-1])
    for category in frame_list[0].index:
        dates = []
        avgs = []
        stds = []
        for index in range(0, len(frame_list)):
            frame = frame_list[index]
            dates.append(date_list[index].replace('_', '/'))
            avgs.append(frame.loc[category, "Avg. Sales Rank"])
            stds.append(frame.loc[category, "Avg. Sales Deviation"])
            index+=1
        category_frame = pd.DataFrame({"Date":dates, "Avg. Sales Rank":avgs, "Sales Rank Std. Variation":stds})
        content.append(Spacer(1, 24))
        content.append(invert_line(category_frame, category, month))
    return content