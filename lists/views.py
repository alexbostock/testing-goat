from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

def home_page(request):
    if(request.method == 'POST'):
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    return render(request, 'home.html', {
        'items': Item.objects.all()
    })
