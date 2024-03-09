from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_database_connection, commit_and_close
from models import process_movie, get_movies_data , get_kinocheck_data
import json

app = Flask(__name__)
CORS(app)

@app.route("/crews", methods=["GET"])
def get_crews_endpoint():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    sqlquery = """
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
    cursor.execute(sqlquery)
    result_set = cursor.fetchall()

    data = []
    for row in result_set:
        movie_data = {
            "movie_id": row[0],
            "crews": json.loads(row[1])
        }
        
        data.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": data})

@app.route("/actors", methods=["GET"])
def get_actors_endpoint():
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
    
    sqlquery = """
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
    cursor.execute(sqlquery)
    result_set = cursor.fetchall()

    data = [] 
    for row in result_set:
        movie_data = {
            "movie_id": row[0],
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

        data.append(movie_data) 

    commit_and_close(conn)
    return jsonify({"results": data}) 

@app.route("/movie", methods=["GET"])
def get_movie_by_id():
    tmdb_id = request.args.get('tmdb_id', default=None, type=int)
    
    conn = get_database_connection()
    cursor = conn.cursor(buffered=True)
   
    if tmdb_id is None:
        sqlquery = """
        SELECT
            M.movie_id,
            M.movie_title,
            M.movie_img_url,
            M.movie_rating,
            M.movie_popular,
            M.movie_release_date,
            (SELECT 
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'id', G.genre_id,
                        'title', G.genre_title
                    )
                )
            FROM Movie_has_Genre AS MG
            LEFT JOIN Genre AS G ON G.genre_id = MG.genre_id
            WHERE MG.movie_id = M.movie_id) AS genres
        FROM
            Movie AS M
        GROUP BY
            M.movie_id,
            M.movie_title,
            M.movie_img_url,
            M.movie_rating,
            M.movie_release_date;
        """
        cursor.execute(sqlquery)
        result_set = cursor.fetchall()

        data = []
        for row in result_set:
            movie_data = {
                "id": row[0],
                "title": row[1],
                "img_url": row[2],
                "rating": row[3] if row[3] is not None else 0,
                "popular": row[4] if row[4] is not None else 0,
                "release_date": row[5],
                "genres": json.loads(row[6]) if row[6] is not None else None,
            }
            data.append(movie_data)

        commit_and_close(conn)
        return jsonify({"results": data})
    
    sqlquery = """
    SELECT 
        M.movie_id,    
        M.movie_title,
        M.movie_overview,
        M.movie_img_url,
        M.movie_rating,
        M.movie_popular,
        M.movie_release_date,
        (SELECT 
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', G.genre_id,
                    'title', G.genre_title
                )
            )
        FROM Movie_has_Genre AS MG
        LEFT JOIN Genre AS G ON G.genre_id = MG.genre_id
        WHERE MG.movie_id = M.movie_id) AS genres,
        (SELECT 
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', T.trailer_id
                )
            )
        FROM Trailer AS T
        WHERE T.movie_id = M.movie_id) AS trailerd,
        (SELECT
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', D.director_id,
                    'fname', D.director_fname,
                    'lname', D.director_lname,
                    'mname', D.director_mname,
                    'img_url', D.director_img_url,
                    'popular', D.director_popular
                )
            )
        FROM Director AS D
        WHERE D.director_id = M.director_id) AS directors,
        (SELECT 
            JSON_ARRAYAGG(
                JSON_OBJECT( 
                    'id', A.actor_id,
                    'fname', A.actor_fname,
                    'lname', A.actor_lname,
                    'mname', A.actor_mname,
                    'img_url', A.actor_img_url,
                    'popular', A.actor_popular
                )
            )
        FROM Movie_has_Actor AS MA
        LEFT JOIN Actor AS A ON A.actor_id = MA.actor_id
        WHERE MA.movie_id = M.movie_id) AS actors,
        (SELECT
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', W.writer_id,
                    'fname', W.writer_fname,
                    'lname', W.writer_lname,
                    'mname', W.writer_mname,
                    'img_url', W.writer_img_url,
                    'popular', W.writer_popular
                )
            )
        FROM Movie_has_Writer AS MW
        LEFT JOIN Writer AS W ON W.writer_id = MW.writer_id
        WHERE MW.movie_id = M.movie_id) AS writers
    FROM Movie AS M
    WHERE M.movie_id = %s
    GROUP BY
        M.movie_id,
        M.movie_title,
        M.movie_overview,
        M.movie_img_url,
        M.movie_rating,
        M.movie_popular,
        M.movie_release_date;
    """
    
    cursor.execute(sqlquery, (tmdb_id,))
    result_set = cursor.fetchall()
    
    data = []
    for row in result_set:
        movie_data = {
            "id": row[0],
            "title": row[1],
            "overview": row[2],
            "img_url": row[3],
            "rating": row[4] if row[4] is not None else 0,
            "popular": row[5] if row[5] is not None else 0,
            "release_date": row[6],
            "genres": json.loads(row[7]) if row[7] is not None else None,
            "trailer": json.loads(row[8]) if row[8] is not None else None,
            "directors": json.loads(row[9]),
            "actors": json.loads(row[10]),
            "writers": json.loads(row[11])
        }
        data.append(movie_data)

    commit_and_close(conn)
    return jsonify({"results": data})


@app.route("/updb", methods=["GET"])
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