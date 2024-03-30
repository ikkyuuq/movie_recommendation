from flask import Flask, jsonify
from flask_cors import CORS
from app.routes.favour import favour_bp
from app.routes.like import like_bp
from app.routes.comment import comment_bp
from app.routes.updatedb import updatedb_bp
from app.routes.movie import movie_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(movie_bp)
app.register_blueprint(favour_bp)
app.register_blueprint(like_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(updatedb_bp)

@app.route("/", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Movie Recommemdation Back-end!"})

if __name__ == "__main__":
    app.run(debug=True)