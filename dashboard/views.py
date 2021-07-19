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

def reslogin(request):
    # template = loader.get_template('./login.html')
    if request.method == 'POST':
        email = request.POST['emailid']
        apartment_number = int(request.POST['aptnumber'])
        password = request.POST['psw']
        table = dynamodb.Table('Renter')
        scankeyemail = table.query(
            KeyConditionExpression = Key('renter_id').eq(request.POST['emailid'])
        )
        items = scankeyemail['Items']
        print(items)
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            return redirect('userpage')

def register(request):
    if request.method =="POST":
        username = request.POST['uname']
        apartment_number = int(request.POST['aptnum'])
        password = request.POST['psw']
        email = request.POST['email']
        contact = request.POST['contact']
        table = dynamodb.Table('Renter')
        table.put_item(
            Item={
                'username': username,
                'renter_id': email,
                'property_id': apartment_number,
                'password': password,
                'contact': contact,
            }
        )
        response = table.get_item(
            Key = {
                'renter_id': email,
                'property_id': apartment_number
            }
        )
        item = response['Item']
        print(item)
        return redirect("userpage")

def userpage(request):
    return render(request, "userpage.html")

def pay(request):
    print("USER WOULD LIKE TO PAY")
    print(user)
    return render(request, 'portal/pay.html', {'user': user})

def info(request):
    return render(request, 'portal/info.html')

def maintenance(request):
    return render(request, 'portal/maintenance.html')

def floorplans(request):
    return render(request, 'portal/floorplans.html')

def gallery(request):
    return render(request, 'portal/gallery.html')

def faq(request):
    return render(request, 'portal/faq.html')

def amenities(request):
    return render(request, 'portal/amenities.html')
    
def index(request):
    return render(request, "index.html")
    # global user
    # if request.method == 'POST':
    #     uname = request.POST['uname']
    #     psw = request.POST['psw']
    #     print(request.POST['uname'])
    #     print(request.POST['psw'])
    #     scanres = dynamodb.Table('Renter').scan(
    #         FilterExpression=Attr('renter_username').eq(uname) & Attr('renter_password').eq(psw)
    #         )
    #     if len(scanres['Items']) == 0:
    #         # reload page if login fail, add fail message later
    #         return render(request, 'portal/index.html')
    #     else:
    #         #expect only one user & password pair so index [0] for user.
    #         user = scanres['Items'][0]
    #         print(user)
    #         return redirect('/portal')
    # else:
    #     return render(request, 'portal/index.html')