
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',SplitExpenseAPIView.as_view(),name='split_expense'),
]
