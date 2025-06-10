from encodings import search_function
from django.contrib import admin
from .models import Expense, Category

# Register your models here.

class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('amount','category','owner','decription','date')
    search_fields = ('amount','category','owner','decription','date')
    list_per_page = 5
    

admin.site.register(Expense, ExpensesAdmin)
admin.site.register(Category)