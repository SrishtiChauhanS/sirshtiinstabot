import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

os.chdir("C:\Users\srishti\Desktop")
text = open('fest.txt' , "r")
data = text.read()

plt.figure(figsize=(20,10))
wordcloud= WordCloud(background_color='red', mode="CMYK", width=2000, height=1000).generate(data)

plt.title("fest.txt wordcloud")
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


