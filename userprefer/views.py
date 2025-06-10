from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from django.contrib import messages
from .models import Userprefer
from userexpense.models import Category
from userincome.models import Source
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    category = Category.objects.all()
    source = Source.objects.all()
    user_prefer = None
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})

    check = Userprefer.objects.filter(user=request.user).exists()
    if check:
        user_prefer = Userprefer.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'userprefer/index.html', {'currencies':currency_data, 'user_prefer':user_prefer, 'category':category, 'source':source})
        
    elif request.method == 'POST':
        currency = request.POST['currency']
        if check:
            user_prefer.currency=currency
            user_prefer.save()
        else:
            Userprefer.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes Saved')
        return render(request, 'userprefer/index.html', {'currencies':currency_data, 'user_prefer':user_prefer, 'category':category, 'source':source})

@login_required
def AddCategory(request):
    if request.method =='GET':
        return render(request, 'userprefer/add-category.html')

    if request.method =='POST':
        category = request.POST['category']
        context = {
            'values':request.POST
        }
        if not category:
            messages.error(request, 'Category is not found')
            return render(request, 'userprefer/add-category.html', context)
        Category.objects.create(name=category)
        messages.success(request, 'Category created successfully')
        return redirect('preferences')

@login_required
def AddSource(request):
    if request.method =='GET':
        return render(request, 'userprefer/add-source.html')

    if request.method =='POST':
        source = request.POST['source']
        context = {
            'values':request.POST
        }
        if not source:
            messages.error(request, 'Source is not found')
            return render(request, 'userprefer/add-source.html', context)
        Source.objects.create(name=source)
        messages.success(request, 'Source created successfully')
        return redirect('preferences')

@login_required
def EditSource(request, id):
    if request.method == 'GET':
        source = Source.objects.get(pk=id)
        context = {
            'source':source,
            'values':source
        }
        return render(request, 'userprefer/edit-source.html', context)

    if request.method == 'POST':
        source = Source.objects.get(pk=id)
        source_got = request.POST['source']
        context = {
            'source':source,
            'values':request.POST
        }
        if not source_got:
            messages.error(request, 'Source cannot be empty')
            return render(request, 'userprefer/edit-source.html', context)

        source.name = source_got
        source.save()
        messages.success(request, 'Source updated successfully')
        return redirect('preferences')


@login_required
def SourceDelete(request, id):
    source = Source.objects.get(pk=id)
    source.delete()
    messages.success(request, 'Source is removed')
    return redirect('preferences')


@login_required
def EditCategory(request, id):
    if request.method == 'GET':
        category = Category.objects.get(pk=id)
        context = {
            'category':category,
            'values':category
        }
        return render(request, 'userprefer/edit-category.html', context)

    if request.method == 'POST':
        category = Category.objects.get(pk=id)
        category_got = request.POST['category']
        context = {
            'category':category,
            'values':request.POST
        }
        if not category_got:
            messages.error(request, 'Category cannot be empty')
            return render(request, 'userprefer/edit-category.html', context)

        category.name = category_got
        category.save()
        messages.success(request, 'Category updated successfully')
        return redirect('preferences')


@login_required
def CategoryDelete(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, 'Category is removed')
    return redirect('preferences')