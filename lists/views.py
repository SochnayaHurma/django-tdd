from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def home_page(request: HttpRequest) -> HttpResponse:
    """ Функция представления домашней страницы """
    return render(request, "home.html", {
        'new_item_text': request.POST.get('item_text')
    })
