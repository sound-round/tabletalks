from django.forms import ModelForm
from tabletalks.base.models import Table


class TableForm(ModelForm):

    class Meta:
        model = Table
        fields = '__all__'
        exclude = ['host', 'participants']