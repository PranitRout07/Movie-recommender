import streamlit as st
import base64
import pickle
import pandas as pd
import requests
import zipfile



movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = None
with zipfile.ZipFile('similarity.zip', 'r') as zip_ref:
    # Extract the pkl file from the zip file
    zip_ref.extract('similarity.pkl')
    # Load the extracted pkl file
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f24d85ecd7048d4729f7f143b9ca6ab8&append_to_response=videos,images')
    # print(response,"response")
    data = response.json()
    # print(data,"data")
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def recommend(movie):
    # print("i")
    movie_index = movies[movies['title']==movie].index[0]
    # print(movie_index,"movie_index")
    distances = similarity[movie_index]
    # print("distances",distances)
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    reccomended_movies = []
    reccomended_movies_posters = []
    for i in movies_list:
        print(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].id
        print("movieid",movie_id)
        reccomended_movies.append(movies.iloc[i[0]].title)
        reccomended_movies_posters.append(fetch_poster(movie_id))
    return reccomended_movies,reccomended_movies_posters





st.set_page_config(
    layout="wide"
)

background_image_path = "pexels-pixabay-52732.jpg"  # Replace with the path to your image file
background_image_bytes = open(background_image_path, "rb").read()

background_image_encoded = base64.b64encode(background_image_bytes).decode()

st.markdown(
    f"""
    <style>
    body {{
        background-image: url('data:image/jpeg;base64,{background_image_encoded}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed; /* Ensures the background image stays fixed while scrolling */
        height: 100vh; /* Sets the height of the body element to full viewport height */
        margin: 0;
        padding: 0;
    }}
    .stApp {{
        background-color: transparent;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Choose a movie name?',
    movies['title'].values
)


if st.button('Recommend'):



    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    card_style = """
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        border: 1px solid #E8E8E8;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        background-color: #16161D;
        transition: box-shadow 0.3s ease;
        cursor: pointer;
        margin-bottom: 20px;
        width: 200px;
    """

    image_style = """
        width: 100%;
        height: auto;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    """

    text_style = """
        font-size: 18px;
        font-weight: bold;
        margin: 10px 0;
        color: #D3D3D3;
    """

    with col1:
        st.markdown(
            f"""
            <div class="card" style="{card_style}">
                <img src="{posters[0]}" alt="Movie Poster" style="{image_style}">
                <h3 style="{text_style}">{names[0]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="card" style="{card_style}">
                <img src="{posters[1]}" alt="Movie Poster" style="{image_style}">
                <h3 style="{text_style}">{names[1]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="card" style="{card_style}">
                <img src="{posters[2]}" alt="Movie Poster" style="{image_style}">
                <h3 style="{text_style}">{names[2]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="card" style="{card_style}">
                <img src="{posters[3]}" alt="Movie Poster" style="{image_style}">
                <h3 style="{text_style}">{names[3]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div class="card" style="{card_style}">
                <img src="{posters[4]}" alt="Movie Poster" style="{image_style}">
                <h3 style="{text_style}">{names[4]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

