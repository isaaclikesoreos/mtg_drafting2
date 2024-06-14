from application import db
from run import app

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database initialized!")
