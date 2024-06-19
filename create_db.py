from application import db
from run import app


with app.app_context():
    db.create_all()
    print("Database initialized!")
