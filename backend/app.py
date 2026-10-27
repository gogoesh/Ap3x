# CourseScope entry
from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def home():
        return jsonify({"name": "CourseScope API", "status": "running"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
