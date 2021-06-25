import django_filters
from django import forms
from django.forms.widgets import NumberInput
from django_filters import DateFilter, CharFilter

from .models import *


class ExpenseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_added", lookup_expr='gte')
    end_date = DateFilter(field_name="date_added", lookup_expr='lte')
    # date_added = forms.DateTimeField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = UserExpense
        fields = ('cost', 'date_added', 'category')
        exclude = ('date_added')
