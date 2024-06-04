from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "login.html")


def registration(request):
    if request.method=='POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            _hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            _newUser = User.objects.create(
                firstname = request.POST['firstname'],
                lastname = request.POST['lastname'],
                email = request.POST['email'],
                password = _hash
            )
            _newUser.save()
            request.session['user_id'] = _newUser.id
            return redirect('/dashboard')
    else:
        return redirect ('/')



def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            log_user=User.objects.get(email__iexact=request.POST['email'])
            request.session['user_id'] = log_user.id
            return redirect('/dashboard')
    else:
        return redirect('/')
    
def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'trips':Trip.objects.all(),
        "user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "dashboard.html", context)
    
def go_create(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'trips':Trip.objects.all(),
        "user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'create_trip.html',context)


def create_trip(request):
    if request.method == 'POST':
        errors = Trip.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/new')
        else:
            this_user= User.objects.get(id=request.session['user_id'])
            newtrip=Trip.objects.create(
                destination = request.POST['destination'],
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                itinerary = request.POST['itinerary'],
                organizer = this_user
            )
            newtrip.travelers.add(this_user)
            newtrip.save()
        return redirect(f'/trips/{newtrip.id}')
    else:
        return redirect('/trips/new')
    

def details(request, _id):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'trip':Trip.objects.get(id=_id)
    }
    return render (request, "details.html", context)

def edit(request, _id):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'trip':Trip.objects.get(id=_id)
    }
    return render (request, "edit.html", context)

def edit_trip(request, _id):
    if request.method == 'POST':
        errors = Trip.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/trips/{_id}/edit')  # Redirect back to the edit page for the specific trip
        else:
            _editShow = Trip.objects.get(id=_id)
            this_user = User.objects.get(id=request.session['user_id'])

            _editShow.destination = request.POST['destination']
            _editShow.start_date = request.POST['start_date']
            _editShow.end_date = request.POST['end_date']
            _editShow.itinerary = request.POST['itinerary']
            _editShow.organizer = this_user
            _editShow.save()
            messages.success(request, "Trip successfully updated!")
            return redirect(f'/trips/{_id}')
    return redirect(f'/trips/{_id}/edit')

def delete_trip(request, _id):
        trip = Trip.objects.get(id=_id)
        user_id = request.session.get('user_id')
        
        if user_id == trip.organizer.id:
            trip.delete()
            messages.success(request, "Trip deleted successfully.")
    
        return redirect('/dashboard')

def my_trips(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    my_trips = user.trips.all()
    joinable_trips = Trip.objects.exclude(travelers=user)
    
    context = {
        'user': user,
        'my_trips': my_trips,
        'joinable_trips': joinable_trips,
    }
    
    return render(request, 'mytrips.html', context)

def join_trip(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.filter(id=trip_id).first()
    
    if not trip:
        messages.error(request, 'The trip you are trying to join does not exist.')
    else:
        trip.travelers.add(user)
        messages.success(request, 'You have successfully joined the trip.')
    
    return redirect('my_trips')

def leave_trip(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.filter(id=trip_id).first()
    
    if not trip:
        messages.error(request, 'The trip you are trying to leave does not exist.')
    else:
        trip.travelers.remove(user)
        messages.success(request, 'You have successfully left the trip.')
    
    return redirect('my_trips')

def logout(request):
    del request.session['user_id']
    return redirect('/')