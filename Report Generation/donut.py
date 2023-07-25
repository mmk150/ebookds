import matplotlib.pyplot as plt


from reportlab.platypus import Image
from local_settings import report_out
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})





def donut(categories_bincount_by_num_books,categories_labels, cat_date):

    combined_arr = [ [categories_bincount_by_num_books[i], categories_labels[i]]  for i in range(len(categories_bincount_by_num_books)) ]

    combined_arr.sort(key=lambda x: 0-x[0])
    

    combined_arr_bin = [combined_arr[i][0] for i in range(len(combined_arr)) ]
    combined_arr_label = [  combined_arr[i][1]  for i in range(len(combined_arr)) ]

    cat_count_arr=[]
    label_arr=[]
    percent_max=int(.95*sum(combined_arr_bin))
    cats_max=12
    sum1=0
    cat_sum=0

    for i in range(len(combined_arr_bin)):
        if combined_arr_bin[i]==1:
            cat_count_arr.append(sum(combined_arr_bin[i+1:]))
            label_arr.append("misc")
            break

        cat_count_arr.append(combined_arr_bin[i])
        label_arr.append(combined_arr_label[i])
        sum1+=combined_arr_bin[i]
        cat_sum+=1

        if cat_sum>cats_max or sum1>percent_max:
            cat_count_arr.append(sum(combined_arr_bin[i+1:]))
            label_arr.append("misc")
            break

    figure_pie=plt.pie(cat_count_arr,labels=label_arr)
    whitespace_circle=plt.Circle((0,0),0.7, color='white')
    figure_donut=plt.gcf()
    figure_donut.gca().add_artist(whitespace_circle)

    plt.title("Normalized Market Share in Top 100 Ranking")
    plt.tight_layout()

    image_name = "donut.png"
    chart_dir = report_out + cat_date + r"/"
    plt.savefig(chart_dir + image_name)
    plt.close()
    
    return Image(chart_dir + image_name, width=600, height=400)



