import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from local_vars import image_dir,rank_dir


rankings_file=rank_dir + r"\average_rankings.txt"

#grab the ranking data
def getRanking(image_filename, text_file):
    with open(text_file, 'r') as f:
        for line in f:
            name, full = line.strip().split(': ')
            rank,count=full.strip().split(",")
            rank=rank.strip()
            count=count.strip()
            if name == image_filename:
                return float(rank),int(count)
    return None  # Return None if no match was found


# function to get the 4 most abundant colors with KMeans
def get_top_colors(image_path, n_colors):
    
    image = Image.open(image_path)
    image = image.resize((50, 50))
    np_image = np.array(image)
    reshaped_image = np_image.reshape(-1, 3)

    # Perform K-means clustering to find the most dominant colors
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(reshaped_image)

    colors = kmeans.cluster_centers_
    colors = colors.round(0).astype(int)

    return colors

# process each image
dominant_colors = {}
for filename in os.listdir(image_dir):
    print("files")
    print(filename)
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # check the image format
        colors=get_top_colors(os.path.join(image_dir, filename), 6)
        ranking,num_weeks=getRanking(filename.replace(".jpg",""),rankings_file)
        dominant_colors[filename]=(colors,ranking,num_weeks)

print(dominant_colors)
sorted_colors = dict(sorted(dominant_colors.items(), key=lambda item: item[1][1]))


size=len(sorted_colors)
cols=7
rows=7

fig, axs = plt.subplots(rows+1, cols, figsize=(cols, rows*2))
fig.subplots_adjust(bottom=0.1, top=0.90, wspace=1.2, hspace=1.8)
for i in range(len(axs.flat)):
    ax=axs.flat[i]
    for sp in ax.spines.values():
        sp.set_visible(False)
        print("line 59")
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

for i, (filename,(colors,ranking,num_weeks)) in enumerate(sorted_colors.items()):
    if i>=50:
        break
    ax = axs.flat[i]
    ax.imshow([colors], aspect='auto')
    ax.set_title(f'Avg. Rank:\n {ranking:.2f}\n#Weeks: {num_weeks:.2f}',pad=6,fontdict={'fontsize': 10})
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax.autoscale(tight=True)

plt.show()
