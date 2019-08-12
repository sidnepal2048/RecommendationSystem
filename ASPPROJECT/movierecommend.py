#import library
import numpy as np
import pandas as pd
# Import libraries from Surprise package
from surprise import Reader, Dataset, SVD, evaluate, accuracy
from surprise.model_selection import KFold, cross_validate
from surprise.model_selection import train_test_split
from sklearn.externals import joblib

# Reading ratings file
ratings = pd.read_csv('F:/ASPPROJECT/ratings.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])

# Reading users file
users = pd.read_csv('F:/ASPPROJECT/users.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])

# Reading movies file
movies = pd.read_csv('F:/ASPPROJECT/movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])
# Load Reader library
#reader = Reader()
#data = Dataset.load_from_df(ratings[['user_id', 'movie_id', 'rating']], reader)
#ratings.head(5)
#trainset, testset = train_test_split(data, test_size=.25)
# We'll use the famous SVD algorithm.
#algo = SVD()
# Train the algorithm on the trainset, and predict ratings for the testset
#algo.fit(trainset)
#predicted_df = algo.test(testset)
# Then compute RMSE
#accuracy.rmse(predicted_df)
#joblib.dump(algo, 'F:/ASPPROJECT/model.pkl')


def recommend_movie(movie_name, user_id):
    model_from_joblib = joblib.load('F:/ASPPROJECT/model.pkl')
    #movie_name = input("search movie ").strip()
    #movies['title'] = movies['title'].str.strip('()')
    #print(movies['title'])
    movie_id = movies[movies['title'].str.match(movie_name)]['movie_id'].values.tolist()
    id = movie_id[0]
    pre = model_from_joblib.predict(user_id, id)
    pre_rating = pre[3:4]
    predicted_rating = round(pre_rating[0])
    user = ratings[(ratings['user_id'] == user_id) & (ratings['rating'] == predicted_rating)]
    user = user.set_index('movie_id')
    user = user.join(movies)['title']
    movie_list = []
    for mov in user:
        movie_list.append(mov)
    return movie_list[0:7]




