import datetime
from flask import render_template, request, redirect, url_for, g
from typing import Optional
from app.models.user_model import UserModel
from app.models.message_model import MessageModel
from app import db
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import aliased
import os


def home():
    print(f"Running app...{os.getenv("DEBUG")}")
    users = UserModel.query.all()
    return render_template("home.html", users=users)


def post_message():
    data = request.form
    message = data['message']
    sender_id = g.user.id
    recipient_id = data['recipient_id']
    sent_at = datetime.datetime.now(datetime.timezone.utc)
    new_message = MessageModel(message=message, sender_id=sender_id, recipient_id=recipient_id, sent_at=sent_at)
    db.session.add(new_message)
    db.session.commit()
    return redirect(request.referrer)


def private_message(recipient_name: str):
    user_recipient: Optional[UserModel] = UserModel.query.where(UserModel.username == recipient_name).first()

    sender = aliased(UserModel)
    recipient = aliased(UserModel)
    messages = db.session.query(MessageModel, sender, recipient) \
        .join(sender, MessageModel.sender_id == sender.id) \
        .join(recipient, MessageModel.recipient_id == recipient.id) \
        .where(
        or_(
            and_(MessageModel.sender_id == g.user.id, MessageModel.recipient_id == user_recipient.id),
            and_(MessageModel.recipient_id == g.user.id, MessageModel.sender_id == user_recipient.id)
        )) \
        .order_by(MessageModel.sent_at.asc()) \
        .all()
    return render_template("private_message.html",
                           user_recipient=user_recipient,
                           messages=messages)