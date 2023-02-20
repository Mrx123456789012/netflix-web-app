import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import requests

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = diff[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append((movies.iloc[i[0]].title, movies.iloc[i[0]].imdb_id))
    return recommended_movies


movies_dict = pickle.load(open("movies_dict2.pkl","rb"))
movies_dict_result = movies_dict()
movies = pd.DataFrame(movies_dict_result)

diff = pickle.load(open('similarity.pkl','rb'))

# Set the background color to black
st.markdown(
    f"""
    <h1 style='text-align: center; color: red;'>NETFLIX RECOMMENDATION SYSTEM BY MD SHADAN</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

movie_name = st.selectbox(
    'search movies',
    movies['title'].values
    )

if st.button('Recommend'):
    recommended_movies = recommend(movie_name)
    for recommended_movie in recommended_movies:
        st.write(f"**{recommended_movie[0]} ({recommended_movie[1]})**")   # display the recommended movie title and summary
        imdb_id = recommended_movie[1]  # get the imdb_id of the recommended movie
        recommended_movie_df = movies[movies['imdb_id'] == imdb_id]  # filter the dataset for the recommended movie
        image_url = recommended_movie_df['image_url'].values[0]  # extract the image URL for the recommended movie
        image = Image.open(requests.get(image_url, stream=True).raw)  # retrieve the image from the URL
        st.image(image)  # display the image
