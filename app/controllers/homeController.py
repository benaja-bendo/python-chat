import datetime
from flask import render_template, request, redirect, url_for, g
from typing import Optional
from app.models.user_model import UserModel
from app.models.message_model import MessageModel
from app.models.notification_model import NotificationModel
from app.controllers.notificationController import send_notification
from app import db
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import aliased
import os
import requests
import folium
from datetime import datetime

current_time = datetime.now()


def home():
    print(f"Running app...{os.getenv("DEBUG")}")
    users = UserModel.query.all()
    return render_template("home.html", users=users)


def post_message():
    data = request.form
    message = data['message']
    sender_id = g.user.id
    recipient_id = data['recipient_id']
    sent_at = datetime.datetime.utcnow()

    # Create a notification model with appropriate attributes
    notification = NotificationModel(type='message', subject='New Message', body=message, sender_id=sender_id, recipient_id=recipient_id, date=sent_at, status='unread')

    # Add the notification to the database session
    db.session.add(notification)

    # Create a message model with appropriate attributes
    new_message = MessageModel(message=message, sender_id=sender_id, recipient_id=recipient_id, sent_at=sent_at)

    # Add the message to the database session
    db.session.add(new_message)

    # Commit changes to the database
    db.session.commit()

    # Send a notification to the recipient
    # notify_user(recipient_id)
    send_notification()

    # Redirect to the previous page
    return redirect(request.referrer)


def private_message(recipient_name: str):
    API_KEY = "de5dec155db7939fd3dd72a0549bbb6c"

    url = "https://api.openweathermap.org/data/2.5/weather?q=Bordeaux,fr&appid=" + API_KEY
    response = requests.get(url)

    data = response.json()
    lon = data["coord"]["lon"]
    lat = data["coord"]["lat"]
    description = data["weather"][0]["description"]
    temp = round(data["main"]["temp"] - 273.15, 1)
    feels_like = round(data["main"]["feels_like"] - 273.15, 1)
    humidity = data["main"]["humidity"]
    speed = data["wind"]["speed"]
    deg = data["wind"]["deg"]
    sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S')
    sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S')

    map = folium.Map(location=[data["coord"]["lon"], data["coord"]["lat"]], zoom_start=12)

    folium.Marker([data["coord"]["lon"], data["coord"]["lat"]], popup=data["weather"][0]["description"]).add_to(map)

    map.save("map.html")

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

    # Mark all notifications between the two users as read
    notifications = NotificationModel.query.filter_by(sender_id=g.user.id, recipient_id=user_recipient.id, status='unread').all()
    for notification in notifications:
        notification.status = 'read'
    db.session.commit()

    return render_template("private_message.html",
                           user_recipient=user_recipient,
                           messages=messages,
                           lon = lon,
                           lat = lat,
                           description = description,
                           temp = temp,
                           feels_like = feels_like,
                           humidity = humidity,
                           speed = speed,
                           deg = deg,
                           sunrise = sunrise,
                           sunset = sunset
                           )