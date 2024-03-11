from perfect_recipe.ext.database import db

def init_app(app):
    @app.cli.command()
    def createdb():
        db.create_all()
