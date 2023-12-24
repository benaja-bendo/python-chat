import datetime
from flask import render_template, request, redirect, url_for, g
from typing import Optional
from app.models.user_model import UserModel
from app.models.message_model import MessageModel
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
    sent_at = datetime.datetime.now(datetime.timezone.utc)
    new_message = MessageModel(message=message, sender_id=sender_id, recipient_id=recipient_id, sent_at=sent_at)
    db.session.add(new_message)
    db.session.commit()
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