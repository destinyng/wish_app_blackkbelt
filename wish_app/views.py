from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method != 'POST':
        return redirect ('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.first_name
        #messages.info(request, "User registered; log in now")
    return redirect('/wishes')
   


def login(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['first_name'] = logged_user.first_name

                return redirect('/wishes')
        messages.error(request, "Email and password are incorrect")
        return redirect('/')

def stats(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.filter(id=request.session['userid'])[0]
        all_wishes = Wish.objects.filter(is_granted = True)
    
        context = {
            'all_granted_wishes_count': len(all_wishes),
            'user_pending_wishes_count': logged_user.pending_wishes,
            'user_granted_wishes_count': logged_user.granted_wishes
        }
    return render(request, 'stats.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def wishes(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.get(id=request.session['userid'])
        Wish.objects.filter(wished_by= logged_user)

        all_wishes = Wish.objects.filter(is_granted = True)
        filtered_wishes = []
        for wish in all_wishes:
            if (wish.wished_by.id != logged_user.id):
                filtered_wishes.append(wish)
            # if (wish.is_granted == True):
            #     filtered_wishes.append(wish)

        context ={
            'my_wishes': Wish.objects.filter(wished_by= logged_user),
            'all_wishes': filtered_wishes,
            'user': logged_user
        }
        return render(request, 'wishes.html', context)



def edit(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=id)
    context = {
        'wish': wish
    }
    return render(request, 'edit.html', context)
        
def update(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/edit/{{id}}")  
    # update wish!
    to_update = Wish.objects.get(id=id)
    # updates each field
    to_update.name = request.POST['name']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect('/wishes')


def new(request):
    return render(request, 'new.html')

def create(request):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Wish.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    logged_user = User.objects.get(id=request.session['userid'])   
    Wish.objects.create(
        name = request.POST['name'],
        description = request.POST['description'],
        is_granted = False,
        wished_by = logged_user
    )
    logged_user.pending_wishes += 1
    logged_user.save()
    return redirect('/wishes')



def delete(request,id):
    to_delete = Wish.objects.get(id=id)
    to_delete.delete()
    return redirect('/wishes')

def make_it_grant(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method == "POST":
        logged_user = User.objects.get(id=request.session['userid'])
        wish_to_grant = Wish.objects.get(id=id)
        if logged_user.id == wish_to_grant.wished_by.id:
            wish_to_grant.is_granted = True
            wish_to_grant.save()
            logged_user.granted_wishes += 1
            logged_user.pending_wishes -= 1
            logged_user.save()
        else:
            return redirect('/wishes')

    return redirect('/wishes')

def like(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method == "POST":
        logged_user = User.objects.get(id=request.session['userid'])
        wish_to_like = Wish.objects.get(id=id)
        liked_users = wish_to_like.user_that_like_wish
        liked_users.add(logged_user)
    return redirect('/wishes')


def logout(request):
    request.session.flush()
    return redirect('/')
