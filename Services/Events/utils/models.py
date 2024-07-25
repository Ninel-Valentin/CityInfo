from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enabled = db.Column(db.Boolean)
    category = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    date = db.Column(db.Date)
    city = db.Column(db.String(128))
    price = db.Column(db.Float)
    location = db.Column(db.String(128))
    
    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if not '_state' in k:
                d[k] = self.__dict__[k]
        return d