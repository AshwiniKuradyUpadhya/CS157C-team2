from django.shortcuts import render, redirect
from django.template import loader

# Create your views here.
import boto3

# Create your views here.
from django.http import HttpResponse, JsonResponse
import simplejson as json

user = {}

def dashboard(request):
    global user
    dynamodb = boto3.resource('dynamodb')
    user = dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1})
    #user = json.dumps(dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1}))

    #print(user)

    return render(request, 'portal/dashboard.html', {'user': user})
    #return HttpResponse("Hello, world. You're at the dashboard index.")

def login(request):
    # template = loader.get_template('./login.html')
    context = {}
    if request.method == 'POST':
        print(request.POST['uname'])
        print(request.POST['psw'])
        return redirect('/portal')
    else:
        return render(request, 'login/login.html', context)

def pay(request):
    print("USER WOULD LIKE TO PAY")
    print(user)
    return render(request, 'portal/pay.html', {'user': user})
    
def maintanence(request):
    return render(request, 'portal/maintanence.html')

def info(request):
    return render(request, 'portal/info.html')

def index(request):
    if request.method == 'POST':
        print(request.POST['uname'])
        print(request.POST['psw'])
        return redirect('/portal')
    else:
        return render(request, 'portal/index.html')