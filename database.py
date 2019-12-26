#!/usr/bin/env python

# ------------------------------------------------------------------------------
# database.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    time = db.Column(db.Integer)
    sender = db.Column(db.String)
    message = db.Column(db.String)

    def __repr__(self):
        return self.message
