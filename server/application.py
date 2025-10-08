import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Plant


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI", "sqlite:///plants.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}})

    @app.route("/")
    def index():
        return jsonify({"message": "API running successfully."}), 200

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": str(e)}), 404

    @app.route("/plants", methods=["GET"])
    def get_plants():
        plants = Plant.query.all()
        return jsonify([p.to_dict() for p in plants]), 200

    @app.route("/plants/<int:id>", methods=["GET"])
    def get_plant(id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        return jsonify(plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["PATCH"])
    def update_plant(id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        data = request.get_json() or {}

        allowed_fields = {"is_in_stock", "price", "name", "image"}
        for attr, value in data.items():
            if attr in allowed_fields:
                setattr(plant, attr, value)

        db.session.commit()
        return jsonify(plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["DELETE"])
    def delete_plant(id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        db.session.delete(plant)
        db.session.commit()
        return "", 204

    return app


app = create_app()
