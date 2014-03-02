# encoding: utf-8
from myapp import db
from sqlalchemy.schema import Sequence as Sequence
from flask.ext.security import UserMixin, RoleMixin


ROLE_USER = 0
ROLE_ADMIN = 1  # use?

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.BigInteger(64), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger(64), Sequence('id_seq'), primary_key = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    uid = db.Column(db.BigInteger(64), unique = True)
    info = db.Column(db.Text())
    create_time = db.Column(db.DateTime())
    last_login_time = db.Column(db.DateTime())
    update_time = db.Column(db.DateTime())

    token = db.Column(db.Text())
    roles = db.relationship('Role', secondary = roles_users,
                            backref = db.backref('users', lazy = 'dynamic'))

    def __init__(self, uid, info, token):
        self.uid = uid
        self.info = info
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.uid

class WeiboList(db.Model):
    __tablename__ = 'weibo_list'
    id = db.Column(db.BigInteger(64), Sequence('id_seq'), primary_key = True)
    uid = db.Column(db.BigInteger(64), unique = True)

    user_uid = db.Column(db.BigInteger(64))
    create_time = db.Column(db.DateTime())
    update_time = db.Column(db.DateTime())
    status_type = db.Column(db.Integer())

    status_id = db.Column(db.BigInteger(64), unique = True)
    created_at = db.Column(db.DateTime())
    source = db.Column(db.Text())

    original_pic = db.Column(db.Text())
    bmiddle_pic = db.Column(db.Text())
    thumbnail_pic = db.Column(db.Text())

    geo = db.Column(db.Text())

    retweeted_status = db.Column(db.Text())

    reposts_count = db.Column(db.Integer())
    comments_count = db.Column(db.Integer())
    attitudes_count = db.Column(db.Integer())
    visible_type = db.Column(db.Integer())

    pic_urls = db.Column(db.Text())

    def __init__(self):
        pass

    def __repr__(self):
        return '<WeiboList %r>' % self.uid
