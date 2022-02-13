from django.db import models

class Chat(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()


class Message(models.Model):
    text = models.CharField(max_length=500)
    chat_id = models.IntegerField()
    sender_id = models.IntegerField()
    time = models.TimeField()
# Create your models here.
