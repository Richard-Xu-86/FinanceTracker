from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userprefer.models import Userprefer
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.db.models import Sum
import xlwt
import csv
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from xhtml2pdf import pisa
from datetime import timedelta
from django.utils.timezone import now


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            decription__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required
def index(request):
    user = request.user
    range_filter = request.GET.get('range', 'lifetime')
    today = now().date()

    income = UserIncome.objects.filter(owner=user)

    # Date filtering
    if range_filter == '1month':
        start_date = today - timedelta(days=30)
        income = income.filter(date__gte=start_date)
    elif range_filter == '6months':
        start_date = today - timedelta(days=182)
        income = income.filter(date__gte=start_date)
    elif range_filter == '1year':
        start_date = today - timedelta(days=365)
        income = income.filter(date__gte=start_date)

    # Sum with fallback
    sum_amount = income.aggregate(Sum('amount'))['amount__sum'] or 0

    # Pagination
    paginator = Paginator(income, 10)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    # Currency
    currency_check = Userprefer.objects.filter(user=user)
    currency = currency_check.first().currency if currency_check.exists() else None

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'sum': sum_amount
    }
    return render(request, 'userincome/index.html', context)


@login_required
def add_income(request):
    source = Source.objects.all()
    context= {
        'sources':source,
        'values':request.POST
        }
    if request.method == 'GET':
        return render(request, 'userincome/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/add_income.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userincome/add_income.html', context)
        if source== 'Choose...':
            messages.error(request, 'Source is required')
            return render(request, 'userincome/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/add_income.html', context)
        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, decription=decription)
        messages.success(request, 'Income saved successfully')
        return redirect('income')

@login_required
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income':income,
        'values':income,
        'sources':sources
        }
    if request.method == 'GET':
        return render(request, 'userincome/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userincome/edit_income.html', context)
        if source == 'Choose...':
            messages.error(request, 'Source is required')
            return render(request, 'userincome/edit_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/edit_income.html', context)

        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.decription=decription
        income.save()

        messages.success(request, 'Income Updated successfully')
        return redirect('income')

@login_required
def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income is removed')
    return redirect('income')



def income_summary(request):
    today_date = datetime.date.today()
    six_months_ago =today_date - datetime.timedelta(days=30*6)
    income = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=today_date)
    finalresult= {}

    def get_source(income):
        return income.source

    source_list = list(set(map(get_source, income)))

    def get_income_source_amount(source):
        amount = 0
        filter_by_source = income.filter(source=source)
        for item in filter_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in source_list:
            finalresult[y]=get_income_source_amount(y)

    return JsonResponse({'income_source_amount':finalresult}, safe=False)

@login_required
def Income_Stats(request):
    return render(request, 'userincome/stats.html')

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Decription','Source','Date'])

    incomes = UserIncome.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount, income.decription, income.source, income.date])

    return response


@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Decription','Source','Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style =  xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner=request.user).values_list('amount','decription','source','date')

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
    income = UserIncome.objects.filter(owner=request.user)
    sum = income.aggregate(Sum('amount'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Expenses_'+str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] ='binary'
    context = {
        'incomes':income,
        'total':sum,
        'date':date,
        'user':user,
        'domain':domain_data
    }
    html_string = render_to_string('userincome/pdf-output.html', context)

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('not found')
    return response

