import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Plant  # <- no dot, relative imports cause test import failures

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
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({"message": "API running successfully."}), 200

    @app.route("/plants", methods=["GET"])
    def get_plants():
        plants = Plant.query.all()
        return jsonify([p.to_dict() for p in plants]), 200

    @app.route("/plants/<int:id>", methods=["GET"])
    def get_plant(id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        return jsonify(plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["PATCH"])
    def update_plant(id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return jsonify({"error": "Plant not found"}), 404

        data = request.get_json() or {}
        for attr, value in data.items():
            if hasattr(plant, attr):
                setattr(plant, attr, value)

        db.session.commit()

        updated_plant = Plant.query.filter_by(id=id).first()
        return jsonify(updated_plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["DELETE"])
    def delete_plant(id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        db.session.delete(plant)
        db.session.commit()
        return "", 204

    return app


app = create_app()
