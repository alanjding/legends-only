#!/usr/bin/env python

# ------------------------------------------------------------------------------
# helper.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from database import db, Message

def add_message(time, sender, message):
    message = Message(time=time, sender=sender, message=message)

    db.session.add(message)
    db.session.commit()

def _message_time(message):
    return message.time

# Returns a list of dictionaries sorted by time
def get_message_log():
    all_messages = db.session.query(Message).all()
    sorted(all_messages, key=_message_time)
    return list(map(lambda message: {'time': message.time,
                                'sender': message.sender,
                                'message': message.message},
               all_messages))
