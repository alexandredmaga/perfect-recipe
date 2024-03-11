from flask import Flask
from perfect_recipe.ext import configuration
from perfect_recipe.ext import database
from perfect_recipe.ext import commands
from perfect_recipe import views
from perfect_recipe.ext import auth
from perfect_recipe import models

app = Flask(__name__)
configuration.init_app(app)
database.init_app(app)
commands.init_app(app)
auth.init_app(app)
views.init_app(app)
    
if __name__ == '__main__':
    app.run(debug=True)