from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from dg.forms import SendMessageFrom
from dg.models import Message, Chat
import datetime
from django.http import *
from dg.forms import UserRegistrationForm, ChangePasswordForm, CreateChatForm
from django import forms
from django.forms.utils import ErrorList
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


def get_base_context():
    menu = {
        'Главная': '/',
        'Логин': '/login',
        'Регистрация': '/register',
        'Выход': '/logout',
        'Глобальный чат': '/global',
        'Профиль': '/profile'
    }
    context = {'menu': menu}
    return context


def home_page(request):
    context = get_base_context()
    if request.method == 'GET':
        chats1 = Chat.objects.all().filter(uid1=request.user.id)
        chats2 = Chat.objects.all().filter(uid2=request.user.id)
        chats = chats1.union(chats2)
        context['chats'] = chats
        names = {}
        for chat in chats:
            if chat.uid1 == request.user.id:
                names[chat.id] = User.objects.all().filter(id=chat.uid2)[0].username
            elif chat.uid2 == request.user.id:
                names[chat.id] = User.objects.all().filter(id=chat.uid1)[0].username
        context['names'] = names
        messages = []
        for chat in chats:
            for message in Message.objects.all().filter(chat_id=chat.id):
                messages.append(message)
        context['messages'] = messages
        context['newchatform'] = CreateChatForm()
    return render(request, "index.html", context)


def register(request):
    """function returns register page(/register) to the client and saves new users

    :request: variable containing http parameters
    """
    context = get_base_context()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return redirect('/login')
    else:
        user_form = UserRegistrationForm()
    context['user_form'] = user_form
    return render(request, 'registration/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.data.get('old_password')):
                user = User.objects.get(username__exact=request.user.username)
                user.set_password(form.data.get('new_password'))
                user.save()
            else:
                raise forms.ValidationError("You forgot to fill in the password field.")

        return redirect('/logout')
    if not request.user.is_authenticated:
        return redirect('/login')
    change_pass_form = ChangePasswordForm()
    context = {'user': request.user, 'change_pass_form': change_pass_form}
    return render(request, 'profile.html', context)


def sendMessage(request):
    if request.method == 'POST':
        user_form = SendMessageFrom(request.POST)
        if user_form.is_valid():
            new_field = Message(time=datetime.datetime.now(), chat_id=user_form.chat_id, sender_id=request.user.id,
                                text=user_form.text)
            new_field.save()
    else:
        return None

@require_http_methods(["POST"])
def newChat(request):
    context = get_base_context()
    if request.method == 'POST':
        user_form = CreateChatForm(request.POST)
        if user_form.is_valid():
            if not User.objects.all().filter(username=user_form.data.get('user_to')):
                raise forms.ValidationError('No such user')
            else:
                secondusername = user_form.data.get('user_to')
                new_field = Chat(uid1=request.user.id, uid2=User.objects.all().filter(username=secondusername)[0].id)
                new_field.save()
        return redirect('/')

