# Deploying Your Project {#chapter-deploy}
This chapter provides a step-by-step guide on how to deploy your Django application on  [PythonAnywhere](https://www.pythonanywhere.com/?affiliate_id=000116e3), which is an online IDE and web hosting service. The service provides in-browser access to the server-based Python and Bash command line interfaces, meaning you can interact with PythonAnywhere's servers just like you would with a regular terminal instance on your own computer. Currently, PythonAnywhere are offering a free beginner account, which is perfect to get started. It provides you up with an adequate amount of storage space and CPU time to get one Django application up and running.

I> ### Go Git It!
I> You can do this chapter independently as we have already implemented Rango and it is available from GitHub. If you haven't used Git/GitHub before, you can check out our [chapter on using Git](#chapter-git)).

## Creating a PythonAnywhere Account
First, [sign up for a Beginner PythonAnywhere account](https://www.pythonanywhere.com/?affiliate_id=000116e3) and take the seven step tour to get familar with the PythonAnywhere interface. If your application takes off and becomes popular, you can always upgrade your account at a later stage to gain more storage space and CPU time along with a number of other benefits - such as hosting specific domains and SSH abilities, for example.

Once your account has been created, and you have confirmed your email, you will have your own little slice of the World Wide Web at `http://<username>.pythonanywhere.com`, where `<username>` is your PythonAnywhere username. It is from this URL that your hosted application will be available.

## The PythonAnywhere Web Interface
The PythonAnywhere web interface contains a *dashboard* which in turn provides a series of different components allowing you to manage your application. The components as [illustrated in the figure below](#pa-interface) include:

- *Consoles*, allowing you to create and interact with Python and Bash console instances;
- *Files*, which allows you to upload to and organise files within your disk quota; and
- *Web Apps*, allowing you to configure settings for your hosted web application;

Other components exist, such as *Notebooks*, but we won't be using them here -- we'll be working primarily with the *consoles* and *web* components. The [PythonAnywhere Wiki](https://www.pythonanywhere.com/wiki/) provides a series of detailed explanations on how to use the other components if you are interested in finding out more.

{#pa-interface}
![The PythonAnywhere dashboard, showing the main components you can use.](images/ch-deploy-pa-interface.png)

## Creating a Virtual Environment
As part of its standard default Bash environment, PythonAnywhere comes with Python 2.7+ and a number of pre-installed Python Packages (including *Django *). But, since we are using a different setup, we need to setup the Python 3 version, manually, through a virtual environment.

First, open a Bash console. If you run `python --version` then you will see that the native Python is 2.7+, so to create a virtual environment that uses Python 3.6+, issue the following command:

{lang="bash",linenos=off}
	11:45 ~ $ mkvirtualenv --python=python3.6 rango
	Running virtualenv with interpreter /usr/bin/python3.6
	New python executable in /home/<username>/.virtualenvs/rango/bin/python3.6
	Also creating executable in /home/<username>/.virtualenvs/rango/bin/python
	Installing setuptools, pip, wheel...done.
	virtualenvwrapper creating /home/<username>/.virtualenvs/.../predeactivate
	virtualenvwrapper creating /home/<username>/.virtualenvs/.../postdeactivate
	virtualenvwrapper creating /home/<username>/.virtualenvs/.../preactivate
	virtualenvwrapper creating /home/<username>/.virtualenvs/.../postactivate
	virtualenvwrapper creating /home/<username>/.virtualenvs/.../get_env_details
    
    
Above we have used Python 3.6, but you can check which version of Python you are using and use that instead. Also, note that where it shows `<username>` that will be replaced with your username. The process of creating the virtual environment will take a little while to complete, after which you will be presented with a slightly different prompt.

{lang="text",linenos=off}
	(rango) 11:45 ~ $

Note the inclusion of `(rango)` compared to the previous command prompt. This signifies that the `rango` virtual environment has been activated, so any package installations will be done within that virtual environment, leaving the wider system setup alone. If you issue the command `ls -la`, you will see that a directory called `.virtualenvs` has been created. This is the directory in which all of your virtual environments and associated packages will be stored. To confirm the setup, issue the command `which pip`. This will print the location in which the active `pip` binary is located - hopefully within `.virtualenvs` and `rango`, as shown in the example below.

{lang="text",linenos=off}    
	/home/<username>/.virtualenvs/test/bin/pip

To see what packages are already installed, enter `pip list`. Now we can customise the virtual environment by installing the required packages for our Rango application. Install all the required packages, by issuing the following commands.

{lang="text",linenos=off}    
	$ pip install -U django==2.1.5
	$ pip install pillow
	$ pip install django-registration-redux
	$ pip install bcrypt
    $ pip install requests
    

**Ensure that you replace the version of Django specified above with the one you are using for development. Here we have used verison 2.1.5, but no doubt a newer verison is available (and o). Not using the same verison as your development machine could lead to some wierd errors and exceptions - which will drive you crazy. To ensure you have the same setup, we recommend using `pip freeze > requirements.txt` on your local development machine. This will note down all the packages in your current development environment. Then on PythonAnywhere, you can run `pip install -r requirements.txt` to install all the packages in one go.

I> ### Waiting to Download...
I> Installing all theses packages may take some time, so you can relax, call a friend, or tweet about our tutorial `@tangowithdjango`!

Once installed, check if Django has been installed with the command `which django-admin.py`. You should receive output similar to the following example.

{lang="text",linenos=off}    
	/home/<username>/.virtualenvs/rango/bin/django-admin.py

I> ### Virtual Environments on PythonAnywhere
I> PythonAnywhere also provides instructions on how to setup virtual environments. [Check out their Wiki documentation for more information](https://help.pythonanywhere.com/pages/VirtualEnvForNewerDjango).

### Virtual Environment Switching
Moving between virtual environments can be done pretty easily. PythonAnywhere should have this covered for you. Below, we provide you with a quick tutorial on how to switch between virtual environments.

At your terminal, you can launch into a pre-existing virtual environment with the `workon` command. For example, to load up the `rango` environment, enter:

{lang="text",linenos=off}    
	11:48 ~ $ workon rango

where `rango` can be replaced with the name of the virtual environment you wish to use. Your prompt should then change to indicate you are working within a virtual environment. This is shown by the addition of `(rango)` to your prompt.

{lang="text",linenos=off}    
	(rango) 11:49 ~ $

You can then leave the virtual environment using the `deactivate` command. Your prompt should then be missing the `(rango)` prefix, with an example shown below.

{lang="text",linenos=off}    
	(rango) 11:49 ~ $ deactivate 
	11:51 ~ $

### Cloning your Git Repository
Now that your virtual environment for Rango is all setup, you can now clone your Git repository to obtain a copy of your project's files. Clone your repository by issuing the following command from your home directory:

{lang="text",linenos=off}    
	$ git clone https://<USERNAME>:<PASSWORD>@github.com/<OWNER>/<REPO_NAME>.git

where you replace - `<USERNAME>` with your GitHub username; - `<PASSWORD>` with your GitHub password; - `<OWNER>` with the username of the person who owns the repository; and - `<REPO_NAME>` with the name of your project's repository.

### Setting Up the Database
With your files cloned, you must then prepare your database. We'll be using the `populate_rango.py` module that we created earlier in the book. As we'll be running the module, you must ensure that you are using the `rango` virtual environment (i.e. you see `(rango)` as part of your prompt - if not, invoke `workon rango`). From your home directory, move into the `tango_with_django_19` directory, then to the `code` directory. This directory will be named after your git repository, so the name may differ. For example, if you called your repository `twd`, the directory will also be called `twd`. Depending upon how you configured your repository, you should also `cd` into the directory with `manage.py` in it - `tango_with_django_project`. Now issue the following commands.

{lang="text",linenos=off}    
	(rango) 16:55 ~/tango_with_django $ python manage.py makemigrations rango
	(rango) 16:55 ~/tango_with_django $ python manage.py migrate
	(rango) 16:56 ~/tango_with_django $ python populate_rango.py
	(rango) 16:57 ~/tango_with_django $ python manage.py createsuperuser

As discussed earlier in the book, the first command creates the migrations for the `rango` app, then the `migrate` command creates the *SQLlite3* database. Once the database is created, the database can be populated and a superuser created.

## Setting up Your Web Application
Now that the database is setup, we need to configure the PythonAnywhere [*NGINX*](https://www.nginx.com/resources/wiki/) Web server to serve up your application. From PythonAnywhere's dashboard, open up the *Web Apps* tab. On the left of the page that appears, click *Add a new web app.*

A popup box will then appear. Follow the instructions on-screen, and when the time comes, select the *manual configuration* option and complete the wizard. Make sure you select the same Python version as the one you selected earlier.

In a new tab or window in your Web browser, go visit your PythonAnywhere subdomain at the address `http://<username>.pythonanywhere.com`. You should be presented with the [default `Hello, World!` webpage, as shown below](#hello-world). This is because the WSGI script is currently serving up this page, and not your Django application. This is what we need to change next.

{#hello-world}
![The default PythonAnywhere *hello world* webpage.](images/ch-deploy-hello-world.png)

### Configure the Virtual Environment
To set the virtual environment for your app, navigate again to the *Web* tab in PythonAnywhere's interface. From there, scroll all the way down under you see the heading *Virtualenv*. 

Enter in the path to your virtual environment. Assuming you created a virtual environment called `rango` the path would be:

{lang="text",linenos=off} 
	/home/<username>/.virtualenvs/rango

You can start a console to check if it is successful. 

Now in the *Code* section, you can set the path to your web applications source code.

{lang="text",linenos=off} 
	/home/<username>/<path-to>/tango_with_django_project/
		
Note that this path should be pointing to the directory with your project's `manage.py` file within it.
If for example you cloned a repository called `tango_with_django19` into your account's home directory, the path will be something like:

{lang="text",linenos=off} 
	/home/<username>/tango_with_django_19/code/tango_with_django_project/

### Configuring the WSGI Script
The [Web Server Gateway Interface](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface), a.k.a. *WSGI* provides a simple and universal interface between Web servers and Web applications. PythonAnywhere uses WSGI to bridge the server-application link and map incoming requests to your subdomain to your web application.

To configure the WSGI script, navigate to the *Web* tab in PythonAnywhere's interface. Under the Code heading you can see a link to the WSGI configuration file in the Code section: e.g. `/var/www/<username>_pythonanywhere_com_wsgi.py`.

The people at PythonAnywhere have set up a sample WSGI file for us with several possible configurations. For your Web application, you'll need to configure the Django section of the file by clicking on the link to open a simple editor. The example below demonstrates a possible configuration for your application.

{lang="python",linenos=off}    
	import os
	import sys
	
	# Add your project's directory the PYTHONPATH
	path = '/home/<username>/<path-to>/tango_with_django_project/'
	if path not in sys.path:
	    sys.path.append(path)
	
	# Move to the project directory
	os.chdir(path)
	
	# Tell Django where the settings.py module is located
	os.environ.setdefault('DJANGO_SETTINGS_MODULE',
	                      'tango_with_django_project.settings')
		
	# Import the Django WSGI to handle any requests
	import django.core.handlers.wsgi
	application = django.core.handlers.wsgi.WSGIHandler()

Ensure that you replace `<username>` with your PythonAnywhere username, and update any other path settings to suit your application. You should also remove all other code from the WSGI configuration script to ensure no conflicts take place.

The script adds your project's directory to the `PYTHONPATH` for the Python instance that runs your web application. This allows Python to access your project's modules. If you have additional paths to add, you can easily insert them here. You can then specify the location of your project's `settings.py` module. The final step is to include the Django WSGI handler and invoke it for your application.

When you have completed the WSGI configuration, click the *Save* button at the top-right of the webpage. Before we can (re)load the application, we need to set a few security parameters (see the [Django Documentation for a Security Deployment Checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/)).


### Allowing your Hostname
In Django, they have a security feature which will only except requests from particular, *allowed* hosts. By only allowing specified domains to be served by your web server, this reduces the chance that your app could be part [HTTP Host Header attack](https://www.acunetix.com/blog/articles/automated-detection-of-host-header-attacks/). If you were to load and view your application now, you would encounter a `DisallowedHost` exception stopping your app from loading.

This is a simple problem to fix, and involves a change in your project's `settings.py` module. First, work out your app's URL on PythonAnywhere. For a basic account, this will be `http://<username>.pythonanywhere.com`, where `<username>` is replaced with your PythonAnywhere username. It's a good idea to edit this file locally (on your own computer), then `git add`, `git commit` and `git push` your changes to your Git repository, before downloading the changes to your PythonAnywhere account. Alternatively, you can edit the file directly on PythonAnywhere by editing the file in the Web interface's files component -- or using a text editor in the terminal, like `nano` or `vi`.

With this information, open your project's `settings.py` module and locate the `ALLOWED_HOSTS` list, which by default will be empty (and found near the top of the file). Add a string with your PythonAnywhere URL into that list -- such that it now looks like the following example.

{lang="python",linenos=off}
	ALLOWED_HOSTS = ['http://<username>.pythonanywhere.com']

If you have edited the file on your own computer, you can now go through the (hopefully) now familiar process of running the `git add settings.py`, `git commit` and `git push` commands to make changes to your Git repository. Once done, you should then run the `git pull` command to retrieve the changes on your PythonAnywhere account. If you have edited the file directly on PythonAnywhere, simply save the file.

All that then remains is for you to reload your PythonAnywhere app. This can be done by clicking the *Reload* button in the PythonAnywhere web components page. Once you've done this, access your app's URL, and you should see your app working, but without static media, which we will set up shortly.
	
I> ### Bad Gateway Errors
I> During deployment sometimes you might receive `HTTP 502 - Bad Gateway` errors instead of your application. Try reloading your application again, and then waiting a longer. If the problem persists, try reloading again. If the problem still persists, [check out your log files](#section-deploy-logfiles) to see if any accesses/errors are occurring, before contacting the PythonAnywhere support.

### Setting the Secret Key
It is wise not to commit your secret key your git repository - and instead load in the key in. To do this, open your project's `settings.py` file and either chnage the secret key that you are using in production (hack) or load it from a file:

{lang="python",linenos=off}
    key = None
    with open('/home/<username>/secret.key') as f:
        key = f.read().strip()
    SECRET_KEY = key

Then create a file called `secret.key` and put it into your home directory.


### Adding your Search API Key
While you are adding secret keys, also 
[add your search API key]({#section-searchapi-adding-key}) to `bing.key` so that the search functionality in Rango is enabled.


### Turning off `DEBUG` Mode
Next you need to turn off the debug mode, because if you leave it on, then you are providing hackers with sensitive information about your web application when they get it to crash. So it is a good idea to instruct Django that your application is now hosted on a production server. To do this, open your project's `settings.py` file and change `DEBUG = True` to `DEBUG = False`. This disables [Django's debug mode](https://docs.djangoproject.com/en/2.1/ref/settings/#debug), and removes explicit error messages. You can still however view Python stack traces to debug any exceptions that are raised as people use your app -- in the server logs (see below).


### Assigning Static Paths
We're almost there. One issue that we still have to address is to sort out paths for our application. Doing so will allow PythonAnywhere's servers to serve your static content, for example From the PythonAnywhere dashboard, click the URL of your app and wait for the page to load.

Once loaded, perform the following under the *Static files* header. We essentially are adding in the correct URLs and filesystem paths to allow PythonAnywhere's web server to find and serve your static media files.

First, we should set the location of the Django admin interface's static media files. Click the *Enter URL* link, and type in `/static/admin/`. Click the tick to confirm your input, and then click the *Enter path* link, entering the following long-winded filesystem path (all on a single line).

{lang="python",linenos=off}  
	/home/<username>/.virtualenvs/rango/lib/<python-version>/site-packages/django/
	  contrib/admin/static/admin
	

As usual, replace `<username>` with your PythonAnywhere username. `<python-version>` should also be replaced with `python2.7`, `python3.6`, etc., depending on which Python version you selected. You may also need to change `rango` if this is not the name of your application's virtual environment. Remember to hit return to confirm the path, or click the tick.

Repeat the two steps above for the URL `/static/` and filesystem path `/home/<username>/<path-to>/tango_with_django_project/static`, with the path setting pointing to the `static` directory of your Web application.

Setting the admin static directory means that when you visit the `admin` interface, it has the predefined Django stylesheets, while the applications static directory means your application has access to the images and scripts. 

### Enabling HTTPS
Not to make sure that your site is serving requests securely we can enable the HTTPS functionality provided by PythonAnywhere. They will vouch for your application, and provide a security certificate to say your application is from a secure site, and the HTTPS protocol will encrypt the requests. To do this, scroll down on the web apps tab and click the enable on the `Force HTTPS` button. You will notice that you can even add a password to protect your site when it is under development. Once you have set the HTTPS setting, you will need re-load your application.

Now go to the top of the web app dashboard and reload your Web application. Visit your website, and hopefully everything should load up nicely... and relatively securely.


## Log Files {#section-deploy-logfiles}
Deploying your Web application to an online environment introduces another layer of complexity. It is likely that you will encounter new and bizarre errors due to unsuspecting problems. When facing such errors, vital clues may be found in one of the three log files that the Web server on PythonAnywhere creates.

Log files can be viewed via the PythonAnywhere web interface by clicking on the *Web* tab, or by viewing the files in `/var/log/` within a Bash console instance. The files provided are:

- `access.log`, which provides a log of requests made to your subdomain;
- `error.log`, which logs any error messages produced by your web application; and
- `server.log`, providing log details for the UNIX processes running your application.

Note that the names for each log file are prepended with your subdomain. For example, `access.log` will have the name `<username>.pythonanywhere.com.access.log`.

When debugging, you may find it useful to delete or move the log files so that you don't have to scroll through a huge list of previous attempts. If the files are moved or deleted, they will be recreated automatically when a new request or error arises.

X> ###Exercises
X> Congratulations, you've successfully deployed Rango!
X> 
X> - Go through the [Django's Security Deployment Checklist](https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/) and configure your application to be more secure.
X> -  Tweet a link of your application to [@tangowithdjango](https://twitter.com/tangowithdjango).
X> -  Tweet or e-mail us to let us know your thoughts on the tutorial!