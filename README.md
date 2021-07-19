# CS157C-team2

## Info
AWS CLI installed with aws configuration for dynamoDB webservices.

By creating a Django project, Django creates a config directory for the project called "residential portal" which consists of files such as "_init_.py", "asgi.py", "settings.py", "urls.py", "wsgi.py"

We created an app directory called "dashboard" which consists of all files required for the main application of our project such as "_init_.py", "admins.py", "apps.py", "models.py", "tests.py", "urls.py" and "view.py"

dashboard/template/portal is where the .html files go. (Need to update img srcs with the django templating syntax)
As of now, created .html files are as below:

amenities.html
dashboard.html
faq.html
floorplans.html
gallery.html
index.html
info.html
login.html(not in use as of now)
maintenance.html
pay.html
request.html(copy of maintenance page -  not in use as of now)
style.css( not in use - as of now)
userpage.html


static/images/ is where images go. Syntax for images in .html is {% static '............' %} ex:
```
<img src="{% static 'images/homemarquee4.png' %}" alt="first" style="width:100%;">
```

Also need {% load static %} in .html document. Check out index.html for example.

dashboard/views.py is where we load the different views with any backend functions.

dashboard/urls.py is where we add our different paths.

Connection usually follow the below path for the home page:

residential portal/urls.py -> dashboard/urls.py -> 'index/' gets accessed from dashboard/views.py -> request is passed to "index.html"(home page)

Start server on "localhost:8000" using 

```
python manage.py runserver

```

On browser -> go to path "localhost:8000/index/" [as of now 'index.html' is a home page]


## Current Progress:

Created a table called Renter in DYnamoDB using Boto3 with render_id[Email ID] as Hash primary key and property_id[apartment_number] as Range primary key

dashboard/views.py : added few more functions:
			"register" function gets executed when user click on "register" button on the home page, with successful registeration -> redirected to userpage.html
			"reslogin" function gets executed when user clicks on "resident login" button in home page, with successful login --> redirected to userpage.html

User data is added to the table "Renter" when user clicks on "register" button and then redirects to userpage.html
User data gets verified from the table "Renter" when user try to login through "reslogin" button and then redirects to userpage.html
