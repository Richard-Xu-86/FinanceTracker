from django.urls import path
from userincome import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income', views.add_income, name='add-income'),
    path('income-edit/<int:id>', views.income_edit, name='income-edit'),
    path('income-stats', views.Income_Stats, name='income-stats'),
    path('income-delete/<int:id>', views.income_delete, name='income-delete'),
    path('search-income', csrf_exempt(views.search_income), name='search-income'),
    path('income_summary', views.income_summary, name='income-'),
    path('income-csv', views.export_csv, name='income-export-csv'),
    path('income-excel',views.export_excel, name='income-export-excel'),
    path('income-pdf', views.export_pdf, name='income-export-pdf')
]