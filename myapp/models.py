# encoding: utf-8
from myapp import db
from sqlalchemy.schema import Sequence as Sequence
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

ROLE_USER = 0
ROLE_ADMIN = 1  # use?

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.BigInteger(
                                 64), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger(64), Sequence('id_seq'), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    uid = db.Column(db.BigInteger(64), unique=True)
    info = db.Column(db.Text())
    update_time = db.Column(db.DateTime())
    create_time = db.Column(db.DateTime())
    token = db.Column(db.Text())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, uid, info, token):
        self.uid = uid
        self.info = info
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.uid
