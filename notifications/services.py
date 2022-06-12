from .models import Notification

def create_notification(project, user, user_from, notification_type, message_value=None):
    Notification.objects.create(project=project, user=user, user_from = user_from, type=notification_type, message=message_value)