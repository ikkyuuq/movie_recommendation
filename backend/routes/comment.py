from flask import Blueprint, jsonify, request
from app.database.db import get_database_connection, execute_query_and_commit, commit_and_close

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comment', methods=["GET", "POST"])
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