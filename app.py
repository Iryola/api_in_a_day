from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Integer, nullable=False)
    special_skill = db.Column(db.String(140), nullable=False)
    def __init__(self, first_name, last_name, birthday, special_skill):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.special_skill = special_skill

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "birthday", "special_skill")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/add-user", methods=["POST"])
def add_user():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    birthday = request.json["birthday"]
    special_skill = request.json["special_skill"]

    record = User(first_name, last_name, birthday, special_skill)
    db.session.add(record)
    db.session.commit()
    user = User.query.get(record.id)

    return user_schema.jsonify(user)

@app.route("/all-users", methods=["GET"])
def all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users).data

    return jsonify(result)

if __name__ == "__main__":
    app.debug = True
    app.run()