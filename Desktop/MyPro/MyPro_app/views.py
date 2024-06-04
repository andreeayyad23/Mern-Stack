from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Show

def index(request):
    return redirect("/showall")

def showall(request):
    data = {
        'shows': Show.objects.all(),
    }
    return render(request, 'showall.html', data)

def go_create(request):
    return render(request, 'index.html')

def createshow(request):
    if request.method == "POST":
        errors = Show.objects.show_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/create')  # Redirect back to create form if there are errors
        else:
            new_show = Show.objects.create(
                title=request.POST['title'],
                network=request.POST['network'],
                date=request.POST['date'],
                description=request.POST['description']
            )
            return redirect(f'/shows/{new_show.id}')
    else:     
        return redirect('/')

def showone(request, _id):
    context = {
        'show': Show.objects.get(id=_id)
    }
    return render(request, 'show.html', context)

def go_edit(request, _id):
    context = {
        'show': Show.objects.get(id=_id)
    }
    return render(request, 'update.html', context)

def editshow(request, _id):
    if request.method == "POST":
        errors = Show.objects.show_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/shows/{_id}/edit')
        else:
            show_to_edit = Show.objects.get(id=_id)
            show_to_edit.title = request.POST['title']
            show_to_edit.network = request.POST['network']
            show_to_edit.date = request.POST['date']
            show_to_edit.description = request.POST['description']
            show_to_edit.save()
            return redirect(f'/shows/{_id}')
    return redirect(f'/shows/{_id}/edit')

def delete_show(request, _id):
    show_to_delete = Show.objects.get(id=_id)
    show_to_delete.delete()
    return redirect('/')