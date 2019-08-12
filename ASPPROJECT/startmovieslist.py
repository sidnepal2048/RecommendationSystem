import numpy as np
import pandas as pd
from sklearn.utils import shuffle

# Reading movies file
movies = pd.read_csv('F:/ASPPROJECT/movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])
movie_list = shuffle(movies)
movie_list = movie_list['title'].values.tolist()
movielist = movie_list[0:5]

