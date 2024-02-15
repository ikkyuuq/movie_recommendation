from db import (
    get_database_connection, commit_and_close,
    disable_foreign_key_checks, enable_foreign_key_checks
)
from config import BASE_IMAGE_URL, API_READ_ACCESS_TOKEN
import requests

HEADERS = {'Authorization': f'Bearer {API_READ_ACCESS_TOKEN}'}

def get_genres_data():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    response = requests.get(url, headers=HEADERS)
    genres = response.json().get('genres', [])
    return genres

def get_kinocheck_data(tmdb_id):
    url = f"https://api.kinocheck.com/movies?tmdb_id={tmdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        yt_video_id = data['trailer']['youtube_video_id']
        return yt_video_id
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def get_movies_data(start_page, stop_page):
    all_results = []

    for page_num in range(start_page, stop_page + 1):
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page_num}&sort_by=popularity.desc"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            all_results.extend(response.json().get('results', []))
        else:
            print(f"Error fetching data for page {page_num}: {response.status_code}")

    return all_results

def get_credit_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    
    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            cast = response.json().get('cast', [])
            crew = response.json().get('crew', [])
            actors = filter_cast_members(cast, "Acting")
            directors = find_director(crew, "Directing", job="Director")
            writers = filter_crew_members(crew, department="Writing", job="Writer") or \
                      filter_crew_members(crew, department="Writing", job="Screenplay") or \
                      filter_crew_members(crew, department="Writing")

            return actors, directors, writers
        else:
            print(f"Failed to fetch credit data for movie {movie_id}. Status code: {response.status_code}")
            return {}
    except requests.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return {}

def filter_cast_members(data, department):
    return [{
        'id': member.get('id'),
        'name': member.get('name'),
        'popularity': member.get('popularity'),
        'profile_path': member.get('profile_path')
    } for member in data if (department is None or member.get('known_for_department') == department)]

def find_director(data, department, job=None):
    for member in data:
        if (department is None or member.get('department') == department) and (job is None or member.get('job') == job):
            result = {
                'id': member.get('id'),
                'name': member.get('name'),
                'popularity': member.get('popularity'),
                'profile_path': member.get('profile_path')
            }
    return result

def filter_crew_members(data, department, job=None):
    return [{
        'id': member.get('id'),
        'name': member.get('name'),
        'popularity': member.get('popularity'),
        'profile_path': member.get('profile_path')
    } for member in data if (department is None or member.get('department') == department) and (job is None or member.get('job') == job)]

