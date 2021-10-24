from django.shortcuts import render
from tabletalks.base.models import Table



# tables = [
#     {'id': 1, 'name': "Let's learn python!"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Frontend developers"},
# ]


def home(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'base/home.html', context)


def table(request, pk):
    table = Table.objects.get(id=pk)
    context = {'table': table}

    return render(request, 'base/table.html', context)
