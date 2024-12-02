import pytest
from app import app, db, Habit
from datetime import datetime

# Configuration du test
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utilisation d'une base en mémoire pour les tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crée la base de données
        yield client
        with app.app_context():
            db.drop_all()  # Nettoie la base après les tests

def test_create_habit(client):
    response = client.post('/habits', json={'name': 'Boire de l\'eau', 'frequency': 'daily'})
    assert response.status_code == 201  # Vérifie que la réponse est 201 Created
    assert response.json['message'] == 'Habit created!'

def test_get_habits(client):
    client.post('/habits', json={'name': 'Boire de l\'eau', 'frequency': 'daily'})
    response = client.get('/habits')
    assert response.status_code == 200  # Vérifie que la réponse est 200 OK
    assert len(response.json) == 1  # Vérifie qu'il y a une habitude dans la liste

def test_complete_habit(client):
    client.post('/habits', json={'name': 'Boire de l\'eau', 'frequency': 'daily'})
    response = client.post('/habits/1/complete')
    assert response.status_code == 200  # Vérifie que la réponse est 200 OK
    assert response.json['message'] == 'Habit marked as completed!'

def test_streak_increment(client):
    client.post('/habits', json={'name': 'Boire de l\'eau', 'frequency': 'daily'})
    client.post('/habits/1/complete')  # Marquer comme complété une fois
    habit = Habit.query.get(1)
    assert habit.streak == 1  # Vérifie que le streak a été incrémenté à 1
