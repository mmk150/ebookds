import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS
from reportlab.platypus import  Spacer, Image
from local_settings import report_out
from utils import date_scrape

        
def week_cloud(cat, cat_date, main_cat="", monthly=0):
    content_tmp = []
    word_image = []
    stopwords = set(STOPWORDS)
    #List of words to filter out from the word cloud
    filter_words = ["book", "s", "one", "bestselling", "m", "u",
                    "a", "b", "c", "d", "e", "f", "g", "h", "j", "k",
                    "l", "n", "o", "p", "q", "r", "t", "v", "w",
                    "x", "y", "z", "York Times", "read", "Times Bestseller",
                    "la", "the", "and", "it", "to", "he", "she", "they", "I", "of", "his", "him", "has", "in", "her",
                    "that", "But", "is", "as", "an", "me", "New", "York","will", "author","life","time", "Times","doesn"]
    stopwords.update(filter_words)
    for k in range(cat.shape[0]):
        comment_words = ''
        tokens = cat["Description"][k]
        comment_words += " ".join(tokens) + " "
        try:
            word_cloud = WordCloud(width=500, height=500,
                                scale=2.0,
                                background_color='white',
                                stopwords=stopwords,
                                max_words=100).generate(comment_words)
        except:
            return content_tmp

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), dpi=65, facecolor=None)
        plt.imshow(word_cloud)

        month,date=date_scrape(cat_date)
        month_titler=""

        if monthly == 0:
            plt.title(main_cat + " Tag Cloud: " + cat.index[k], fontsize=23)
        else:
            plt.title(main_cat + " " + month + " Tag Cloud: " + cat.index[k], fontsize=23)
            month_titler= month + "_"
        plt.axis("off")
        plt.tight_layout(pad=0)

        word_image.append(main_cat + "_" + month_titler + "word_plot_" + cat.index[k] + ".png")
        plt.savefig(report_out + cat_date + r"/"+  word_image[k],transparent=True)
        plt.close()

        word_plot = Image(report_out + cat_date + r"/"+ word_image[k], width=500, height=350)
        content_tmp.append(word_plot)

        # Add a spacer
        content_tmp.append(Spacer(1, 24))

    return content_tmp

    