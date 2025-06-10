from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='preferences'),
    path('add-category', views.AddCategory, name='add-category'),
    path('add-source', views.AddSource, name='add-source'),
    path('edit-source/<int:id>', views.EditSource, name='edit-source'),
    path('edit-category/<int:id>', views.EditCategory, name='edit-category'),
    path('delete-source/<int:id>', views.SourceDelete, name='delete-source'),
    path('delete-category/<int:id>', views.CategoryDelete, name='delete-category')
]