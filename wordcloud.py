
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)




# Read the whole text.
text = open(path.join(d, 'fifaWC.txt')).read()

# read the mask image

fifaWC_mask = np.array(Image.open(path.join(d, "fifaWC_mask.jpg")))

stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=fifaWC_mask,
               stopwords=stopwords)

# generate word cloud

wc.generate(text)

# store to file

wc.to_file(path.join(d, "fifaWC.jpg"))



plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(fifaWC_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()