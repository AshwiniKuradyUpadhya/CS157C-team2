from django.shortcuts import render, redirect
from django.template import loader

# Create your views here.
import boto3
from boto3.dynamodb.conditions import Key, Attr

from django.http import HttpResponse, JsonResponse
import simplejson as json

user = {}
dynamodb = boto3.resource('dynamodb')


def dashboard(request):
    global user
    global dynamodb
    #user = dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1})
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
    global user
    if request.method == 'POST':
        uname = request.POST['uname']
        psw = request.POST['psw']
        print(request.POST['uname'])
        print(request.POST['psw'])
        scanres = dynamodb.Table('Renter').scan(
            FilterExpression=Attr('renter_username').eq(uname) & Attr('renter_password').eq(psw)
            )
        if len(scanres['Items']) == 0:
            # reload page if login fail, add fail message later
            return render(request, 'portal/index.html')
        else: 
            #expect only one user & password pair so index [0] for user.
            user = scanres['Items'][0]
            print(user)
            return redirect('/portal')
    else:
        return render(request, 'portal/index.html')