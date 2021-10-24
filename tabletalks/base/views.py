from django.shortcuts import render, redirect
from tabletalks.base.models import Table, Topic
from tabletalks.base.forms import TableForm


# tables = [
#     {'id': 1, 'name': "Let's learn python!"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Frontend developers"},
# ]


def home(request):
    tables = Table.objects.all()
    topics = Topic.objects.all()
    context = {'tables': tables, 'topics': topics}
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