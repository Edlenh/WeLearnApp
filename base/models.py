from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null= True, unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.
#create database tables here. 
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    #someone must host the room so this is related to a user. 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    #a topic can have many rooms. but a room can only have one topic 
    name = models.CharField(max_length = 200)
    description = models.TextField(null=True, blank= True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
        #ordering by latest created
    def __str__(self):
        return self.name 
        # def __str here will return the name of the room in the database/admin page

class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    #a user can have many messages but a message has one user. 
    #the user and message have a one to many relationship
    #CASCADE delete means one you delete one thing, things related to the class will also be deleted
    room= models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]
        # this is basically a preview, the first 50 characters. 