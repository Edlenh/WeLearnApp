from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message , User

admin.site.register(User)
#to add things to the admin site you must register them here. 
admin.site.register(Room)
#register each model you create in the models.py file. 
admin.site.register(Topic)
#on the admin page you can access this information and even change them. 
admin.site.register(Message)