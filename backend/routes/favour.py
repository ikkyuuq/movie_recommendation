from flask import Blueprint, jsonify, request
from app.database.db import get_database_connection, execute_query_and_commit, commit_and_close

favour_bp = Blueprint('favour', __name__)

@favour_bp.route('/favour', methods=["GET", "POST", "DELETE"])
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
