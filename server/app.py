#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Raccoon, Trashcan, Visit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!

@app.get('/raccoons')
def get_raccoons():
    raccoons=Raccoon.query.all()
    return make_response(jsonify([r.to_dict(rules=('-visits',)) for r in raccoons]), 200)

@app.get('/raccoons/<int:id>')
def get_raccoons_by_id(id):
    raccoon= db.session.get(Raccoon, id)
    if raccoon:
        return make_response(jsonify(raccoon.to_dict(rules=('-visits.trashcan',))),200)
    return make_response(jsonify({"error": f"There is no racoon with this {id}"}),404)

@app.delete('/raccoons/<int:id>')
def delete_raccoon(id):
    raccoon= db.session.get(Raccoon, id)
    if not raccoon:
        return make_response(jsonify({"error": f"There is no racoon with this {id}"}),404)
    db.session.delete(raccoon)
    db.session.commit()
    return make_response(jsonify({}), 200)


@app.get('/trashcans')
def get_trashcans():
    trashcans=Trashcan.query.all()
    return make_response(jsonify([t.to_dict(rules=('-visits',)) for t in trashcans]), 200)

@app.get('/trashcans/<int:id>')
def get_trashcans_by_id(id):
    trashcan= db.session.get(Trashcan, id)
    if trashcan:
        return make_response(jsonify(trashcan.to_dict(rules=('-visits',))),200)
    return make_response(jsonify({"error": f"There is no trashcan with this {id}"}),404)


@app.post('/visits')
def post_visits():
    data = request.get_json()
    if not(db.session.get(Raccoon, data['raccoon_id']) or db.session.get(Trashcan, data['trashcan_id'])):
        return make_response(jsonify({"error": f"There is no trashcan or racoon with those ides"}),404)
    try:
        new_visit=Visit(date=data['date'],raccoon_id=data['raccoon_id'], trashcan_id=data['trashcan_id'])
        db.session.add(new_visit)
        db.session.commit()
        return make_response(jsonify(new_visit.to_dict()),200)
    except Exception as e:
        return make_response(jsonify({"error": f"There is an error: {e}"}),404)
    
@app.delete('/visits/<int:id>')
def delete_visit(id):
    visit = db.session.get(Visit, id)
    if visit:
        db.session.delete(visit)
        db.session.commit()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": f"There is no visit with this {id}"}),404)




if __name__ == '__main__':
    app.run(port=5555, debug=True)