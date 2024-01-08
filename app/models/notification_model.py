from datetime import datetime
from app import db


class NotificationModel(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.VARCHAR(255), nullable=False) # type of notification (message, invitation, etc.)
    subject = db.Column(db.VARCHAR(255), nullable=False) # subject of the notification
    body = db.Column(db.TEXT, nullable=False) # body of the notification
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id')) # identifier of the sender (user or group)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id')) # identifier of the recipient (user or group)
    date = db.Column(db.DateTime, default=datetime.utcnow) # date of the notification
    status = db.Column(db.VARCHAR(255), nullable=False) # status of the notification (read, unread, deleted, etc.)

    def __repr__(self):
        return f"<Notification {self.id} of Type {self.type} for User {self.recipient_id}>"


