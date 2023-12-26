from flask import render_template, request, redirect, url_for, g,Response
import json

def send_notification():
    # Traitement de la requête

    # Envoi de l'événement "see" à l'utilisateur
    # def generate_event():
    #     event_data = {"message": "Notification vue par l'utilisateur"}
    #     yield f"data: {json.dumps(event_data)}\n\n"
    # return Response(generate_event(), mimetype="text/event-stream")
    # Envoi de l'événement "see" à l'utilisateur
    event_data = {"message": "Notification vue par l'utilisateur"}
    return Response(f"data: {json.dumps(event_data)}\n\n", mimetype="text/event-stream")

def new_message_notification():
    pass
