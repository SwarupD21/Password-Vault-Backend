from .views import *
from django.urls import path

urlpatterns = [
    path('create/',CreateView.as_view(),name="vault-create"),
    path('list/',ListView.as_view(),name="vault-list"),
    path('update/<int:id>',UpdateView.as_view(),name="vault-update"),
    path('delete/<int:id>',DeleteView.as_view(),name="vault-delete"),
    path('detail/<int:id>',DetailView.as_view(),name="vault-detail"),
]
