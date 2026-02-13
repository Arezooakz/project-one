import streamlit as st
import pandas as pd

from API import omdb_search, omdb_get_by_imdb_id, normalize_omdb_movie
from data import init_db, insert_movie, get_all_movies, search_local_movies , get_stats, get_latest_movies 
#-----------------------------
st.set_page_config(page_title="Cinema System", page_icon="🎬", layout="wide")
init_db()

st.title("🎬 Cinema System")

st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choose", ("Home", "Search Online", "Local Library"))

def df_local(rows):
    return pd.DataFrame(rows, columns=["id", "movie_name", "release_year", "genre", "director", "imdb_id", "imdb_rating"])
#------------------------------
if page == "Home":
    
    st.write("Search movies in OMDb and save them to your local cinema database.")

    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("🔎 Search in OMDb\n\nGo to **Search** to find movies online.")
    with c2:
        st.info("💾 Local Library\n\nSee your saved movies in **Library**.")
    with c3:
        st.info("➕ Add Manually\n\nAdd your own movie data in **Add**.")

    st.divider()

    
    total, genres, avg_year = get_stats()
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Movies (Local)", total)
    k2.metric("Genres", genres)
    k3.metric("Average Release Year", "-" if avg_year is None else int(avg_year))

    st.divider()

    
    st.subheader("Latest added movies")
    latest = get_latest_movies(limit=5)

    if not latest:
        st.warning("No movies saved yet. Go to Search and save your first movie.")
    else:
        for mid, name, year, genre, director in latest:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                with left:
                    st.markdown(f"**{name}**")
                    st.write(f"Year: {year} | Genre: {genre} | Director: {director}")
                with right:
                    st.caption(f"ID: {mid}")

elif page == "Search Online":
    st.subheader("🔎 Search in OMDb")

    query = st.text_input("Enter movie name")
    if query.strip():
        res = omdb_search(query.strip())

        if res.get("Response") != "True":
            st.error(res.get("Error", "Movie not found"))
        else:
            results = res.get("Search", [])
            options = [f"{m['Title']} ({m['Year']}) — {m['imdbID']}" for m in results]
            picked = st.selectbox("Results", options)

            imdb_id = picked.split("—")[-1].strip()
            detail = omdb_get_by_imdb_id(imdb_id)

            if detail.get("Response") != "True":
                st.error(detail.get("Error", "Could not load details"))
            else:
                record = normalize_omdb_movie(detail)

                col1, col2 = st.columns([1, 2])
                with col1:
                    if record.get("poster"):
                        st.image(record["poster"], use_container_width=True)
                with col2:
                    st.markdown(f"### {record.get('movie_name')}")
                    st.write("Year:", record.get("release_year"))
                    st.write("Genre:", record.get("genre"))
                    st.write("Director:", record.get("director"))
                    st.write("IMDb Rating:", record.get("imdb_rating"))
                    st.write("Plot:", record.get("plot"))

                if st.button("Save to database"):
                    insert_movie(
                        record.get("movie_name"),
                        record.get("release_year"),
                        record.get("actor_numbers"),
                        None, 
                        record.get("genre"),
                        record.get("director"),
                        record.get("imdb_id"),
                        record.get("imdb_rating"),
                        record.get("plot"),
                        record.get("poster")
                    )
                    st.success("Saved (or already exists).")

elif page == "Local Library":
    st.subheader(" Local Movies")

    tab1, tab2 = st.tabs(["All", "Search"])
    with tab1:
        rows = get_all_movies()
        st.dataframe(df_local(rows), use_container_width=True)

    with tab2:
        q = st.text_input("Search in local DB")
        if q.strip():
            rows = search_local_movies(q.strip())
            st.dataframe(df_local(rows), use_container_width=True)
