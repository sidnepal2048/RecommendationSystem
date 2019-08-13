#import numpy as np
#import pandas as pd
#from sklearn.utils import shuffle

# Reading movies file
#movies = pd.read_csv('F:/ASPPROJECT/movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])
#movie_list = shuffle(movies)
#movie_list = movie_list['title'].values.tolist()
#movielist = movie_list[0:5]


import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from scipy.sparse.linalg import svds
# Reading ratings file
ratings = pd.read_csv('F:/ASPPROJECT/ratings.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating', 'timestamp'])

# Reading users file
users = pd.read_csv('F:/ASPPROJECT/users.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])

# Reading movies file
movies = pd.read_csv('F:/ASPPROJECT/movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])
n_users = ratings.user_id.unique().shape[0]
n_movies = ratings.movie_id.unique().shape[0]
Ratings = ratings.pivot(index = 'user_id', columns ='movie_id', values = 'rating').fillna(0)
R = Ratings.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
Ratings_demeaned = R - user_ratings_mean.reshape(-1, 1)
sparsity = round(1.0 - len(ratings) / float(n_users * n_movies), 3)
U, sigma, Vt = svds(Ratings_demeaned, k = 50)
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds = pd.DataFrame(all_user_predicted_ratings, columns = Ratings.columns)


#function that user hasn't rated movies
def recommend_movies(userID, num_recommendations):

    # Get and sort the user's predictions
    user_row_number = userID - 1 # User ID starts at 1, not 0
    sorted_user_predictions = preds.iloc[user_row_number].sort_values(ascending=False) # User ID starts at 1

    # Get the user's data and merge in the movie information.
    user_data = ratings[ratings.user_id == (userID)]
    user_full = (user_data.merge(movies, how = 'left', left_on = 'movie_id', right_on = 'movie_id').sort_values(['rating'], ascending=False))

    print ('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print ('Recommending highest {0} predicted ratings movies not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies[~movies['movie_id'].isin(user_full['movie_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'movie_id',
               right_on = 'movie_id').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).iloc[:num_recommendations, :-1])

    return user_full, recommendations


#actual, predictions = recommend_movies(1, 10)
#movie_predict = predictions.iloc[:, 1:]
#movie_predict.iloc[:, 1:]

#actual, predictions = recommend_movies(1310, 10)
#print(actual['title'])
#print(predictions)
