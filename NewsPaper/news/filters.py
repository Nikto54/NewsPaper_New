from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django import forms

from .models  import Author


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    author_post = ModelChoiceFilter(field_name='author_post',
                               label='Автор',
                               queryset=Author.objects.all(),)
    title = CharFilter(field_name='title', lookup_expr='contains', label='Заголовок')
    date = DateFilter(field_name='datetime_in', lookup_expr='gt', label='Дата публикации', widget=DateInput)