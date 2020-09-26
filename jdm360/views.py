from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def loginreg(request):
    return render(request, 'loginreg.html')

def services(request):
    return render(request,'services.html')

def aboutus(request):
    return render(request,'aboutus.html')

def register(request):
    if request.method == 'POST':
        errors = Users.objects.validate(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect("/loginreg")
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Users.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['name'] = new_user.fname
        request.session['user_id'] = new_user.id
        return(render(request, 'client.html'))

def login(request):
    context = {
        'error' : ""
    }
    if request.method == 'POST':
        current_user = Users.objects.filter(email=request.POST['email'])
        if len(current_user) > 0:
            current_user = current_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), current_user.password.encode()):
                request.session['name'] = current_user.fname
                request.session['user_id'] = current_user.id
                if current_user.classification == 'admin':
                    return redirect('/admin')
                if current_user.classification == 'Photographer':
                    return redirect('/photographerpage')                
                return redirect('/client')
            return redirect('/')
    return render(request,'index.html')

def order(request):
    return render(request, 'order.html')

def placeorder(request):
    if request.method == 'POST':
        new_location = Locations.objects.create(address= request.POST['address'], city=request.POST['city'], state=request.POST['state'],zipcode=request.POST['zipcode'])
        new_order = Orders.objects.create(location=new_location, package=request.POST['package'],client=Users.objects.get(id=request.session['user_id']),orderdate=request.POST['date'], status='Open')
        if Users.objects.get(id=request.session['user_id']).classification == 'admin':
            return redirect('/admin')
        if Users.objects.get(id=request.session['user_id']).classification == 'client':
            return redirect('/client')
        if Users.objects.get(id=request.session['user_id']).classification == 'Photographer':
            return redirect('/photographerpage')
        return redirect('/')
    return redirect('/order')

def updateorder(request, order_id):
    if request.method == "POST":
        updated_order = Orders.objects.get(id=order_id)
        updated_order.package = request.POST['package']
        updated_order.address = request.POST['address']
        updated_order.city = request.POST['city']
        updated_order.state = request.POST['state']
        updated_order.zipcode = request.POST['zipcode']
        updated_order.photographer = request.POST['photographer']
        updated_order.save()
        return redirect('/admin')

def assign(request, order_id):
    if request.method == "POST":
        updated_order = Orders.objects.get(id=order_id)
        updated_order.photographer.set(Users.objects.get(id=request.POST[photographer]))
        updated_order.save()
        return redirect('/admin')


def admin(request):
    if Users.objects.get(id=request.session['user_id']).classification == 'admin':
        context = {
            'all_orders' : Orders.objects.all().order_by('status'),
            'all_users' : Users.objects.all().order_by('classification'),
        } 
        return render(request, 'admin.html', context)
    return redirect('/client')

def photopage(request):
    if Users.objects.get(id=request.session['user_id']).classification == 'Photographer':
        context = {
            'all_orders' : Orders.objects.all().order_by('status'),
            'all_users' : Users.objects.all().order_by('classification'),
        } 
        return render(request, 'photographer.html', context)
    return redirect('/client')

def client(request):
    if Users.objects.get(id=request.session['user_id']).classification == 'client':
        context = {
            'all_orders' : Orders.objects.filter(client=Users.objects.get(id=request.session['user_id'])).order_by('orderdate'),
        } 
        return render(request, 'client.html', context)
    return render(request,'index.html')

def completed(request, order_id):
        current_order = Orders.objects.get(id=order_id)
        new_status = OrderStatus.objects.create(status='Completed',order = current_order)
        return render(request,'admin.html')

def edit(request, order_id):
    context = {
        'current_order' : Orders.objects.get(id=order_id),
        'photographers' : Users.objects.filter(classification="Photographer"),
    }
    return render(request, 'edit.html', context)

def view(request, order_id):
    context = {
        'current_order' : Orders.objects.get(id=order_id),
        'address' : Orders.objects.get(id=order_id).location.address,
        'city' : Orders.objects.get(id=order_id).location.city,
        'state' : Orders.objects.get(id=order_id).location.state,
    }
    return render(request, 'view.html', context)

def deleteorder(request, order_id):
    deletedorder = Orders.objects.get(id=order_id)
    deletedorder.delete()
    return redirect('/admin')
    

def photographer(request, user_id):
    photographer = Users.objects.get(id=user_id)
    photographer.classification = "Photographer"
    photographer.save()
    return redirect('/admin')

def makeadmin(request, user_id):
    photographer = Users.objects.get(id=user_id)
    photographer.classification = "admin"
    photographer.save()
    return redirect('/admin')

def makeclient(request, user_id):
    photographer = Users.objects.get(id=user_id)
    photographer.classification = "client"
    photographer.save()
    return redirect('/admin')

def payorder(request, order_id):
    payorder = Orders.objects.get(id=order_id)
    payorder.status='Paid'
    payorder.save()
    return redirect('/admin')

def completed(request, order_id):
    payorder = Orders.objects.get(id=order_id)
    payorder.status='Closed'
    payorder.save()
    return redirect('/admin')

def openorder(request, order_id):
    payorder = Orders.objects.get(id=order_id)
    payorder.status='Open'
    payorder.save()
    return redirect('/admin')

def logout(request):
    request.session.flush()
    return redirect('/')