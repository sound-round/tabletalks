from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from tabletalks.base.models import Table, Topic, Message
from tabletalks.base.forms import TableForm


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()  # TODO .lower()? (look register_user())
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password.')

    # TODO delete context if it's need
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # TODO .lower()? (look login_user())
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    tables = Table.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()
    table_count = tables.count()
    all_messages = Message.objects.filter(Q(table__topic__name__icontains=q))

    context = {
        'tables': tables,
        'topics': topics,
        'table_count': table_count,
        'all_messages': all_messages,
    }
    return render(request, 'base/home.html', context)


def table(request, pk):
    table = Table.objects.get(id=pk)
    table_messages = table.message_set.all().order_by('created')
    participants = table.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            table = table,
            body = request.POST.get('body')
        )
        table.participants.add(request.user)
        return redirect('table', pk=table.id)

    context = {
        'table': table,
        'table_messages': table_messages,
        'participants': participants,
    }
    return render(request, 'base/table.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    tables = user.table_set.all()
    all_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'tables': tables,
        'all_messages': all_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_table(request):
    form = TableForm()
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.host = request.user
            table.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/table_form.html', context)


@login_required(login_url='login')
def update_table(request, pk):
    table = Table.objects.get(id=pk)
    form = TableForm(instance=table)

    if request.user != table.host:
        return HttpResponse('You are not allowed here.')

    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/table_form.html', context)


@login_required(login_url='login')
def delete_table(request, pk):
    table = Table.objects.get(id=pk)

    if request.user != table.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        table.delete()
        return redirect('home')

    context = {'obj': table}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        table = message.table
        message.delete()
        if not table.message_set.filter(user=request.user):
            table.participants.remove(request.user)

        return redirect('table', pk=table.id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)
