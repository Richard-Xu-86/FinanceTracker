from django.shortcuts import redirect, render
from userexpense.models import Expense
from userincome.models import UserIncome
from .models import Graphprefer
from django.http import JsonResponse
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userexpense.models import Budget, Expense
from django.db.models import Sum
from datetime import date

def LastMonthData(request):
    days_data = 0
    check = Graphprefer.objects.filter(user=request.user).exists()
    if check:
        user = Graphprefer.objects.get(user=request.user)
        graph = user.graph
        month_data = user.month
        if month_data == '1 Month':
            days_data = 30
        elif month_data == '6 Months':
            days_data = 180
        elif month_data == '1 Year':
            days_data = 366
        else:
            days_data = 30
    else:
        graph = 'bar'
        days_data = 30
    today_date = datetime.date.today()
    last_months_ago =today_date - datetime.timedelta(days=days_data)
    expenses = Expense.objects.filter(owner=request.user, date__gte=last_months_ago, date__lte=today_date)
    income = UserIncome.objects.filter(owner=request.user, date__gte=last_months_ago, date__lte=today_date)
    finalresult1= {}
    finalresult2= {}

    def get_category(expenses):
        return expenses.category
    def get_source(income):
        return income.source

    category_list = list(set(map(get_category, expenses)))
    source_list = list(set(map(get_source, income)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount
    def get_income_source_amount(source):
        amount = 0
        filter_by_source = income.filter(source=source)
        for item in filter_by_source:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalresult1[y]=get_expense_category_amount(y)
    for x in income:
        for y in source_list:
            finalresult2[y]=get_income_source_amount(y)

    return JsonResponse({'expense_category_amount':finalresult1, 'income_source_amount':finalresult2, 'type':graph, 'days':month_data}, safe=False)

@login_required
def LastMonth(request):
    graph_data = ('bar','pie','line','radar','doughnut','polarArea')
    Month_data = ('1 Month','6 Months','1 Year')
    check = Graphprefer.objects.filter(user=request.user).exists()
    
    if check:
        user = Graphprefer.objects.get(user=request.user)
        user_graph = user.graph
        user_month = user.month
    else:
        user_graph = 'bar'
        user_month = '1 Month'

    # Determine selected date range
    if user_month == '1 Month':
        days_data = 30
    elif user_month == '6 Months':
        days_data = 180
    elif user_month == '1 Year':
        days_data = 365
    else:
        days_data = 30

    today = date.today()
    start_date = today - datetime.timedelta(days=days_data)
    this_month_start = today.replace(day=1)

    # Budget logic (from old `dashboard()` view)
    budgets = Budget.objects.filter(user=request.user, month__year=today.year, month__month=today.month)

    budget_data = []
    for b in budgets:
        spent = Expense.objects.filter(
            owner=request.user,
            category=b.category,
            date__gte=this_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0

        over_amount = spent - b.amount if spent > b.amount else 0

        budget_data.append({
            'id': b.id,
            'category': b.category,
            'budget': b.amount,
            'spent': spent,
            'remaining': b.amount - spent,
            'over_budget': spent > b.amount,
            'over_amount': over_amount
        })

    if request.method == 'POST':
        graph_selected = request.POST['graph']
        month_selected = request.POST['month']
        if check:
            user.graph = graph_selected
            user.month = month_selected
            user.save()
        else:
            Graphprefer.objects.create(user=request.user, graph=graph_selected, month=month_selected)
        messages.success(request, 'Changes Saved')
        return redirect('dashboard-lastmonth')

    # Add budget_data to context
    context = {
        'user_graph': user_graph,
        'user_month': user_month,
        'graphs': graph_data,
        'months': Month_data,
        'budget_data': budget_data
    }

    return render(request, 'dashboard/index.html', context)
