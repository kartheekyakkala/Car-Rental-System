from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages,auth
from CarRentalApp.models import *
from datetime import datetime
import requests
import json

# Create your views here.
def Home(request):
    username = request.session['username']
    cdata=car_details.objects.all()
    context={
        'data':cdata,
        'username':username,
        "carcount":cdata.count()
    }
    return render(request,'home.html',context)

def car(request):
    username = request.session['username']
    cdata=car_details.objects.all()
    context={
        'data':cdata,
        'username':username
    }
    return render(request,'car.html',context)

# def contact(request):
#     username = request.session['username']
#     context={
#         'username':username
#     }
#     return render(request,'contact.html',context)

def booking(request):
    username = request.session['username']
    cdata=car_booking.objects.all()
    context={
        'data':cdata,
        'username':username
    }
    return render(request,'booking.html',context)

def total_booking(request):
    username = request.session['username']
    cdata=car_booking.objects.all()
    context={
        'data':cdata,
        'username':username
    }
    return render(request,'admin_page/total_booking.html',context)

def edit_booking(request, id):
    booking_data = car_booking.objects.filter(id = id).first()
    print(booking_data)
    car_data = car_details.objects.filter(name= booking_data.car_name).first()
    booking_data.confirm_at=datetime.now()
    booking_data.booking_status=True
    booking_data.save()
    car_data.is_available=False
    car_data.save()
    messages.success(request,'Booking processed successfully')
    return redirect('total_booking')

def journey_status(request, id):
    booking_data = car_booking.objects.filter(id = id).first()
    car_data = car_details.objects.filter(name= booking_data.car_name).first()
    # booking_data.confirm_at=datetime.now()
    booking_data.booking_status=False
    booking_data.journey_status=True
    booking_data.save()
    car_data.is_available=True
    car_data.save()
    messages.success(request,'journey Completed successfully')
    return redirect('total_booking')

def delete_booking(request, id):
    book_data = car_booking.objects.filter(id = id).first()
    car_data = car_details.objects.filter(name= book_data.car_name).first()
    car_data.is_available = True
    car_data.save()
    book_data.delete()
    messages.success(request,'Booking deleted successfully')
    return redirect('total_booking')
    
def car_detail(request,id):
    username = request.session['username']
    cdata=car_details.objects.get(id=id)
    if request.method == "POST":
        username = request.session['username']
        if username == "":
            messages.warning(request,'For booking login is required')
            return redirect('/login/')
        else:
            name = request.session['name']
            Email = request.session['email']
            mobile_no = request.session['mobile']
            r_uname = username
            r_ctname = name
            r_email = Email
            r_mobile = mobile_no
            r_images = cdata.carimage
            r_cname = cdata.name
            r_city = request.POST['city']
            r_zipcode = request.POST['zipcode']
            r_address = request.POST['address']
            r_bk_from = request.POST['bk_from']
            r_bk_to = request.POST['bk_to']
            car_booking(carimage=r_images,car_name=r_cname,customer_name=r_ctname,customer_username=r_uname,
            mobile=r_mobile,email=r_email,city=r_city,zipcode=r_zipcode,address=r_address,booking_from=r_bk_from,booking_to=r_bk_to).save()
            messages.success(request,'Your car booked successfully')
            return redirect('booking')
    else:
        # ddata=car_details.objects.get(id=id)
        return render(request,'car_details.html',{'data':cdata,'username':username})


def login(request):
    return render(request,'login.html')

def dashboard(request):
    subdata=subscriber.objects.all().count()
    cardata=car_details.objects.all().count()
    bookingdata=car_booking.objects.all().count()
    

    return render(request,'admin_page/dashboard.html',{'subdata':subdata,'cardata':cardata,'bookingdata':bookingdata})

def logout(request): 
    auth.logout(request)
    request.session['username'] = ""
    return redirect('/')

