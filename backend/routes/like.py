from flask import Blueprint, jsonify, request
from app.database.db import get_database_connection, execute_query_and_commit, commit_and_close

like_bp = Blueprint('like', __name__)

@like_bp.route('/like', methods=["GET", "PUT"])
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