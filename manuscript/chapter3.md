# Django Basics {#chapter-django-basics}
Let's get started with Django! In this chapter, we'll be giving you an overview of the creation process. You'll be setting up a new project and a new Web application. By the end of this chapter, you will have a simple Django powered website up and running!

## Testing Your Setup

Let's start by checking that your Python and Django installations are correct for this tutorial. To do this, open a new terminal window and issue the following command, which tells you what Python version you have.

{lang="text",linenos=off}
	$ python --version

The response should be something like `2.7.11` or `3.5.1`, but any 2.7.5+ or 3.4+ versions of Python should work fine. If you need to upgrade or install Python go to the chapter on [setting up your system](#chapter-system-setup). 

If you are using a virtual environment, then ensure that you have activated it - if you don't remember how go back to our chapter on [virtual environments](#chapter-virtual-environments).

After verifying your Python installation, check your Django installation. In your terminal window, run the Python interpreter by issuing the following command.

{lang="text",linenos=off}    
    $ python 
	Python 2.7.10 (default, Jul 14 2015, 19:46:27) 
	[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>>
	

At the prompt, enter the following commands:

{lang="text",linenos=off}
	>>> import django
	>>> django.get_version()
	'1.9.10'
	>>> exit()


All going well you should see the correct version of Django, and then can use `exit()` to leave the Python interpreter. If `import django` fails to import, then check that you are in your virtual environment, and check what packages are installed with `pip list` at the terminal window. 

If you have problems with installing the packages or have a different version installed, go to [System Setup](#chapter-system-setup) chapter or consult the [Django Documentation on Installing
Django](https://docs.djangoproject.com/en/1.9/topics/install/).


I> ### Prompts
I> In this book, there's two things you should look out for when we include code snippets.
I>
I> Snippets beginning with a dollar sign (`$`) indicates that the remainder of the following line is a terminal or Command Prompt command.
I>
I> Whenever you see `>>>`, the following is a command that should be entered into the interactive Python interpreter. This is launched by issuing `$ python`. See what we did there? You can also exit the Python interpreter by entering `quit()`.

## Creating Your Django Project
To create a new Django Project, go to your `workspace` directory, and issue the following command:

{lang="text",linenos=off}
	$ django-admin.py startproject tango_with_django_project

If you don't have a `workspace` directory, then create one, so that you can house your Django projects and other code projects within this directory. We will refer to your `workspace` directory in the code as `<workspace>`. You will have to substitute in the path to your `workspace` directory, for example: `/Users/leifos/Code/` or `/Users/maxwelld90/Workspace/`.

I> ### Can't find `django-admin.py`?
I> Try entering `django-admin` instead. Depending on your setup, some systems may not recognise `django-admin.py`.
I> 
I> While, on Windows, you may have to use the full path to the `django-admin.py` script, for example:
I>
I> {lang="text",linenos=off}
I> 	python c:\python27\scripts\django-admin.py 
I> 	       startproject tango_with_django_project
I>
I> as suggested on [StackOverflow](http://stackoverflow.com/questions/8112630/cant-create-django-project-using-command-prompt).

This command will invoke the `django-admin.py` script, which will set up a new Django project called `tango_with_django_project` for you. Typically, we append `_project` to the end of our Django project directories so we know exactly what they contain - but the naming convention is entirely up to you.

You'll now notice within your workspace is a directory set to the name of your new project, `tango_with_django_project`. Within this newly created directory, you should see two items:

-   another directory with the same name as your project, `tango_with_django_project`; and
-   a Python script called `manage.py`.

For the purposes of this tutorial, we call this nested directory called `tango_with_django_project` the *project configuration directory*. Within this directory, you will find four Python scripts. We will discuss these scripts in detail later on, but for now you should see:

-   `__init__.py`, a blank Python script whose presence indicates to the Python interpreter that the directory is a Python package;
-   `settings.py`, the place to store all of your Django project's settings;
-   `urls.py`, a Python script to store URL patterns for your project; and
-   `wsgi.py`, a Python script used to help run your development server and deploy your project to a production environment.

In the project directory, you will see there is a file called `manage.py`. We will be calling this script time and time again as we develop our project. It provides you with a series of commands you can run to maintain your Django project. For example, `manage.py` allows you to run the built-in Django development server, test your application and run various database commands. We will be using the script for virtually every Django command we want to run.

I> ### The Django Admin and Manage Scripts
I> For Further Information on Django admin script, see the Django documentation for more details about the  [Admin and Manage scripts](https://docs.djangoproject.com/en/1.9/ref/django-admin/#django-admin-py-and-manage-py).
I>
I> Note that if you run `python manage.py help` you can see the list of commands available.

You can try using the `manage.py` script now, by issuing the following command.

`$ python manage.py runserver`

Executing this command will launch Python, and instruct Django to initiate its lightweight development server. You should see the output in your terminal window similar to the example shown below:

{lang="text",linenos=off}
    $ python manage.py runserver
	
	Performing system checks...

	System check identified no issues (0 silenced).

	You have unapplied migrations; your app may 
	not work properly until they are applied.

	Run 'python manage.py migrate' to apply them.

	October 2, 2016 - 21:45:32
	Django version 1.9.10, using settings 'tango_with_django_project.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.


In the output you can see a number of things. First, there are no issues that stop the application from running. Second, however, you will notice that a warning is raised, i.e. unapplied migrations. We will talk about this in more detail when we setup our database, but for now we can ignore it. Third, and most importantly, you can see that a URL has been specified: `http://127.0.0.1:8000/`, which is the address of the Django development webserver.
   

Now open up your Web browser and enter the URL [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/). You should see a webpage similar to the one shown in below.

{id="img-ch3-django-powered-page"}
![A screenshot of the initial Django page you will see when running the development server for the first time.](images/ch3-django-powered-page.png)

You can stop the development server at anytime by pushing `CTRL + C` in your terminal or Command Prompt window. If you wish to run the development server on a different port, or allow users from other machines to access it, you can do so by supplying optional arguments. Consider the following command:

{lang="text",linenos=off}
	$ python manage.py runserver <your_machines_ip_address>:5555

Executing this command will force the development server to respond to incoming requests on TCP port `5555`. You will need to replace `<your_machines_ip_address>` with your computer's IP address or `127.0.0.1`. 

I> ### Don't know your IP Address?
I> If you use `0.0.0.0`, Django figures out what your IP address is. Go ahead and try:
I>
I> `python manage.py runserver 0.0.0.0:5555`

When setting ports, it is unlikely that you will be able to use TCP port 80 or 8080 as these are traditionally reserved for HTTP traffic. Also, any port below 1024 is considered to be [privileged](http://www.w3.org/Daemon/User/Installation/PrivilegedPorts.html) by your operating system. 

While you won't be using the lightweight development server to deploy your application, it's nice to be able to demo your application on another machine in your network. Running the server with your machine's IP address will enable others to enter in `http://<your_machines_ip_address>:<port>/` and view your Web application. Of course, this will depend on how your network is configured. There may be proxy servers or firewalls in the way that would need to be configured before this would work. Check with the administrator of the network you are using if you can't view the development server remotely.

## Creating a Django App
A Django project is a collection of *configurations* and *apps* that together make up a given Web application or website. One of the intended outcomes of using this approach is to promote good software engineering practices. By developing a series of small applications, the idea is that you can theoretically drop an existing application into a different Django project and have it working with minimal effort. 

A Django application exists to perform a particular task. You need to create specific apps that are responsible for providing your site with particular kinds of functionality. For example, we could imagine that a project might consist of several apps including a polling app, a registration app, and a specific content related app. In another project, we may wish to re-use the polling and registration apps, and so can include them in other projects. We will talk about this later. For now we are going to create the app for the *Rango* app.

To do this, from within your Django project directory (e.g. `<workspace>/tango_with_django_project`), run the following command.

{lang="text",linenos=off}
    $ python manage.py startapp rango

The `startapp` command creates a new directory within your project's root. Unsurprisingly, this directory is called `rango` - and contained within it are a number of Python scripts:

- another `__init__.py`, serving the exact same purpose as discussed previously;
- `admin.py`, where you can register your models so that you can benefit from some Django machinery which creates an admin interface for you;
- `apps.py`, that provides a place for any app specific configuration; 
- `models.py`, a place to store your app's data models - where you specify the entities and relationships between data;
- `tests.py`, where you can store a series of functions to test your app's code; 
- `views.py`, where you can store a series of functions that handle requests and return responses; and
- `migrations` directory, which stores database specific information related to your models.
    

`views.py` and `models.py` are the two files you will use for any given app, and form part of the main architectural design pattern employed by Django, i.e. the *Model-View-Template* pattern. You can check out [the official Django documentation](https://docs.djangoproject.com/en/1.9/intro/overview/) to see how models, views and templates relate to each other in more detail.

Before you can get started with creating your own models and views, you must first tell your Django project about your new app's existence. To do this, you need to modify the `settings.py` file, contained within your project's configuration directory. Open the file and find the `INSTALLED_APPS` tuple. Add the `rango` app to the end of the tuple, which should then look like the following example.

{lang="python",linenos=off}
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'rango',
	]

Verify that Django picked up your new app by running the development server again. If you can start the server without errors, your app was picked up and you will be ready to proceed to the next step.

I> ### `startapp` Magic
I>
I> When creating a new app with the `python manage.py startapp` command, Django may add the new app's name to your `settings.py` `INSTALLED_APPS` list automatically for you. It's nevertheless good practice to check everything is setup correctly before you proceed.

## Creating a View
With our Rango app created, let's now create a simple view. For our first view, let's just send some text back to the client - we won't concern ourselves about using models or templates just yet.

In your favourite IDE, open the file `views.py`, located within your newly created `rango` app directory. Remove the comment `# Create your views here.` so that you now have a blank file.

You can now add in the following code.

{lang="python",linenos=off}
	from django.http import HttpResponse
	
	def index(request):
	    return HttpResponse("Rango says hey there partner!")

Breaking down the three lines of code, we observe the following points about creating this simple view.

-   We first import the [`HttpResponse`](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpResponse) object from the `django.http` module.
-   Each view exists within the `views.py` file as a series of individual functions. In this instance, we only created one view - called `index`.
-   Each view takes in at least one argument - a [`HttpRequest`](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest) object, which also lives in the `django.http` module. Convention dictates that this is named `request`, but you can rename this to whatever you want if you so desire.
-   Each view must return a `HttpResponse` object. A simple `HttpResponse` object takes a string parameter representing the content of the page we wish to send to the client requesting the view.

With the view created, you're only part of the way to allowing a user to access it. For a user to see your view, you must map a [Uniform Resource Locator (URL)](http://en.wikipedia.org/wiki/Uniform_resource_locator) to the view.

To create an initial mapping, open `urls.py` located in your project directory and add the following lines of code to the `urlpatterns`:

{lang="python", linenos=off}
	from rango import views
	
	urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^admin/', admin.site.urls),
	]

This maps the basic URL to the `index` view in the `rango` app. Run the development server (e.g. `python manage.py runserver`) and visit `http://127.0.0.1:8000` or whatever address your development server is running on. You'll then see the rendered output of the `index` view.

## Mapping URLs
Rather than directly mapping URLs from the project to the app, we can make our app more modular (and thus re-usable) by changing how we route the incoming URL to a view. To do this, we first need to modify the project's `urls.py` and have it point to the app to handle any specific Rango app requests. We then need to specify how Rango deals with such requests.

First, open the project's `urls.py` file which is located inside your project configuration directory. As a relative path from your workspace directory, this would be the file `<workspace>/tango_with_django_project/tango_with_django_project/urls.py`. Update the `urlpatterns` list as shown in the example below.

{lang="python",linenos=off}
	from django.conf.urls import url
	from django.contrib import admin
	from django.conf.urls import include 
	from rango import views
	
	urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^rango/', include('rango.urls')),
	    # above maps any URLs starting 
	    # with rango/ to be handled by
	    # the rango application
	    url(r'^admin/', admin.site.urls),
	]


You will see that the `urlpatterns` is a Python list, which is expected by the Django framework.  The added mapping looks for URL strings that match the patterns `^rango/`. When a match is made the remainder of the URL string is then passed onto and handled by `rango.urls` through the use of the  `include()` function from within `django.conf.urls`.  

Think of this as a chain that processes the URL string - as illustrated in the [URL chain figure](#fig-url-chain). In this chain, the domain is stripped out and the remainder of the URL string (`rango/`) is passed on to `tango_with_django` project, where it finds a match and strips away `rango/`, leaving an empty string to be passed on to the app `rango` for it to handle.

Consequently, we need to create a new file called `urls.py` in the `rango` app directory, to handle the remaining URL string (and map the empty string to the `index` view):

{lang="python",linenos=off}
	from django.conf.urls import url
	from rango import views
	
	urlpatterns = [
	    url(r'^$', views.index, name='index'),
	]

This code imports the relevant Django machinery for URL mappings and the `views` module from `rango`. This allows us to call the function `url` and point to the `index` view for the mapping in `urlpatterns`. 

When we talk about URL strings, we assume that the host portion of a given URL has *already been stripped away*. The host portion of a URL denotes the host address or domain name that maps to the webserver, such as `http://127.0.0.1:8000` or `http://www.tangowithdjango.com`. Stripping the host portion away means that the Django machinery needs to only handle the remainder of the URL string. For example, given the URL `http://127.0.0.1:8000/rango/about/`, Django would have a URL string of `/rango/about/`.

The URL mapping we have created above calls Django's `url()` function, where the first parameter is the regular expression `^$`, which matches to an empty string because `^` denotes starts with, while `$` denotes ends with. As there is nothing in between these characters then it only matches an empty string.  Any URL string supplied by the user that matches this pattern means that the view `views.index()` would be invoked by Django. You might be thinking that matching a blank URL is pretty pointless - what use would it serve? Remember that when the URL pattern matching takes place, only a portion of the original URL string is considered. This is because Django will first process the URL patterns in the project processing the original URL string (i.e. `rango/`) and strip away the `rango/` part. Django will then pass on an empty string to the Rango app to handle via the URL patterns in `rango/urls.py`.

The next parameter passed to the `url()` function is the `index` view, which will handle the incoming requests, followed by the optional parameter, `name` that is set to a string `'index'`. By naming our URL mappings we can employ *reverse URL matching* later on. That is we can reference the URL mapping by name rather than by the URL. Later we will explain how to use this when creating templates. But do check out [the Official Django documentation on this topic](https://docs.djangoproject.com/en/1.9/topics/http/urls/#naming-url-patterns) for more information.

Now, restart the Django development server and visit `http://127.0.0.1:8000/rango/`. If all went well, you should see the text `Rango says hey there partner!`. It should look just like the screenshot shown below.

{id="fig-url-chain"}
![An illustration of a URL, represented as a chain, showing how different parts of the URL following the domain are the responsibility of different `url.py` files.](images/ch3-url-chain.png)


{id="fig-ch3-hey-there"}
![A screenshot of a Web browser displaying our first Django powered webpage. Hello, Rango!](images/ch3-hey-there.png)

Within each app, you will create a number of URL mappings. The initial mapping is quite simple, but as we progress through the book we will create more sophisticated, parameterised URL mappings. 

It's also important to have a good understanding of how URLs are handled in Django. It may seem a bit confusing right now, but as we progress through the book, we will be creating more and more URL mappings, so you'll soon be a pro. To find out more about them, check out the [official Django documentation on URLs](https://docs.djangoproject.com/en/1.9/topics/http/urls/) for further details and further examples.

I> ###Note on Regular Expressions
I> Django URL patterns use [regular expressions](http://en.wikipedia.org/wiki/Regular_expression) to perform the matching. It is worthwhile familiarising yourself on how to use regular expressions in Python. The official Python documentation contains a [useful guide on regular expressions](http://docs.python.org/2/howto/regex.html), while `regexcheatsheet.com` provides a [neat summary of regular expressions](http://regexcheatsheet.com/).

If you are using version control, now is a good time to commit the changes you have made to your workspace. Refer to the [chapter providing a crash course on Git](#chapter-git) if you can't remember the commands and steps involved in doing this.

## Basic Workflows

What you've just learnt in this chapter can be succinctly summarised into a list of actions. Here, we provide these lists for the two distinct tasks you have performed. You can use this section for a quick reference if you need to remind yourself about particular actions later on.

### Creating a new Django Project

1.  To create the project run, `python django-admin.py startproject <name>`, where `<name>` is the name of the project you wish to create.

### Creating a new Django App

1.  To create a new app, run `$ python manage.py startapp <appname>`, where `<appname>` is the name of the app you wish to create.
2.  Tell your Django project about the new app by adding it to the `INSTALLED_APPS` tuple in your project's `settings.py` file.
3.  In your project `urls.py` file, add a mapping to the app.
4.  In your app's directory, create a `urls.py` file to direct incoming URL strings to views.
5.  In your app's `view.py`, create the required views ensuring that they return a `HttpResponse` object.

X>###Exercises
X>
X> Now that you have got Django and your new app up and running, give the following exercises a go to reinforce what you've learnt. Getting to this stage is a significant landmark in working with Django. Creating views and mapping URLs to views is the first step towards developing more complex and usable Web applications.
X> 
X> - Revise the procedure and make sure you follow how the URLs are mapped to views.
X> - Create a new view method called `about` which returns the following `HttpResponse`: `'Rango says here is the about page.'`
X> - Map this view to `/rango/about/`. For this step, you'll only need to edit the `urls.py` of the Rango app. Remember the `/rango/` part is handled by the projects `urls.py`.
X> - Revise the `HttpResponse` in the `index` view to include a link to the about page.
X> - In the `HttpResponse` in the `about` view include a link back to the main page.
X> - Now that you have started the book, follow us on Twitter [@tangowithdjango](https://twitter.com/tangowithdjango), and let us know how you are getting on!

I> ### Hints
I> If you're struggling to get the exercises done, the following hints will
I> hopefully provide you with some inspiration on how to progress.
I> 
I> - In your `views.py`, create a function called: `def about(request):`, and have the function return a HttpResponse(), insert your HTML inside this response.
I> - The regular expression to match `about/` is `r'^about/'` - so in `rango/urls.py` add in a new mapping to the `about()` view.
I> - Update your `index()` view to include a link to the `about` view. Keep it simple for now - something like `Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>`. 
I> - Also add the HTML to link back to the index page is into your response from the `about()` view `<a href="/rango/">Index</a>`.
I>
I> - If you haven't done so already, now's a good time to head off and complete part one of the official [Django Tutorial](https://docs.djangoproject.com/en/1.9/intro/tutorial01/).