def login_success(request):
    if request.method == "POST":
        uname = request.POST['username']
        passwd = request.POST['password']
        try:
            # if subscriber.objects.filter(username=uname,password=passwd).exists():
            roledata = subscriber.objects.get(username=uname,password=passwd).role
            fname = subscriber.objects.get(username=uname,password=passwd).FullName
            Username = subscriber.objects.get(username=uname,password=passwd).username
            mobile = subscriber.objects.get(username=uname,password=passwd).mobile
            email = subscriber.objects.get(username=uname,password=passwd).email
            request.session['role'] = roledata
            role=request.session['role']

            request.session['username'] = Username
            Username=request.session['username']

            request.session['mobile'] = mobile
            mobile_no = request.session['mobile']

            request.session['email'] = email
            Email = request.session['email']
            
            request.session['name']=fname
            name=request.session['name']

            request.session['role'] = roledata
            if role == "admin":
                return redirect('/dashboard/')
            elif role == "customer":
                return redirect('/home/')

            else:
                messages.success(request,'Invalid Credentials')
                return redirect('/login/')
        except:
            messages.error(request,'Invalid User name or Password')
            return HttpResponseRedirect('/login/')                        
    else:
        messages.error(request,'Mehod Not Found')
        return HttpResponseRedirect('/login/')


def customer_register(request):
    if request.method =='GET':
        return render(request,'customer/customer_register.html')
    elif request.method =='POST':   
        r_Fname = request.POST['fname']
        r_email = request.POST['email']
        r_mobile = request.POST['mobile']
        r_uname = request.POST['uname']
        r_pass = request.POST['pwd']
        r_role = "customer"
        if subscriber.objects.filter(username=r_uname).exists():
            messages.warning(request,'Username "'+ r_uname +'" already exists')
            return redirect('customer/customer_register.html')
        else:
            subscriber(FullName=r_Fname,mobile=r_mobile,email=r_email,username=r_uname,password=r_pass,role=r_role).save()
            messages.success(request,'Customer "'+ r_Fname +'"Registered successfully')
            return HttpResponseRedirect('/login/')
    else:
        return render(request,'customer/customer_register.html')

def car_list(request):
    cdata=car_details.objects.all()
    context={
        'data':cdata
    }
    return render(request,'admin_page/car/car_list.html',context)

def add_car(request):
    if request.method == 'POST' and request.FILES['img']:
        cname= request.POST["cname"]
        images= request.FILES["img"]
        Fuel= request.POST["fuel"]
        Seats= request.POST["seats"]
        Mileage= request.POST["mileage"]
        Luggage= request.POST["luggage"]
        rentprice= request.POST["rp"]
        City= request.POST["city"]
        Features= request.POST["features"]
        Description= request.POST["descripton"]
        car_details(name=cname,carimage=images,fuel=Fuel,seats=Seats,mileage=Mileage,luggage=Luggage,
        rent_amount=rentprice,city=City,features=Features,descripton=Description).save()
        messages.success(request,'Car "'+cname+'"Added  successfully')
        return HttpResponseRedirect('/car_list/')
    
    else:
        return render(request,'admin_page/car/add_car.html')

def edit_car(request,id):
    if request.method == 'POST':
        cname= request.POST["cname"]
        Fuel= request.POST["fuel"]
        Seats= request.POST["seats"]
        Mileage= request.POST["mileage"]
        Luggage= request.POST["luggage"]
        rentprice= request.POST["rp"]
        Exp= request.POST["exp"]
        City= request.POST["city"]
        Features= request.POST["features"]
        Description= request.POST["descripton"]
        car_details.objects.filter(id=id).update(name=cname,fuel=Fuel,seats=Seats,mileage=Mileage,luggage=Luggage,
        rent_amount=rentprice,city=City,features=Features,addedat=Exp,descripton=Description)
        messages.success(request,'Car "'+cname+'"updated  successfully')
        return HttpResponseRedirect('/car_list/')
    else:
        data=car_details.objects.get(id=id)
        context={
            'data':data
        }
        return render(request,'admin_page/car/edit_car.html',context)