def process_movie(cursor, conn, movie):
    try:
        conn = get_database_connection()
        cursor =  conn.cursor(buffered=True)  
        cursor.execute("START TRANSACTION")

        disable_foreign_key_checks(cursor, conn)

        movie_id = movie.get('id')
        actor, director, writer = get_credit_data(movie_id)

        # Process Director
        director_id = director.get('id') if director else 0
        director_name_parts = director.get('name', '').split()
        director_fname = director_name_parts[0] if director_name_parts else ""
        director_lname = director_name_parts[1] if len(director_name_parts) > 1 else ""
        director_mname = director_name_parts[2] if len(director_name_parts) > 2 else ""
        director_img_url = director.get('profile_path', "")
        director_popular = director.get('popularity', 0)
        d_full_img = f"{BASE_IMAGE_URL}{director_img_url}" if director_img_url else ""

        # Insert or update Director
        cursor.execute("""
            REPLACE INTO Director (director_id, director_fname, director_mname, director_lname, director_img_url, director_popular)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (director_id, director_fname, director_mname, director_lname, d_full_img, director_popular))
        print("Movie:", movie_id, "Director:", director_id)

        # Process Movie
        movie_title = movie.get('title', "")
        movie_img = movie.get('poster_path', "")
        movie_popular = movie.get('popularity', 0)
        m_full_img = BASE_IMAGE_URL + movie_img if movie_img else ""
        movie_overview = movie.get('overview', "")
        movie_release_date = movie.get('release_date', "")
        movie_rating = movie.get('vote_average', 0)

        # Insert or update Movie
        cursor.execute("""
            REPLACE INTO Movie (movie_id, movie_title, movie_overview, movie_release_date, movie_img_url, movie_rating, movie_popular, director_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (movie_id, movie_title, movie_overview, movie_release_date, m_full_img, movie_rating, movie_popular, director_id))

        # Process Genres
        genres_data = get_genres_data()
        genre_ids = set(movie.get('genre_ids', []))

        for genre in genres_data:
            genre_ID = genre.get('id')
            genre_name = genre.get('name')

            # Insert or update Genre
            cursor.execute("""
                REPLACE INTO Genre (genre_id, genre_title) VALUES (%s, %s)
            """, (genre_ID, genre_name))

            # Insert Movie-Genre relationship if genre is associated with the movie
            if genre_ID in genre_ids:
                cursor.execute("""
                    INSERT INTO Movie_has_Genre (movie_id, genre_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE movie_id=movie_id
                """, (movie_id, genre_ID))
                print("Movie:", movie_id, "Genre:", genre_ID)

        # Process Actors
        for a in actor:
            actor_id = a.get('id')
            actor_name_parts = a.get('name', '').split(" ")
            actor_fname = actor_name_parts[0] if actor_name_parts else ""
            actor_lname = actor_name_parts[1] if len(actor_name_parts) > 1 else ""
            actor_mname = actor_name_parts[2] if len(actor_name_parts) > 2 else ""
            actor_img_url = a.get('profile_path', "")
            actor_popular = a.get('popularity', 0)
            a_full_img = f"{BASE_IMAGE_URL}{actor_img_url}" if actor_img_url else ""

            # Insert or update Actor
            cursor.execute("""
                REPLACE INTO Actor (actor_id, actor_fname, actor_mname, actor_lname, actor_img_url, actor_popular)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (actor_id, actor_fname, actor_mname, actor_lname, a_full_img, actor_popular))

            # Insert Movie-Actor relationship
            cursor.execute("""
                INSERT INTO Movie_has_Actor (movie_id, actor_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE movie_id=movie_id
            """, (movie_id, actor_id))
            print("Movie:", movie_id, "Actor:", actor_id)

        # Process Writers
        for w in writer:
            writer_id = w.get('id')
            writer_name_parts = w.get('name', '').split(" ")
            writer_fname = writer_name_parts[0] if writer_name_parts else ""
            writer_lname = writer_name_parts[1] if len(writer_name_parts) > 1 else ""
            writer_mname = writer_name_parts[2] if len(writer_name_parts) > 2 else ""
            writer_img_url = w.get('profile_path', "")
            writer_popular = w.get('popularity', 0)
            w_full_img = f"{BASE_IMAGE_URL}{writer_img_url}" if writer_img_url else ""

            # Insert or update Writer
            cursor.execute("""
                REPLACE INTO Writer (writer_id, writer_fname, writer_mname, writer_lname, writer_img_url, writer_popular)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (writer_id, writer_fname, writer_mname, writer_lname, w_full_img, writer_popular))

            # Insert Movie-Writer relationship
            cursor.execute("""
                INSERT INTO Movie_has_Writer (movie_id, writer_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE movie_id=movie_id
            """, (movie_id, writer_id))
            print("Movie:", movie_id, "Writer:", writer_id)
        
        yt_video_id = get_kinocheck_data(movie_id)
        
        if yt_video_id:
            cursor.execute("""
                REPLACE INTO YouTubeVideo (yt_video_id, movie_id)
                VALUES (%s, %s)
            """, (yt_video_id, movie_id))
            print("Inserted Video_ID for Movie:", movie_id)

        enable_foreign_key_checks(cursor, conn)
        commit_and_close(conn)
        print("Success")

    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Error during database operation: {e}")
        return None