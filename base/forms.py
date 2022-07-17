from django.forms import ModelForm 
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

#this is linked to the models in the model.py file

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2' ]



class RoomForm(ModelForm):
    class Meta:
        model = Room
        #specifcy where you want to create a form for
        #in this case we are using the Room model 
        fields = '__all__'
        exclude = ['host','participants']
        #specify which fields you want to see

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email', 'bio']
       
        