from django.urls import path
from userexpense import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('expenses-stats', views.Expenses_Stats, name='expenses-stats'),
    path('expense-edit/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('expenses_summary', csrf_exempt(views.expenses_summary), name='expenses-summary'),
    path('export-csv', views.export_csv, name='expenses-export-csv'),
    path('export-excel', views.export_excel, name='expenses-export-excel'),
    path('export-pdf', views.export_pdf, name='expenses-export-pdf'),
    path('set-budget/', views.set_budget, name='set-budget'),
    path('delete-budget/<int:id>/', views.delete_budget, name='delete-budget'),
]