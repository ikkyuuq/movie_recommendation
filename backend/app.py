from flask import Flask, jsonify, request
from db import get_database_connection, commit_and_close
from models import process_movie, get_movies_data
import json

app = Flask(__name__)

@app.route("/getmovies", methods=["GET"])
def get_movies():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    query_combined = """
    SELECT
    Movie.movie_id,
    JSON_OBJECT(
        'movie_title', Movie.movie_title,
        'movie_overview', Movie.movie_overview,
        'movie_img_url', Movie.movie_img_url,
        'movie_rating', Movie.movie_rating,
        'movie_popular', Movie.movie_popular,
        'movie_release_date', Movie.movie_release_date,
        'genres', JSON_ARRAYAGG(
            JSON_OBJECT(
                'genre_id', Genre.genre_id,
                'genre_title', Genre.genre_title
            )
        )
    ) AS movie_detail
    FROM
        Movie
    LEFT JOIN
        Movie_has_Genre ON Movie.movie_id = Movie_has_Genre.movie_id
    LEFT JOIN
        Genre ON Movie_has_Genre.genre_id = Genre.genre_id
    GROUP BY
        Movie.movie_id,
        Movie.movie_title,
        Movie.movie_overview,
        Movie.movie_img_url,
        Movie.movie_rating,
        Movie.movie_popular,
        Movie.movie_release_date;
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    movies = []
    for row in result_set:
        movie_data = {
            "movie_id": row[0],
            "movie_detail": json.loads(row[1])
        }
        movies.append(movie_data)

    commit_and_close(conn)
    return jsonify({"results": movies})

@app.route("/getcrews", methods=["GET"])
def get_crews():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    query_combined = """
    SELECT
        Movie.movie_id,
        JSON_OBJECT(
            'directors', JSON_OBJECT(
                    'director_id', Director.director_id,
                    'director_fname', Director.director_fname,
                    'director_lname', Director.director_lname,
                    'director_mname', Director.director_mname,
                    'director_img_url', Director.director_img_url,
                    'director_popular', Director.director_popular
            ),
            'writers', JSON_ARRAYAGG(
                JSON_OBJECT(
                    'writer_id', Writer.writer_id,
                    'writer_fname', Writer.writer_fname,
                    'writer_lname', Writer.writer_lname,
                    'writer_mname', Writer.writer_mname,
                    'writer_img_url', Writer.writer_img_url,
                    'writer_popular', Writer.writer_popular
                )
            )
        ) AS crews
    FROM
        Movie
    LEFT JOIN
        Director ON Movie.director_id = Director.director_id
    LEFT JOIN 
        Movie_has_Writer ON Movie.movie_id = Movie_has_Writer.movie_id
    LEFT JOIN
        Writer ON Writer.writer_id = Movie_has_Writer.writer_id
    GROUP BY
        Movie.movie_id
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    crews = [] 
    for row in result_set:
        movie_data = {
            "movie_id": row[0],
            "crews": json.loads(row[1])
        }
        
        crews.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": crews})



@app.route("/getactors", methods=["GET"])
def get_actors():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    query_combined = """
    SELECT
        Movie.movie_id,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'actor_fname', Actor.actor_fname,
                'actor_lname', Actor.actor_lname,
                'actor_mname', Actor.actor_mname,
                'actor_img_url', Actor.actor_img_url,
                'actor_popular', Actor.actor_popular
            )
        ) AS actors
    FROM
        Actor
    LEFT JOIN Movie_has_Actor ON Movie_has_Actor.actor_id = Actor.actor_id
    LEFT JOIN Movie ON Movie.movie_id = Movie_has_Actor.movie_id
    GROUP BY
        Movie.movie_id;
    """
    cursor.execute(query_combined)
    result_set = cursor.fetchall()

    actors = [] 
    for row in result_set:
        movie_data = {
            "movie_id": row[0],
            "actors": [] 
        }

        actors_json = json.loads(row[1])

        for actor_data in actors_json:
            actor = {
                "actor_fname": actor_data["actor_fname"],
                "actor_lname": actor_data["actor_lname"],
                "actor_mname": actor_data["actor_mname"],
                "actor_img_url": actor_data["actor_img_url"],
                "actor_popular": actor_data["actor_popular"]
            }
            movie_data["actors"].append(actor)

        actors.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": actors}) 

@app.route("/fetchapitodb")
def update_db():
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

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Flask"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
