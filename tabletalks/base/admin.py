from django.contrib import admin
from tabletalks.base.models import Table, Topic, Message


admin.site.register(Table)
admin.site.register(Topic)
admin.site.register(Message)