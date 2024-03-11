from perfect_recipe.ext.database import db
from flask_login import UserMixin

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    ingredients = db.relationship('Ingredient')  
    instructions = db.relationship('Instruction')    
    preparation_time = db.Column(db.String)
    portion = db.Column(db.String)
    # category = db.Column(db.String)
    # dificultity = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    recipes = db.relationship('Recipe')