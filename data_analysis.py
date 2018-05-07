import pandas as pd
import matplotlib.pyplot as plt

font_data = pd.read_csv("font_data.csv", sep=",")
fd = font_data[font_data['rating'] != 0].hist('rating')
rating_counts = font_data.groupby('rating').nunique()
print "Non zero font count: {}".format(rating_counts[1:].sum()[0])
plt.show()
