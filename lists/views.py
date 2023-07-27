from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    """ Функция представления домашней страницы """
    if request.method == "POST":
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect("/lists/ed-v-mire-spisok/")
    return render(request, "home.html")


def view_list(request: HttpRequest) -> HttpResponse:
    """ Функция представления списка дел """
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
