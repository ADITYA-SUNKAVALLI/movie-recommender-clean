# 🎬 Movie Recommender System

A content-based movie recommendation engine that suggests the **top 10 similar movies** based on your selection — powered by cosine similarity and enriched with live movie posters via the TMDB API.

---

## 🚀 Features

- **Content-Based Filtering** — Recommends movies similar to your chosen title using cosine similarity on movie metadata.
- **Bag of Words Vectorization** — Movie metadata is vectorized using BoW for efficient similarity computation.
- **Interactive UI** — Built with Streamlit for a clean, intuitive browsing experience.
- **Live Movie Posters** — Fetches dynamic poster images using the [TMDB API](https://www.themoviedb.org/documentation/api).
- **Fast Recommendations** — Precomputed similarity matrices ensure near-instant results.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas / NumPy | Data processing |
| Scikit-learn | BoW vectorization & cosine similarity |
| Streamlit | Interactive web UI |
| TMDB API | Movie poster retrieval |
| Pickle | Precomputed similarity matrix storage |

---

## 📂 Project Structure

```
movie-recommender-clean/
├── app.py                  # Streamlit application
├── movie_list.pkl          # Preprocessed movie data
├── similarity.pkl          # Precomputed cosine similarity matrix
├── notebooks/
│   └── movie_recommender.ipynb  # Data processing & model building
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ADITYA-SUNKAVALLI/movie-recommender-clean.git
cd movie-recommender-clean
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your TMDB API key

Get a free API key at [themoviedb.org](https://www.themoviedb.org/settings/api) and add it to `app.py`:

```python
API_KEY = "aee7c45af0a6b1bcab47d7bd3508363b"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. **Data Preprocessing** — Movie metadata (genres, cast, crew, keywords, overview) is cleaned and combined into a single tag string per movie.
2. **Vectorization** — Tags are converted into numerical vectors using Bag of Words (CountVectorizer).
3. **Similarity Computation** — Cosine similarity is calculated between all movie vectors and saved as a precomputed matrix.
4. **Recommendation** — When a user selects a movie, the top 10 most similar movies are retrieved from the matrix and displayed with their posters.

---

## 📸 Demo

> Select any movie from the dropdown → Click **Recommend** → See your top 10 picks with posters.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Aditya Sunkavalli**
[GitHub](https://github.com/ADITYA-SUNKAVALLI) · [LinkedIn](https://linkedin.com/in/aditya-sunkavalli)