def delete_car(request, id):
    car_data = car_details.objects.filter(id = id).first()
    dt=car_booking.objects.filter(car_name=car_data.name).exists()
    if dt:
        messages.error(request,'Car assined to customer it can not be deleted')
        return redirect('car_list')
    car_data.delete()
    messages.success(request,'Car deleted successfully')
    return redirect('car_list')

# def customer_register(request):
#     if request.method =='GET':
#         return render(request,'customer/customer_register.html')
#     elif request.method =='POST':   
#         r_Fname = request.POST['fname']
#         r_email = request.POST['email']
#         r_mobile = request.POST['mobile']
#         r_uname = request.POST['uname']
#         r_pass = request.POST['pwd']
#         r_role = "customer"
#         if subscriber.objects.filter(username=r_uname).exists():
#             messages.warning(request,'Username "'+ r_uname +'" already exists')
#             return redirect('customer_register')
#         url='https://6q62os1gvd.execute-api.ap-south-1.amazonaws.com/v1/provision'
#         headers = {'content-type':'application/json'}
#         data = {
#             'FullName':r_Fname,
#             'email':r_email,
#             'mobile':r_mobile,
#             'username':r_uname,
#             'password':r_pass,
#             'role':r_role
#             }
#         r = requests.post(url, data = json.dumps(data), headers=headers)
#         if r.status_code ==200:
#           messages.success(request, 'User Registered Successfully')
#           return HttpResponseRedirect('/')
#         else:
#           messages.warning(request,'User Alredy Exits')
#           return HttpResponseRedirect('/customer_register/')
#     else:
#         messages.warning(request,'Method not found')
#         return HttpResponseRedirect('/')
        





# def login_success(request):
#     if request.method == 'POST':
#         request.session['username'] = request.POST['username']
#         passwd = request.POST['password']
#         username=request.session['username']
#         url='https://6q62os1gvd.execute-api.ap-south-1.amazonaws.com/v1/login' 
#         headers = {'content-type':'application/json'}
#         data = {"username": username, "password": passwd} 
#         r = requests.post(url, data=json.dumps(data), headers=headers)
#         if r.status_code == 200:
#             api_request = json.loads(r.content)
#             request.session['role'] = api_request['role']
#             request.session['email'] = api_request['email']
#             request.session['mobile'] = api_request['mobile']
#             request.session['FullName'] = api_request['FullName']
#             role=request.session['role']
#             if role == "admin":
#                 return redirect('/dashboard/')
#             else:
#                 return redirect('/home/')    
#         else:
#             messages.error(request,'Invalid User name or Password')
#             return HttpResponseRedirect('/')

#     else:
#         messages.error(request,'method not found')
#         return HttpResponseRedirect('/')


def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']      
        cno = request.POST['cno']
        Sub = request.POST['subject']
        Message = request.POST['message']
        url = 'https://34yc2s360a.execute-api.ap-south-1.amazonaws.com/v1/contactus'
        headers = {'content-type':'application/json'}
        data = {
            'name':name,
            'email':email,
            'contact':cno,
            'subject':Sub,
            'message':Message
            }
        r = requests.post(url, data = json.dumps(data), headers=headers)
        if r.status_code ==200:
          messages.success(request, 'Your message sent successfully ')
          return HttpResponseRedirect('/home/')
        #   return HttpResponseRedirect('/contactussuccess')
        else:
          messages.warning(request,'Sorry, Unable to submit your request, if urgent please call me.')
          return HttpResponseRedirect('/contact/')
    else:
        username = request.session['username']
        context={
            'username':username
        }
        return render(request,'contact.html',context)
       

def contact_list(request):
    url="https://o3ca3ecl1g.execute-api.us-east-1.amazonaws.com/v1/contactform"
    headers = {'content-type':'application/json'}
    r = requests.get(url,headers=headers)
    api_request = json.loads(r.content)
    if r.status_code == 200:
        return render(request, 'admin_page/contact_list.html', {"data":api_request})
    else:
        return render(request, 'admin_page/contact_list.html')