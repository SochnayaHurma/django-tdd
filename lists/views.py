from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request: HttpRequest) -> HttpResponse:
    """ Функция представления домашней страницы """
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """ Функция представления списка дел """
    todo_list = List.objects.get(pk=list_id)
    form = ExistingListItemForm(for_list=todo_list)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=todo_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(todo_list)
    return render(request, "list.html", {"list": todo_list, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    """Функция представления создает список дел"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        todo_list = List.objects.create()
        form.save(for_list=todo_list)
        return redirect(todo_list)
    return render(request, 'home.html', {"form": form})
