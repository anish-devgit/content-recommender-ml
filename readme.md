<h1 align="center">🎬 CineMatch</h1>
<h3 align="center">A production-ready content-based movie recommendation engine</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/scikit--learn-1.3-orange?style=flat-square&logo=scikit-learn" />
  <img src="https://img.shields.io/badge/Deployed-Heroku-purple?style=flat-square&logo=heroku" />
  <img src="https://img.shields.io/badge/NLP-TF--IDF-green?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
</p>
<p align="center">
  <a href="YOUR_HEROKU_URL">🚀 Live Demo</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#%EF%B8%8F-installation">Quick Start</a> •
  <a href="#%EF%B8%8F-architecture--workflow">Architecture</a>
</p>

## 🔍 Overview
CineMatch is a content-based movie recommendation system that suggests films based on their semantic similarity to a title you love. Rather than relying on user ratings or collaborative behavior, it analyzes movie metadata — genres, cast, crew, keywords, and plot overviews — to build a rich feature space and surface the most similar films using cosine similarity.
Built end-to-end: from raw data ingestion and NLP preprocessing to a deployed, interactive web application — this project mirrors a real-world ML product pipeline.

## 🚀 Live Demo

🌐 **Try it live →** [cinematch.herokuapp.com](https://cinematch.herokuapp.com) *(Update with your actual Heroku URL)*

Enter any movie title and get 5–10 intelligent recommendations in under a second.
<!-- Show Image -->

## ✨ Features

- 🎯 **Smart Content Analysis** — Combines genres, cast, crew, keywords, and plot to build a holistic movie profile
- ⚡ **Sub-second Recommendations** — Pre-computed similarity matrix enables near-instant results
- 🧠 **NLP-Powered Matching** — TF-IDF vectorization extracts meaningful signal from unstructured text
- 📐 **Cosine Similarity Engine** — Mathematically finds the closest movies in high-dimensional feature space
- 🌐 **Live Web App** — Interactive Streamlit UI deployed on Heroku, accessible without any local setup
- 🔧 **Modular Pipeline** — Cleanly separated preprocessing, modeling, and serving layers
- 📦 **Serialized Model Artifacts** — Trained artifacts stored with pickle for efficient loading at inference time

## 🛠️ Tech Stack

**Machine Learning & NLP**
| Tool | Purpose |
|------|---------|
| `scikit-learn` | TF-IDF Vectorizer, cosine similarity computation |
| `NLTK` | Text preprocessing, Porter stemming |
| `pandas` / `numpy` | Data wrangling and matrix operations |

**Backend & Serving**
| Tool | Purpose |
|------|---------|
| `Streamlit` | Interactive web frontend |
| `pickle` | Model serialization for fast loading |
| `requests` | TMDB API integration for movie posters |

**Deployment**
| Tool | Purpose |
|------|---------|
| `Heroku` | Cloud deployment platform |
| `gunicorn` | Production WSGI server |
| `Procfile` | Heroku process configuration |

## 🏗️ Architecture / Workflow

```text
Raw Data (TMDB 5000)
        │
        ▼
┌─────────────────────┐
│   Data Preprocessing │  ← Merge datasets, handle nulls, parse JSON cols
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Feature Engineering │  ← Combine: genres + cast + crew + keywords + overview
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   NLP Vectorization  │  ← TF-IDF on "tags" column → sparse matrix
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Similarity Compute  │  ← Cosine similarity → (5000 × 5000) matrix
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Model Artifacts    │  ← Pickle: movies_dict.pkl + similarity.pkl
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Streamlit App      │  ← Load artifacts → recommend() → display with posters
└────────┬────────────┘
         │
         ▼
    Heroku Cloud
```

## 🧠 How It Works

### 1. Data Preparation
We use the TMDB 5000 Movie Dataset (movies + credits CSV files). After merging on `movie_id`, we extract and clean:
- **genres** → parsed from JSON, flattened to list of strings
- **cast** → top 3 actors, spaces removed to treat as single tokens (e.g., `SamWorthington`)
- **crew** → director name only
- **keywords** → extracted and normalized
- **overview** → tokenized plot summary

### 2. Feature Engineering — The "Tags" Column
All features are concatenated into a single `tags` column per movie:
```python
df['tags'] = (
    df['overview'] + ' ' +
    df['genres'].apply(lambda x: ' '.join(x)) + ' ' +
    df['keywords'].apply(lambda x: ' '.join(x)) + ' ' +
    df['cast'].apply(lambda x: ' '.join(x)) + ' ' +
    df['crew']
)
```
Stemming is applied via NLTK's `PorterStemmer` to normalize word forms (loved → love, fighting → fight).

### 3. Vectorization
`TfidfVectorizer` converts the tags into a 5000 × 5000 sparse matrix, capturing term importance across the corpus:
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(df['tags'])
```

### 4. Cosine Similarity
We compute pairwise cosine similarity across all movie vectors:
```python
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)
# Shape: (5000, 5000) — each cell is similarity score between two movies
```

### 5. Recommendation at Inference
Given a movie title, we locate its row, sort similarity scores descending, and return the top N:
```python
def recommend(movie, n=5):
    idx = df[df['title'] == movie].index[0]
    scores = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    return [df.iloc[i[0]].title for i in scores[1:n+1]]
