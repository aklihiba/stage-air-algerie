from django.contrib.auth import models
import django_filters
from budget.models import Pos6

class pos_filter(django_filters.FilterSet):
    class Meta:
        model=Pos6
        fields=['scf']
        