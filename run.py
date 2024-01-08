import os
from app import app, db
from app.controllers import homeController, authController,notificationController
from flask import session, g
from app.models.user_model import UserModel
from app.models.notification_model import NotificationModel

with app.app_context():
    db.create_all()


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        g.unread_notification_count = 0
    else:
        g.user = UserModel.query.get(user_id)
        g.unread_notification_count = NotificationModel.query.filter_by(recipient_id=user_id, status='unread').count()


app.add_url_rule("/", view_func=homeController.home, methods=["GET", "POST"])
app.add_url_rule("/message", view_func=homeController.post_message, methods=["POST"])
app.add_url_rule("/private-message/<recipient_name>", view_func=homeController.private_message, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=authController.login, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=authController.register, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=authController.logout, methods=["POST"])
app.add_url_rule("/api/notifications", view_func=notificationController.send_notification, methods=["GET"])

if __name__ == "__main__":
    DEBUG = os.getenv("DEBUG")
    app.run(debug=DEBUG)  
