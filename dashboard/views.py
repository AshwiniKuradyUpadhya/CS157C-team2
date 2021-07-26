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

def employeedashboard(request):
    global user
    global dynamodb
    renterTable = dynamodb.Table('Renter')
    maintenanceTable = dynamodb.Table('Maintenance')
    amenitiesTable = dynamodb.Table('Amenities')
    propertyTable = dynamodb.Table('Property')
    scanAllRenter = renterTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    scanAllRenter.get('Items')
    scanUnpaidRenter = renterTable.scan(
        FilterExpression=Attr('paid').eq("false")
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    scanMaintenanceRequest = maintenanceTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    updateFixedMaintenance = maintenanceTable.update_item(
        Key={
            'property_id': propid,
            'renter_id': resid
        },
        UpdateExpression = "set maintainence_fixed = true"
    )
    scanAmenities = amenitiesTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )

    scanProperty = propertyTable.scan(
         #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )

    # unoccupied properties
    scanUnoccupiedProp = propertyTable.scan(
        FilterExpression=Attr('property_availability').eq('true')
    )

    updateRentAmount = propertyTable.update_item(
        Key={
            'property_id': propid
        },
        UpdateExpression = "set rent " + rentamount
    )


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
    global user
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
        user = response['Item']
        # return redirect("userpage")
        return render(request, "portal/userpage.html", {'user': user})

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
    global user
    if request.method == 'POST':
        email = request.POST['empemail']
        password = request.POST['psw']
        table = dynamodb.Table('Employee')
        scanattributes = table.scan(
            FilterExpression=Attr('employee_id').eq(email) & Attr('password').eq(password)
        )
        items = scanattributes['Items']
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            user = items[0]
            print(user)
            return redirect('employeepage')
            #return render(request, 'portal/employeepage.html', {'user':user})

def userpage(request):
    return render(request, "userpage.html")

def employeepage(request):
    global user
    global dynamodb
    renterTable = dynamodb.Table('Renter')
    maintenanceTable = dynamodb.Table('Maintenance')
    amenitiesTable = dynamodb.Table('Amenities')
    propertyTable = dynamodb.Table('Property')
    scanAllRenter = renterTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    renters = scanAllRenter.get('Items')
    scanMaintenanceRequest = maintenanceTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    maintenance = scanMaintenanceRequest.get('Items')
    scanProperty = propertyTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    properties = scanProperty.get('Items')
    
    for r in renters:
        for p in properties:
            if r['property_id'] == p['property_id']:
                r['rent'] = p['rent']

    if('del_maint' in request.POST):
        print("RESOLVED CLICKED RESOLVE CLICKED")
        print(request.POST['property_id'])
        print(request.POST['renter_id'])
        print(request.POST['req_desc'])
        print(request.POST['urgency'])
        # ADD DYNAMODB DELETE WITH PROPERTY_ID and RENTER_ID

    return render(request, "employeepage.html", {'user':user, 'renters': renters, 'maintenance': maintenance})

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

def maintenance_redirect(request):
    return render(request, 'portal/maintenance.html',{'user': user})

def maintenance(request):
    global user
    global maintenance
    print(user['username'])
    if request.method == 'POST':
        aptnum = int(request.POST['apartmentnum'])
        description = request.POST['request']
        urgency = request.POST['select']
        table = dynamodb.Table('Maintenance')
        table.put_item(
            Item={
                'property_id': aptnum,
                'renter_id': user['renter_id'],
                'request_description': description,
                'urgency': urgency,
            }
        )
        response = table.get_item(
            Key={
                'renter_id': "resident1",
                'property_id': aptnum,
            }
        )
        item = response['Item']
        print(item)
        return render(request, 'userpage.html',{'user': user})

def important_numbers(request):
    return render(request, 'portal/important_numbers.html', {'user': user})


def floorplans(request):
    return render(request, 'portal/floorplans.html')

def gallery(request):
    return render(request, 'portal/gallery.html')

def faq(request):
    return render(request, 'portal/FAQ.html')

def amenities(request):
    return render(request, 'portal/amenities.html')
    
def index(request):
    return render(request, "index.html")