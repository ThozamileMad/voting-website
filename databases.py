from flask_sqlalchemy import SQLAlchemy


def sqlalchemy_app(app):
    return SQLAlchemy(app)


def web_databases(app, usermixin, db):
    with app.app_context():
        class Registration(db.Model):
            __bind_key__ = "registrations"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String,  nullable=False, unique=False)
            surname = db.Column(db.String, nullable=False, unique=False)
            id_number = db.Column(db.String, nullable=False, unique=True)
            date_of_birth = db.Column(db.String, nullable=False, unique=False)
            address = db.Column(db.String, nullable=False, unique=False)
            contact_numbers = db.Column(db.String, nullable=False, unique=True)
            proof_of_address = db.Column(db.String, nullable=False, unique=False)
            citizenship = db.Column(db.String, nullable=False, unique=False)
            province = db.Column(db.String, nullable=False, unique=False)
            language = db.Column(db.String, nullable=False, unique=False)
            political_party_affiliation = db.Column(db.String, nullable=False, unique=False)
            disabled = db.Column(db.String, nullable=False, unique=False)
            gender = db.Column(db.String, nullable=True, unique=False)
            married = db.Column(db.String, nullable=True, unique=False)

        class User(usermixin, db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String,  nullable=False, unique=False)
            surname = db.Column(db.String, nullable=False, unique=False)
            email = db.Column(db.String, nullable=False, unique=True)
            password = db.Column(db.String, nullable=False, unique=True)
            id_number = db.Column(db.String, nullable=False, unique=True)
            tsandcs = db.Column(db.String, nullable=False, unique=False)

        db.create_all()

        return [Registration, User]