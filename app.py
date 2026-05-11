import streamlit as st
import pickle
import requests
import os
import gdown
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -----------------------------------
# DOWNLOAD similarity.pkl IF NOT EXISTS
# -----------------------------------

FILE_ID = "1zh6Yew0IZwFs4JYo3DmlUXfmK2dhin-9"

if not os.path.exists("similarity.pkl"):

    url = f"https://drive.google.com/uc?id={FILE_ID}"

    gdown.download(url, "similarity.pkl", quiet=False, fuzzy=True)


# --- CONFIG ---
API_KEY = "aee7c45af0a6b1bcab47d7bd3508363b"

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1)))

@st.cache_resource
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# --- STYLING ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    p, span, label { color: #FFFFFF !important; }
    
    .movie-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 8px;
    height: 3.5em; 
    min-height: 3.5em;
    max-height: 3.5em;
    
    overflow: hidden;
    color: #FFFFFF;
    text-align: center;
    line-height: 1.2;
    
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
    .stButton>button {
        width: 100%;
        background-color: #E50914;
        color: white !important;
        border: none;
        font-weight: bold;
        height: 3em;
    }
    .movie-link {
        color: #E50914 !important;
        text-decoration: none;
        font-size: 0.75rem;
        display: block;
        text-align: center;
        margin-bottom: 20px;
    }
    .stProgress > div > div > div > div {
        background-color: #E50914;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
@st.cache_data(show_spinner=False)
def fetch_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        res = session.get(url, timeout=3).json()
        poster = f"https://image.tmdb.org/t/p/w500{res.get('poster_path')}" if res.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Image"
        return poster, res.get('homepage')
    except:
        return "https://via.placeholder.com/500x750?text=Error", None

def get_recommendations(movie_name):
    idx = movies[movies['title'] == movie_name].index[0]
    # Fetching top 10 instead of 5
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:11]
    return [(movies.iloc[i[0]].id, movies.iloc[i[0]].title) for i in distances]

# --- UI ---
st.title("🎬 Movie Recommender")
selected_movie = st.selectbox("Search for a movie...", movies['title'].values)

if st.button('Get Recommendations'):
    loading_text = st.empty()
    progress_bar = st.progress(0)
    
    loading_text.markdown("<h3 style='text-align: center; color: #E50914;'>🎬 Finding top 10 movies for you...</h3>", unsafe_allow_html=True)
    
    recs_data = get_recommendations(selected_movie)
    
    # Grid logic: 2 rows of 5 for better responsiveness
    for row in range(2):
        cols = st.columns(5)
        for col_idx in range(5):
            movie_idx = (row * 5) + col_idx
            m_id, title = recs_data[movie_idx]
            
            # Update progress (10% per movie)
            progress_bar.progress((movie_idx + 1) * 10)
            
            with cols[col_idx]:
                poster, link = fetch_details(m_id)
                st.image(poster, use_container_width=True)
                st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
                if link:
                    st.markdown(f"<a href='{link}' target='_blank' class='movie-link'>Visit Site 🔗</a>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size:0.7rem; text-align:center; color:gray; margin-bottom:20px;'>No Site Available</p>", unsafe_allow_html=True)

    loading_text.empty()
    progress_bar.empty()
    st.success(f"Top 10 recommendations for '{selected_movie}'")
