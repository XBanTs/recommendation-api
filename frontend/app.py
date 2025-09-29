import streamlit as st
import requests

API_URL = "https://recommendation-api-3wqy.onrender.com/"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System API")

# Fetch movies
try:
    movies = requests.get(f"{API_URL}/movies/").json()
    movie_titles = [m["title"] for m in movies] if isinstance(movies, list) else []
except Exception as e:
    st.error("❌ Could not load movies from API. Make sure FastAPI is running.")
    st.stop()

if not movie_titles:
    st.info("No movies available in the database. Please add some movies first.")
    st.stop()

# --- Recommendation Section ---
st.header("🔎 Get Movie Recommendations")
selected_movie = st.selectbox("Select a movie:", movie_titles, key="rec_movie")

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.get(f"{API_URL}/recommend/{selected_movie}")
            if response.status_code == 200:
                data = response.json()
                st.subheader(f"Recommendations for: **{data['input']}**")

                if "message" in data:
                    st.warning(data["message"])
                elif data.get("recommendations"):
                    for i, rec in enumerate(data["recommendations"], start=1):
                        st.write(f"**{i}. {rec}**")
                else:
                    st.info("No recommendations found.")
            else:
                st.error(f"⚠️ Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Could not fetch recommendations: {e}")


# --- Rating Section ---
st.header("⭐ Rate a Movie")

with st.form("rating_form"):
    user_id = st.number_input("User ID", min_value=1, step=1)
    movie_to_rate = st.selectbox("Choose a movie to rate:", movie_titles, key="rate_movie")
    rating_value = st.slider("Your Rating", 0.0, 5.0, 3.0, 0.5)
    
    submitted = st.form_submit_button("Submit Rating")
    if submitted:
        try:
            # Find the movie_id of the selected title
            movie_obj = next((m for m in movies if m["title"] == movie_to_rate), None)
            if not movie_obj:
                st.error("⚠️ Movie not found in database.")
            else:
                payload = {
                    "user_id": user_id,
                    "movie_id": movie_obj["movie_id"],
                    "rating": rating_value
                }
                response = requests.post(f"{API_URL}/rate/", json=payload)

                if response.status_code == 200:
                    st.success("✅ Rating submitted successfully! Model retrained.")
                else:
                    st.error(f"⚠️ Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Could not submit rating: {e}")
