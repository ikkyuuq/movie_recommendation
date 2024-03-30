# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_database_connection, commit_and_close, execute_query_and_commit
from models_movie_api import process_movie, get_movies_data
import json

app = Flask(__name__)
CORS(app)

@app.route("/updb", methods=["GET"])
def updatedb():
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

@app.route("/movie", methods=["GET"])
def movie():
    tmdb_id = request.args.get('tmdb_id', default=None, type=int)
    
    conn = get_database_connection()
    cursor = conn.cursor()
   
    if tmdb_id is None:
        sqlquery = """
        SELECT
            M.movie_id,
            M.movie_title,
            M.movie_img_url,
            M.movie_rating,
            M.movie_popular,
            M.movie_release,
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
            M.movie_release;
        """
        cursor.execute(sqlquery)
        results = cursor.fetchall()

        movie_data = [{
                "id": row[0],
                "title": row[1],
                "img_url": row[2],
                "rating": row[3] if row[3] is not None else 0,
                "popular": row[4] if row[4] is not None else 0,
                "release_date": row[5],
                "genres": json.loads(row[6]) if row[6] is not None else None,
            } for row in results]

        commit_and_close(conn)
        return jsonify({"results": movie_data})
    
    sqlquery = """
    SELECT 
        M.movie_id,    
        M.movie_title,
        M.movie_overview,
        M.movie_img_url,
        M.movie_rating,
        M.movie_popular,
        M.movie_release,
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
        M.movie_release;
    """
    
    cursor.execute(sqlquery, (tmdb_id,))
    results = cursor.fetchall()
    
    movie_data = [{
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
        } for row in results]

    commit_and_close(conn)
    return jsonify({"results": movie_data})


@app.route('/like', methods=["GET", "PUT"])
def like():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("START TRANSACTION")
    
    try:
        if request.method == "GET":
            movie_id = request.args.get('movie_id', default=None, type=str)
            user_id = request.args.get('user_id', default=None, type=str)
            
            query = """
                    SELECT DISTINCT(CL.comment_id)
                    FROM Movie_has_Comment AS MC
                    LEFT JOIN Comment_has_Like AS CL
                    ON CL.user_id = %s
                    WHERE MC.movie_id = %s"""
                    
            cursor.execute(query, (user_id, movie_id))
            results = cursor.fetchall()
            likes_list = [{'comment_id': row[0]} for row in results]
        
            return jsonify({'likes': likes_list}), 200
        
        elif request.method == "PUT":
            data = request.json
            comment_id = data.get('comment_id')
            action = data.get('action')
            user_id = data.get('user_id')
            
            if action not in ('like', 'unlike'):
                return jsonify({"error": "Invalid action. Use 'like' or 'unlike'."}), 400
            
            if action == 'like':
                query = "INSERT INTO Comment_has_Like (comment_id, user_id) VALUES (%s, %s)"
                execute_query_and_commit(conn, cursor, query, (comment_id, user_id))
            elif action == 'unlike':
                query = "DELETE FROM Comment_has_Like WHERE comment_id = %s AND user_id = %s"
                execute_query_and_commit(conn, cursor, query, (comment_id, user_id))
            
            return jsonify({"message": "Like updated successfully"}), 200
    
    except Exception as e:
        cursor.execute("ROLLBACK")
        return jsonify({"error": f"An error occurred while updating like: {e}"}), 400

