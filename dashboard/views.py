from django.shortcuts import render, redirect

# Create your views here.
import boto3
from boto3.dynamodb.conditions import Attr


user={}
dynamodb = boto3.resource('dynamodb')


def dashboard(request):
    global user
    global dynamodb
    #user = dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1})
    #user = json.dumps(dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1}))

    #print(user)

    return render(request, 'portal/dashboard.html', {'user': user})
    #return HttpResponse("Hello, world. You're at the dashboard index.")

def resident_register(request):
    if request.method == "POST":
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
            Key={
                'renter_id': email,
                # 'property_id': apartment_number
            }
        )
        item = response['Item']
        print(item)
        return redirect("userpage")

def reslogin(request):
    # template = loader.get_template('./login.html')
    if request.method == 'POST':
        email = request.POST['resemail']
        password = request.POST['psw']
        table = dynamodb.Table('Renter')
        scanattributes = table.scan(
            FilterExpression=Attr('renter_id').eq(email) & Attr('password').eq(password)
        )
        items = scanattributes['Items']
        print(items)
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            response = table.get_item(
                Key={
                    'renter_id': email,
                }
            )
        item = response['Item']
        print(item['username'])
        # return redirect("userpage")
        return render(request, "portal/userpage.html", {'content': item['username']})

def employee_register(request):
    if request.method == "POST":
        ename = request.POST['ename']
        pswdd = request.POST['pswdd']
        emailid = request.POST['emailid']
        phone = int(request.POST['phone'])
        table = dynamodb.Table('Employee')
        table.put_item(
            Item={
                'username': ename,
                'password': pswdd,
                'contact': phone,
                'employee_id': emailid,
            }
        )
        response = table.get_item(
            Key={
                'employee_id': emailid,
            }
        )
        item = response['Item']
        print(item)
        return redirect('userpage')

def employeelogin(request):
    if request.method == 'POST':
        email = request.POST['empemail']
        password = request.POST['psw']
        table = dynamodb.Table('Employee')
        scanattributes = table.scan(
            FilterExpression=Attr('employee_id').eq(email) & Attr('password').eq(password)
        )
        items = scanattributes['Items']
        print(items)
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            return redirect('userpage')

def userpage(request):
    return render(request, "userpage.html")

def pay(request):
    global property
    print("USER WOULD LIKE TO PAY")
    print(user)
    scanres = dynamodb.Table('Property').scan(
    FilterExpression=Attr('property_id').eq(user['property_id']))
    property = scanres['Items'][0]
    return render(request, 'portal/pay.html', {'user': user, 'property': property})

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