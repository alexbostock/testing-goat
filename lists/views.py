from django.shortcuts import redirect, render

from lists.models import Item

def home_page(request):
    if(request.method == 'POST'):
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list')
    return render(request, 'home.html')

def view_list(request):
    return render(request, 'list.html', {
        'items': Item.objects.all()
    })