```

## ⚙️ Installation

**Prerequisites**
- Python 3.9+
- pip or conda

**Setup**
```bash
# 1. Clone the repository
git clone https://github.com/anish-devgit/content-recommender-ml.git
cd content-recommender-ml

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
🖥️ App will launch at `http://localhost:8501`

## 🖥️ Usage
1. Open the app (locally or via the Heroku link)
2. Type or select any movie from the dropdown
3. Click "Get Recommendations"
4. View 5 recommended movies with posters, fetched live from the TMDB API

### 📸 Screenshots
- Home Screen
- Recommendations Output
<!-- Show Image -->
<!-- Show Image -->

## 🚢 Deployment (Heroku)

**Required Files**
| File | Content |
|------|---------|
| `Procfile` | `web: sh setup.sh && streamlit run app.py` |
| `setup.sh` | Streamlit server config (headless mode) |
| `runtime.txt` | `python-3.10.12` |
| `requirements.txt` | All pinned dependencies |

**Deploy Steps**
```bash
# 1. Login to Heroku CLI
heroku login

# 2. Create a new Heroku app
heroku create cinematch-app

# 3. Set Python buildpack
heroku buildpacks:set heroku/python

# 4. Push to Heroku
git add .
git commit -m "deploy: initial production release"
git push heroku main

# 5. Open your live app
heroku open
```

**setup.sh**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml
```

## 🔮 Future Improvements
- **Hybrid Filtering** — Blend content-based scores with collaborative filtering (SVD via Surprise library)
- **Transformer Embeddings** — Replace TF-IDF with all-MiniLM-L6-v2 (Sentence-BERT) for deeper semantic understanding
- **REST API Layer** — Expose `/recommend?movie=Inception&n=5` via FastAPI for programmatic access
- **User Session Personalization** — Store watch history in Streamlit session state to refine recommendations
- **A/B Testing Framework** — Compare recommendation strategies with click-through rate tracking
- **Docker + GitHub Actions CI/CD** — Containerize and automate test + deploy pipeline
- **Thumbs Up/Down Feedback** — Collect implicit signals to retrain and improve the model
- **Genre & Year Filters** — Let users constrain recommendations by genre, decade, or language

## 🤝 Contributing
Contributions are welcome and appreciated!
```bash
# Fork → Clone → Branch
git checkout -b feature/your-feature-name

# Make changes → Commit (follow Conventional Commits)
git commit -m "feat: add genre filter to recommendation API"

# Push → Open Pull Request
git push origin feature/your-feature-name
```
Please ensure all PRs include relevant tests and updated documentation.

## 📄 License
This project is licensed under the MIT License — see LICENSE for full details.

## 👤 Author
**anish-devgit**
<!-- Show Image -->
<!-- Show Image -->
<!-- Show Image -->

---

<p align="center">
  Found this useful? Give it a ⭐ — it helps others discover the project!
</p>