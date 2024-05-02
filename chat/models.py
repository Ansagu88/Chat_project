from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Create your models here.
class Chat(models.Model):
    """
    A model representing a chat message.

    Attributes:
        user (User): The user who sent the message.
        message (str): The message sent by the user.
        response (str): The response sent by the chatbot.
        created_at (datetime): The date and time when the message was sent.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'