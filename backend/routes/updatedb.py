from flask import Blueprint, jsonify, request
from app.database.db import get_database_connection
from app.api.models_movie_api import process_movie, get_movies_data

updatedb_bp = Blueprint('updatedb', __name__)

@updatedb_bp.route("/updb", methods=["GET"])
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