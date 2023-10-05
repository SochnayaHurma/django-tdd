from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import get_user_model
from typing import Optional

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

User = get_user_model()


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
        todo_list = List()
        todo_list.owner = request.user
        todo_list.save()
        form.save(for_list=todo_list)
        return redirect(todo_list)
    return render(request, 'home.html', {"form": form})


def my_lists(request: HttpRequest, email: Optional[str] = None) -> HttpResponse:
    """
    Представление: при указанном параметре email отрисовывает списки привязанные
    к данному пользователю
    """
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {"owner": owner})
