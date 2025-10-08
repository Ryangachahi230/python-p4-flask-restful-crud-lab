import json
import pytest
from server.application import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        '''Run before each test'''
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Seed the database with initial test data
            plant_1 = Plant(name="Aloe", image="./images/aloe.jpg", price=11.50)
            plant_2 = Plant(name="ZZ Plant", image="./images/zz-plant.jpg", price=25.98, is_in_stock=False)
            db.session.add_all([plant_1, plant_2])
            db.session.commit()

        yield  # Run the test here

        # Clean up after test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["name"] == "Aloe"

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = app.test_client().patch(
            '/plants/1',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["is_in_stock"] is False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''deletes a plant successfully'''
        with app.app_context():
            lo = Plant(
                name="Live Oak",
                image="https://example.com/live-oak.jpg",
                price=250.00,
                is_in_stock=False,
            )
            db.session.add(lo)
            db.session.commit()
            plant_id = lo.id

        response = app.test_client().delete(f'/plants/{plant_id}')
        assert response.status_code in [200, 204]

        # Verify deletion
        with app.app_context():
            deleted = Plant.query.get(plant_id)
            assert deleted is None