@app.route('/favour', methods=["GET", "POST", "DELETE"])
def favour():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("START TRANSACTION")
    
    try:
        if request.method == "GET":
            user_id = request.args.get('user_id', default=None, type=str)
            if not user_id:
                return jsonify({"error": "User ID is required for getting favourites"}), 400
            
            query = "SELECT favour_id, movie_id, movie_title, movie_release_date, user_id FROM Favour WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            favour_list = [{'favour_id': row[0], 'movie_id': row[1], 'movie_title': row[2], 'movie_release_date': row[3], 'user_id': row[4]} for row in results]
            commit_and_close(conn)
            return jsonify({'favour': favour_list}), 200
        
        elif request.method == "POST":
            data = request.json
            user_id = data.get('user_id')
            movie_id = data.get('movie_id')
            movie_title = data.get('movie_title')
            movie_release_date = data.get('movie_release_date')
            
            if not (user_id and movie_id):
                return jsonify({"error": "User ID and movie ID are required for adding to favourites"}), 400
            
            cursor.execute("SELECT * FROM Favour WHERE movie_id = %s AND user_id = %s", (movie_id, user_id))
            if cursor.fetchone():
                return jsonify({"error": "This movie is already in your favourites list"}), 400
            
            query = "INSERT INTO Favour (user_id, movie_id, movie_title, movie_release_date) VALUES (%s, %s, %s, %s)"
            execute_query_and_commit(conn, cursor, query, (user_id, movie_id, movie_title, movie_release_date))
            return jsonify({'message': f'Added {movie_id} into favourite!'}), 200

        
        elif request.method == "DELETE":
            favour_id = request.args.get('favour_id')
            if favour_id:
                query = "DELETE FROM Favour WHERE favour_id = %s"
                execute_query_and_commit(conn, cursor, query, (favour_id,))
                return jsonify({'message': f'Deleted {favour_id} from favourite!'}), 200
            else:
                user_id = request.json.get('user_id')
                movie_id = request.json.get('movie_id')
                
                if not user_id or not movie_id:
                    return jsonify({"error": "User ID and Movie ID are required for deleting from favourites"}), 400
                
                query = "SELECT * FROM Favour WHERE user_id = %s AND movie_id = %s"
                cursor.execute(query, (user_id, movie_id))
                if not cursor.fetchone():
                    return jsonify({"error": f"No favour found on User ID: {user_id} with Movie ID: {movie_id}"}), 404
                
                query = "DELETE FROM Favour WHERE user_id = %s AND movie_id = %s"
                execute_query_and_commit(conn, cursor, query, (user_id, movie_id))
                return jsonify({'message': f'Deleted {movie_id} from favourite!'}), 200
            
    except Exception as e:
        cursor.execute("ROLLBACK")
        return jsonify({"error": f"An error occurred while processing the request: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
           
@app.route('/comment', methods=["GET", "POST"])
def comment():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("START TRANSACTION")
    
    try:
        if request.method == "GET":
            movie_id = request.args.get('movie_id', default=None, type=str)
            if movie_id is None:
                return jsonify({"error": "Movie ID is required for fetching comments"}), 400
            
            cursor.execute("""
                            SELECT C.comment_id, C.comment_content, C.comment_timestamp, C.user_id, C.display_name, C.user_img_url, COUNT(CL.user_id) AS like_count
                            FROM Movie_has_Comment AS MC
                            LEFT JOIN Comment AS C ON MC.comment_id = C.comment_id
                            LEFT JOIN Comment_has_Like AS CL ON MC.comment_id = CL.comment_id
                            WHERE MC.movie_id = %s
                            GROUP BY C.comment_id
                            """, (movie_id,))
            results = cursor.fetchall()
            comments = [{
                "comment_id": row[0],
                "content": row[1],
                "timestamp": row[2],
                "user_id": row[3],
                "displayName": row[4],
                "img_url": row[5],
                "like_count": row[6]
            } for row in results]
           
            return jsonify({"comments": comments}), 200
        
        elif request.method == "POST":
            movie_id = request.args.get('movie_id', default=None, type=int)
            data = request.json
            content = data.get('content')
            user_id = data.get('user_id')
            name = data.get('name')
            img_url = data.get('img_url')
            
            if not all((movie_id, content, user_id, name, img_url)):
                return jsonify({"error": "Movie ID, Content, User ID, Name, and Image URL are required for creating a comment"}), 400
            
            cursor.execute('INSERT INTO Comment (comment_content, user_id, display_name, user_img_url) VALUES (%s, %s, %s, %s)', (content, user_id, name, img_url))
            latest_comment_id = cursor.lastrowid
            cursor.execute('INSERT INTO Movie_has_Comment (movie_id, comment_id) VALUES (%s, %s)', (movie_id, latest_comment_id))
            commit_and_close(conn)
            return jsonify({"message": "Create Comment Success"}), 201
    
    except Exception as e:
        conn.rollback()
        print(f"Error during database operation: {e}")
        return jsonify({"error": f"An error occurred while fetching or creating the comment: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/")
def say_hello():
    return jsonify({"msg": "Hello from Movie Recommendation Back-end!"})

if __name__ == "__main__":
    app.run()
