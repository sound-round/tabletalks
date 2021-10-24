from django.shortcuts import render, redirect
from django.db.models import Q
from tabletalks.base.models import Table, Topic
from tabletalks.base.forms import TableForm


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