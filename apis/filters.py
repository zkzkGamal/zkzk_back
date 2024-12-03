import django_filters
from django_filters import CharFilter

from django import forms

from .models import *

class PostFilter(django_filters.FilterSet):
	title = CharFilter(field_name='title', lookup_expr="icontains", label='title')
	tags = django_filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(),
		)
	class Meta:
		model = ProjectPost
		fields = ['title', 'tags']