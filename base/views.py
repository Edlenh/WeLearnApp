from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

#The views page are the information the user will see

def loginPage(request):
    page = 'login'
    #this gives in the loginPage a page variable
    #that variable can be called in html
    if request.user.is_authenticated:
        #if the user is logged in, dont send them to login page
        #redirect them to the home page
        return redirect('home')

    if request.method == 'POST':
        #user POSTS because he is sending his info/ username/password
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        #after user sends his info, we want to GET their post. 
        try:
            #use a try except to catch non users. 
            user =User.objects.get(email=email)
        except:
            messages.error(request, 'User Does Not Exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            #if the user is good to go, call the login function. 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist!')

    context = {'page': page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            #commit = false makes the form tangible
            #freezes the form in time but makes certain checks like casing
            #clean the data 
            user.username = user.username.lower()
            #then save it 
            user.save()
            #after you save the user, they will be logged in and sent to the home page
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error during registration, please try again')

    return render(request, 'base/login_register.html', {'form':form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #search query = q. if q is not none then q is the parameter
    #else q equals to an empty string
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        #topic can search by topic
        Q(name__icontains=q) |
        #name can search by author
        Q(description__icontains=q)
        #description can search by descriptor
    )
    #icontains = insensitve caps
    #icontains= atleast contains a part of the search 
    #for example pyt in python, gen in generic. 
    

    topics= Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics':topics,
             'room_count': room_count,
             'room_messages':room_messages,
    }
    return render(request,'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants= room.participants.all() 

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')

        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    #here the context pairs the room variable with the room iterator. 
    return render(request,'base/room.html',context)



#import roomform to see the form created in the forms.py file

def userProfile(request, pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context= {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form =RoomForm()
    #set the form to link to the RoomForm you created
    topics= Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic= topic,
            name= request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

            
    #the redirect 'home' is sent to the page specified in the url on the app level
    context = {'form':form, 'topics':topics}
    #here the context passed in is the form variable
    #the dict key value pair is form and form 
    #in the html you can pass in form to link to the form context
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    #passing the pk links objects by their private key
    room = Room.objects.get(id= pk)
    #get room by id. 
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not the User')
    #instance is prefilled with the room that was made previously
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html',context ) 

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not the User')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not the User')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url= 'login')
def updateUser(request):
    user= request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics= Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})