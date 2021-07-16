# CS157C-team2

## Info
AWS CLI installed with aws configuration for dynamoDB webservices.

dashboard/ is where the main application is.

dashboard/template/ is where the .html files go. (Need to update img srcs with the django templating syntax) 

static/images/ is where images go. Syntax for images in .html is {% static '............' %} ex:
```
<img src="{% static 'images/homemarquee4.png' %}" alt="first" style="width:100%;">
```

Also need {% load static %} in .html document. Check out index.html for example.

dashboard/views.py is where we load the different views with any backend functions.

dashboard/urls.py is where we add our different paths.


Start server on localhost:8000
```
python manage.py runserver
```