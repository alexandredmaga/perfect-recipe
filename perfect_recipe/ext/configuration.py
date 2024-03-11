def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['WTF_CSRF_ENABLED'] = False