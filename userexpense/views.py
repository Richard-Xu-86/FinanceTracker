from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from datetime import datetime, timedelta, date
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import json
from userprefer.models import Userprefer
import csv
import xlwt
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum
from django.utils.timezone import now
from .models import Budget, Category
from django.shortcuts import get_object_or_404


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            decription__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)



@login_required
def home(request):
    user = request.user
    range_filter = request.GET.get('range', 'lifetime')
    today = now().date()

    # Start with all expenses
    expenses = Expense.objects.filter(owner=user)

    # Apply date filtering
    if range_filter == '1month':
        start_date = today - timedelta(days=30)
        expenses = expenses.filter(date__gte=start_date)
    elif range_filter == '6months':
        start_date = today - timedelta(days=182)
        expenses = expenses.filter(date__gte=start_date)
    elif range_filter == '1year':
        start_date = today - timedelta(days=365)
        expenses = expenses.filter(date__gte=start_date)
    # else: lifetime = no filter

    # Calculate total
    sum_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Paginate
    paginator = Paginator(expenses, 10)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    # Get user currency
    currency_check = Userprefer.objects.filter(user=request.user)
    currency = currency_check.first().currency if currency_check.exists() else None

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'sum': sum_amount
    }

    return render(request, 'userexpense/main.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context= {
        'categories':categories,
        'values':request.POST
        }
    if request.method == 'GET':
        return render(request, 'userexpense/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userexpense/add_expense.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userexpense/add_expense.html', context)
        if category == 'Choose...':
            messages.error(request, 'Category is required')
            return render(request, 'userexpense/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userexpense/add_expense.html', context)
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, decription=decription)
        messages.success(request, 'Expense saved successfully')
        return redirect('home')


@login_required
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
        }
    if request.method == 'GET':
        return render(request, 'userexpense/expense-edit.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userexpense/expense-edit.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userexpense/expense-edit.html', context)
        if category == 'Choose...':
            messages.error(request, 'Category is required')
            return render(request, 'userexpense/expense-edit.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userexpense/expense-edit.html', context)

        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.decription=decription
        expense.save()

        messages.success(request, 'Expense Updated successfully')
        return redirect('home')

@login_required
def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense is removed')
    return redirect('home')

def expenses_summary(request):
    today_date = date.today()
    six_months_ago = today_date - timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=today_date)
    finalresult= {}

    def get_category(expenses):
        return expenses.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalresult[y]=get_expense_category_amount(y)

    return JsonResponse({'expense_category_amount':finalresult}, safe=False)

@login_required
def Expenses_Stats(request):
    return render(request, 'userexpense/stats.html')


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Decription','Category','Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.decription, expense.category, expense.date])

    return response

@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Decription','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style =  xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount','decription','category','date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response

@login_required
def export_pdf(request):
    domain_data = 'http://'+get_current_site(request).domain
    date = datetime.datetime.now
    user = request.user
    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "inline; filename=Expenses"+str(datetime.datetime.now())+".pdf"
    response['Content-Transfer-Encoding'] ='binary'
    context = {
        'expenses':expenses,
        'total':sum,
        'date':date,
        'user':user,
        'domain':domain_data
    }
    html_string = render_to_string('userexpense/pdf-output.html', context)

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('not found')
    return response

@login_required
def set_budget(request):
    if request.method == 'POST':
        category = request.POST['category']
        amount = float(request.POST['amount'])
        month = datetime.strptime(request.POST['month'], "%Y-%m")

        Budget.objects.update_or_create(
            user=request.user,
            category=category,
            month=month,
            defaults={'amount': amount}
        )
        messages.success(request, 'Budget set successfully!')
        return redirect('dashboard-lastmonth')

    categories = Category.objects.all()
    today = datetime.today()

    return render(request, 'userexpense/set_budget.html', {
        'categories': categories,
        'today': today
    })

@login_required
def delete_budget(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    budget.delete()
    messages.success(request, f"Budget for '{budget.category}' deleted.")
    return redirect('dashboard-lastmonth')