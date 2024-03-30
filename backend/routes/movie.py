import json
from flask import Blueprint, jsonify, request
from app.database.db import get_database_connection, commit_and_close

movie_bp = Blueprint('movie', __name__)

@movie_bp.route("/movie", methods=["GET"])
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