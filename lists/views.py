from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """ Функция представления домашней страницы """
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    """ Функция представления списка дел """
    todo_list = List.objects.get(pk=list_id)
    items = Item.objects.filter(list=todo_list)
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest) -> HttpResponse:
    """Функция представления создает список дел"""
    todo_list = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), list=todo_list)
    return redirect(f'/lists/{todo_list.pk}/')
