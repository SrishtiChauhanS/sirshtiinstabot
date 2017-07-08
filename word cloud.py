
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)
#myfile = open('C:/Users/narae/Desktop/alice.txt')   # Windows
#mytext = myfile.read()\
 #   myfile.close()


# Read the whole text.
text = open(path.join(d, 'fest.txt')).read()

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
fest_mask = np.array(Image.open(path.join(d, "fest_mask.jpg")))

stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=fest_mask,
               stopwords=stopwords)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "fest.jpg"))

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(fest_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()