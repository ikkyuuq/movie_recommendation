from flask import Flask, jsonify, request
from db import get_database_connection, commit_and_close
from models import process_movie, get_movies_data , get_kinocheck_data
import json

app = Flask(__name__)

@app.route("/movies", methods=["GET"])
def get_movies_endpoint():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    query_combined = """
    SELECT
        M.movie_id,
        JSON_OBJECT(
            'title', M.movie_title,
            'overview', M.movie_overview,
            'img_url', M.movie_img_url,
            'rating', M.movie_rating,
            'popular', M.movie_popular,
            'release_date', M.movie_release_date,
            'genres', JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', G.genre_id,
                    'title', G.genre_title
                )
            ),
            'yt_video_ids', (SELECT JSON_ARRAYAGG(YT.yt_video_id)
                             FROM YouTubeVideo YT
                             WHERE YT.movie_id = M.movie_id)
        ) AS details
    FROM
        Movie AS M
    LEFT JOIN
        Movie_has_Genre AS MG 
        ON M.movie_id = MG.movie_id
    LEFT JOIN
        Genre AS G 
        ON G.genre_id = MG.genre_id
    GROUP BY
        M.movie_id,
        M.movie_title,
        M.movie_overview,
        M.movie_img_url,
        M.movie_rating,
        M.movie_popular,
        M.movie_release_date;
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    movies = []
    for row in result_set:
        movie_data = {
            "id": row[0],
            "details": json.loads(row[1])
        }
        movies.append(movie_data)

    commit_and_close(conn)
    return jsonify({"results": movies})


@app.route("/crews", methods=["GET"])
def get_crews_endpoint():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    query_combined = """
    SELECT
        M.movie_id,
        JSON_OBJECT(
            'directors', JSON_OBJECT(
                    'id', D.director_id,
                    'fname', D.director_fname,
                    'lname', D.director_lname,
                    'mname', D.director_mname,
                    'img_url', D.director_img_url,
                    'popular', D.director_popular
            ),
            'writers', JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', W.writer_id,
                    'fname', W.writer_fname,
                    'lname', W.writer_lname,
                    'mname', W.writer_mname,
                    'img_url', W.writer_img_url,
                    'popular', W.writer_popular
                )
            )
        ) AS crews
    FROM
        Movie AS M
    LEFT JOIN
        Director AS D 
        ON M.director_id = D.director_id
    LEFT JOIN 
        Movie_has_Writer AS MW 
        ON M.movie_id = MW.movie_id
    LEFT JOIN
        Writer AS W 
        ON W.writer_id = MW.writer_id
    GROUP BY
        M.movie_id
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    crews = [] 
    for row in result_set:
        movie_data = {
            "id": row[0],
            "crews": json.loads(row[1])
        }
        
        crews.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": crews})

@app.route("/actors", methods=["GET"])
def get_actors_endpoint():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    query_combined = """
    SELECT
        M.movie_id,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'fname', A.actor_fname,
                'lname', A.actor_lname,
                'mname', A.actor_mname,
                'img_url', A.actor_img_url,
                'popular', A.actor_popular
            )
        ) AS actors
    FROM
        Actor AS A
    LEFT JOIN 
        Movie_has_Actor AS MA 
        ON A.actor_id = MA.actor_id
    LEFT JOIN
        Movie AS M
        ON M.movie_id = MA.movie_id
    GROUP BY
        M.movie_id;
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    actors = [] 
    for row in result_set:
        movie_data = {
            "id": row[0],
            "actors": [] 
        }

        actors_json = json.loads(row[1])

        for actor_data in actors_json:
            actor = {
                "fname": actor_data["fname"],
                "lname": actor_data["lname"],
                "mname": actor_data["mname"],
                "img_url": actor_data["img_url"],
                "popular": actor_data["popular"]
            }
            movie_data["actors"].append(actor)

        actors.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": actors}) 

@app.route("/update-database", methods=["GET"])
def update_database_endpoint():
    start_p = request.args.get('start_p', default=None, type=int)
    stop_p = request.args.get('stop_p', default=None, type=int)

    if start_p is None or stop_p is None:
        return jsonify({"error": "Both start_p and stop_p parameters are required."})

    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    movies_data = get_movies_data(start_p, stop_p)

    if movies_data:
        processed_movies = [process_movie(cursor, conn, movie) for movie in movies_data]
        return jsonify(processed_movies)

    print("No Results Found!")
    return jsonify([])

@app.route("/", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Movie Recommemdation Back-end!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)