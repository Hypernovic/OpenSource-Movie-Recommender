import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy

def get_data():
    movie_data = pd.read_csv('data.csv')
    movie_data['original_title'] = movie_data['original_title'].str.lower()
    return movie_data



def combine_data(data):
    data_recommend = data.drop(columns=['movie_id', 'original_title','plot'])
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(
                                                                         lambda x: ','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data_recommend.drop(columns=[ 'cast','genres'])
    return data_recommend

def transform_data(data_combine, data_plot):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['combine'])

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_plot['plot'])

    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
    
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim

find_movie = get_data()
combine_result = combine_data(find_movie)
transform_result = transform_data(combine_result,find_movie)
indices = pd.Series(find_movie.index, index = find_movie['original_title'])

def recommend_movies(listing, data, transform):
    index=indices[0]
    addition=transform[index]
    addition=addition*0

    for i in listing:
        index=indices[i]
        addition=addition+transform[index]
        
    sim_scores = list(enumerate(addition))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    size=len(listing)
    sim_scores = sim_scores[size:size+21]
    
    movie_indices = [i[0] for i in sim_scores]

    movie_id = data['movie_id'].iloc[movie_indices]
    movie_title = data['original_title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]
    movie_poster = data['poster'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['Movie_Id','Name','Genres','poster'])

    recommendation_data['Movie_Id'] = movie_id
    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres
    recommendation_data['poster'] = movie_poster


    return recommendation_data

def giveDummy():
    movie_indices=indices[0:20]
    movie_id = find_movie['movie_id'].iloc[movie_indices]
    movie_title = find_movie['original_title'].iloc[movie_indices]
    movie_genres = find_movie['genres'].iloc[movie_indices]
    movie_poster = find_movie['poster'].iloc[movie_indices]
    
    dummy_data = pd.DataFrame(columns=['Movie_Id','Name','Genres','poster'])

    dummy_data['Movie_Id'] = movie_id
    dummy_data['Name'] = movie_title
    dummy_data['Genres'] = movie_genres
    dummy_data['poster'] = movie_poster


    return dummy_data.to_dict('records')

def search(string):


    new= find_movie.loc[find_movie["original_title"].str.contains(string.lower())][0:10]
    # movie_id = new['movie_id']
    # movie_title = new['original_title']
    # movie_genres = new['genres']
    # movie_poster= new['poster']
    return new.to_dict('records')




def results(movie_list):
    movie_list = list(map(str.lower, movie_list))
    print(movie_list)
    recommendations = recommend_movies(movie_list, find_movie, transform_result)
    check=recommendations.to_dict('records')

    return check
