from myapp import db
from sqlalchemy.schema import Sequence as Sequence

class User(db.Model):
    id = db.Column(db.BigInteger(64), Sequence('id_seq'), primary_key=True)
    uid = db.Column(db.BigInteger(64), unique=True)
    info = db.Column(db.Text())
    update_time = db.Column(db.DateTime())
    create_time = db.Column(db.DateTime())

    def __init__(self, uid,info):
        self.uid = uid
        self.info = info

    def __repr__(self):
        return '<User %r>' % self.uid