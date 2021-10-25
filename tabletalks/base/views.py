from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tabletalks.base.models import Table, Topic
from tabletalks.base.forms import TableForm


def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
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

    context = {}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


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

    context = {
        'tables': tables,
        'topics': topics,
        'table_count': table_count,
    }
    return render(request, 'base/home.html', context)


def table(request, pk):
    table = Table.objects.get(id=pk)
    context = {'table': table}
    return render(request, 'base/table.html', context)


def create_table(request):
    form = TableForm()
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/table_form.html', context)


def update_table(request, pk):
    table = Table.objects.get(id=pk)
    form = TableForm(instance=table)

    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/table_form.html', context)


def delete_table(request, pk):
    table = Table.objects.get(id=pk)

    if request.method == 'POST':
        table.delete()
        return redirect('home')

    context = {'obj': table}
    return render(request, 'base/delete.html', context)