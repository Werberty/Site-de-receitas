from django.shortcuts import render
from utils.recipes.factory import make_recipe

from .models import Recipe


def home(request):
    recepes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recepes,
    })


def category(request, category_id):
    recepes = Recipe.objects.filter(
        category__id=category_id, is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recepes,
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
