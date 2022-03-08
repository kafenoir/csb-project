from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funds = models.IntegerField(default=100)
    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField('event name', max_length=50)
    date = models.DateTimeField('event date')
    price = models.IntegerField('ticket price', default=0)
    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booker = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, default=000000000000)
    def __str__(self):
        return self.event.name
