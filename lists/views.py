from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError
from django.utils.html import escape

from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """ Функция представления домашней страницы """
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """ Функция представления списка дел """
    todo_list = List.objects.get(pk=list_id)
    error = ""

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=todo_list)
            item.full_clean()
            item.save()
            return redirect(todo_list)
        except ValidationError:
            error = "You can`t have an empty list item"
    return render(request, "list.html", {"list": todo_list, "error": error})


def new_list(request: HttpRequest) -> HttpResponse:
    """Функция представления создает список дел"""
    todo_list = List.objects.create()
    item = Item.objects.create(text=request.POST.get('item_text'), list=todo_list)
    try:
        item.full_clean()
    except ValidationError:
        todo_list.delete()
        error = escape("You can`t have an empty list item")
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{todo_list.pk}/')
