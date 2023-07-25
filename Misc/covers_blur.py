import os
import io
from PIL import Image
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
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
    return None



# process each image
image_list={}
for filename in os.listdir(image_dir):
    print("files")
    print(filename)
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # check the image format

        img = Image.open(os.path.join(image_dir, filename))
        small = img.resize((256,256*2), resample=Image.NEAREST)
        result = small.resize(img.size, Image.NEAREST)
        result = result.filter(ImageFilter.GaussianBlur(12))

        bytes_arr=io.BytesIO()
        result.save(bytes_arr,format='PNG')
        ranking,num_weeks=getRanking(filename.replace(".jpg",""),rankings_file)
        image_list[filename]=(bytes_arr.getvalue(),ranking,num_weeks)


sorted_img = dict(sorted(image_list.items(), key=lambda item: item[1][1]))
size=len(sorted_img)

cols=7
rows=7
fig, axs = plt.subplots(rows+1, cols, figsize=(128, 128))
fig.subplots_adjust(bottom=0.1, top=0.90, wspace=0.3, hspace=0.7)

for i in range(len(axs.flat)):
    ax=axs.flat[i]
    for sp in ax.spines.values():
        sp.set_visible(False)
        print("line 59")
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

for i, (filename,(image,ranking,num_weeks)) in enumerate(sorted_img.items()):
    if i>=50:
        break
    ax = axs.flat[i]
    byte_stream=io.BytesIO(image)
    img=Image.open(byte_stream)
    ax.imshow(img)
    ax.set_title(f'Avg. Rank:\n {ranking:.2f}\n#Weeks: {num_weeks:.2f}',pad=2,fontdict={'fontsize': 8})

fig.suptitle("Book cover display for the SF&F- Fantasy Subcategory",fontsize=20)
plt.show()
