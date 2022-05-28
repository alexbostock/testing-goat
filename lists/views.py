from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    errorMessage = None
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            errorMessage = 'List item must not be empty'
    return render(request, 'list.html', {
        'list': list_,
        'error': errorMessage,
    })

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        return render(request, 'home.html', {
            'error': 'List item must not be empty'
        })
    return redirect(f'/lists/{list_.id}/')
