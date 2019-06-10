# User Authentication with `Django-Registration-Redux` {#chapter-redux}
In a [previous chapter](#chapter-user), we added in login and registration functionality by manually coding up the URLs, views and templates. However, such functionality is common to many web applications. Because of this, developers have created numerous add-on apps that can be included in your Django project to reduce the amount of code required to provide user-related functionality, such as logging in, registration, one-step and two-step authentication, password changing, password recovery, and so forth. In this chapter, we will change Rango's login and register functionality so that it uses a packaged called `django-registration-redux`.

This will mean we will need to re-factor our code to remove the login and registration functionality we previously created. From there, we will then work through setting up and configuring Rango and our wider `tango_with_django_project` codebase to make use of the `django-registration-redux` application. This chapter also will provide you with some experience of using external Django apps, and will show you how easy it is to plug them into your project.

## Setting up Django Registration Redux
First, we need to install `django-registration-redux` version `2.2` into your development environment using `pip`. Issue the following command at your terminal/Command Prompt.

{lang="text",linenos=off}
	$ pip install -U django-registration-redux==2.2

With the package installed, we need to tell Django that we will be using the `registration` app that comes within the `django-registration-redux` Python package. Open up your project's `settings.py` file, and update the `INSTALLED_APPS` list to include the `registration` package. An example `INSTALLED_APPS` list is shown below.

{lang="python",linenos=off}
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'rango',
	    'registration'  # Add in the registration package
	    ]
	

While you are in the `settings.py` module, you can also add the following variables that are part of the `registration` package's configuration. We provide shorthand comments to explain what each configuration variable does.

{lang="python",linenos=off}
	# If True, users can register.
	REGISTRATION_OPEN = True
	
	# If True, the user will be automatically logged in after registering.
	REGISTRATION_AUTO_LOGIN = True
	
	# The URL that Django redirects users to after logging in.
	LOGIN_REDIRECT_URL = 'rango:index' 
	
	# The page users are directed to if they are not logged in.
	# This was set in a previous chapter. The registration package uses this, too.
	LOGIN_URL = 'auth_login' 

Remember, we can specify URL mapping names instead of absolute URLs to make our configuration more versatile. Have a look at the section below to see where the value for `LOGIN_URL` comes from. The value for `LOGIN_REDIRECT_URL` simply points to the Rango homepage; we redirect users here after successfully logging in.

In your *project's* `urls.py` module (i.e. `<Workspace>/tango_with_django_project/urls.py`), you can now update the `urlpatterns` list so that it includes a reference to the `registration` package:

{lang="python",linenos=off}
	path('accounts/', include('registration.backends.simple.urls')),

The `django-registration-redux` package provides a number of different registration backends that you can use, depending on your needs. For example, you may want a two-step process where user is sent a confirmation email and a verification link. Here we will just be using the simple one-step registration process where a user sets up their account by entering in a username, email, and password -- and from there is automatically logged in.

## Functionality and URL mapping {#section-redux-urls}
The Django Registration Redux package provides the machinery for numerous functions. In the `registration.backends.simple.urls`, it provides key mappings, as shown in the table below.

| **Activity**             | **URL**                           | **Mapping Name**            |
|--------------------------|-----------------------------------|-----------------------------|
| Login                    | `/accounts/login/`                | `auth_login`                |
| Logout                   | `/accounts/logout/`               | `auth_logout`               |
| Registration             | `/accounts/register/`             | `registration_register`     |
| Registration Closed      | `/accounts/register/closed/`      | `registration_disallowed`   |
| Password Change          | `/accounts/password/change/`      | `auth_password_change`      |
| Change Complete          | `/accounts/password/change/done/` | `auth_password_change_done` |

All too good to be true! While the functionality is provided for you, the `django-registration-redux` package unfortunately does not provide templates for each of the required pages. This makes sense, as templates tend to be application-specific. As such, we'll need to create templates for each view.

## Setting up the Templates
In the [Django Registration Redux Quick Start Guide](https://django-registration-redux.readthedocs.org/en/latest/quickstart.html), an overview of what templates are required is provided. However, it is not immediately clear what goes within each template. Rather than try and work it out from the code, we can take a look at a set of [templates written by Anders Hofstee](https://github.com/macdhuibh/django-registration-templates) to quickly get the gist of what we need to code up.

As we'll be working on templates that the `registration` app uses, we will need to create a new directory to keep these new templates separate from our `rango` templates. In the `templates` directory, create a new directory called `registration`. We will be working on creating the basic templates from within there, as the `registration` package will look in that directory for its templates.

I> ### Inheriting Templates across Apps
I> You can inherit from base templates that belong to other apps. We'll be doing this in the code snippets below. Although we create templates in the `registration` directory for the `registration` app, we extend these templates from the `base.html` template for Rango. This will allow us to ensure a consistent look is provided across each rendered page, key to a professional website's design.

I> ### What does `form action="."` do?
I> In the templates we add below, you will notice that those with a `<form>` element have an `action` set to `.`. What does the period mean? When referencing directories and files, the period (`.`) denotes the *current file or directory.* Translated to a form submission, this means *submit the contents of the form using a POST request to the same URL as we are currently on.*
I>
I> This behaviour is the same as forms we created in prior chapters, where corresponding views had a conditional switch for processing data from a `POST` request, or rendering a blank form for a `GET` request.

### Login Template {#section-redux-templates-login}
In the `templates/registration` directory, create the file `login.html`. This will house the template used by the `registration` `auth_login` view. Add the following code to the template.

{lang="html",linenos=off}
	{% extends 'rango/base.html %}
	
	{% block title_block %}
	    Login
	{% endblock %}
	
	{% block body_block %}
	    <h1>Login</h1>
	
	    <form method="post" action=".">
	        {% csrf_token %}
	    
	        {{ form.as_p }}
	    
	        <input type="submit" value="Log in" />
	        <input type="hidden" name="next" value="{{ next }}" />
	    </form>
	
	    <p>
	        Not registered? <a href="{% url 'registration_register %}">Register here!</a>
	    </p>
	{% endblock %}

Notice that whenever a URL is referenced, the `url` template tag is once again used to reference it. If you visit `http://127.0.0.1:8000/accounts/`, you will see the list of URL mappings and the names associated with each URL (assuming that `DEBUG=True` in `settings.py`). Alternatively, refer to the shorthand table we provided above.

### Logout Template
In the `templates/registration` directory, create the file `logout.html`. This template will be rendered whenever a user logs out from Rango. Add the following code to the new template.

{lang="html",linenos=off}
	{% extends 'rango/base.html' %}
	
	{% block title_block %}
	    Logged Out
	{% endblock %}
	
	{% block body_block %}
	    <h1>Logged Out</h1>
	    
	    <p>
	        You have been successfully logged out. Thanks for spending time on Rango!
	    </p>
	{% endblock %}

### Registration Template
In `templates/registration` directory, create the file `registration_form.html`. This will house the template used to render a registration form. Add the following code to the new template.

{lang="html",linenos=off}
	{% extends 'rango/base.html %}
	
	{% block title_block %}
	    Register
	{% endblock %}
	
	{% block body_block %}
	    <h1>Register Here</h1>
	
	    <form method="post" action=".">
	        {% csrf_token %}
	        
	        {{ form.as_p }}
	        
	        <input type="submit" value="Log in" />
	    </form>
	{% endblock %}

### Registration Closed Template
In `templates/registration` directory, create the file `registration_closed.html`. This template will be rendered if a potential user attempts to register when registration is closed. Add the following code to the new file.

{lang="html",linenos=off}
	{% extends 'rango/base.html %}
	
	{% block title_block %}
	    Registration Closed
	{% endblock %}
	
	{% block body_block %}
	    <h1>Registration Closed</h1>
	    
	    <p>Unfortunately, registration is currently closed. Please try again later!</p>
	{% endblock %}

### Try out the Registration Process
With the basic forms created, we can now attempt to register using the `django-registration-redux` package. First, we will need to migrate our database using the `$ python manage.py migrate` command, followed by `$ python manage.py makemigrations`. After these steps, visit the registration page at <http://127.0.0.1:8000/accounts/register/>.

{id="fig-ch11-redux-registration"}
![A screenshot of the updated registration page using `django-registration-redux`.](images/ch11-redux-registration.png)

As seen in the [figure above](#fig-ch11-redux-registration), note how the registration form contains two fields for the new user's password. This is standard in pretty much every website nowadays, and provides a means for validating the password entered by the user. Try registering, but enter different passwords.

Notice how the `registration` app is handling all of the logic for you, and also redirects you to the rango homepage on a successful registration, as per the `LOGIN_REDIRECT_URL` setting specified in your project's `settings.py` module.

### Refactoring your Existing Project
Now that you are happy with the `registration` code, we will need to update our existing `rango` codebase to point to the new `django-registration-redux` URLs.

In the `rango/base.html` template, update the following URLs.

- Update the `Logout` URL to point to `{% url 'auth_logout' %}?next={% url 'rango:index '%}`.
- Update the `Login` URL to point to `{% url 'auth_login' %}`.
- Update the `Sign Up` URL to point to `{% url 'registration_register' %}`.

Next, open your project's `settings.py` module. You should have updated this earlier, but it's good to double check.

- Verify that the value of `LOGIN_URL` points to `auth_login`. This will translate to the `registration` URL for the login action.

Notice that for the logout hyperlink we have included an additional component to the URL, namely `?next={% url 'rango:index' %}`. This is provided so when the user logs out, it will redirect them straight to the Rango index page. If we exclude it, then they will be directed to the log out page that we created earlier, telling them that they have been successfully logged out. We include this to demonstrate some of the advanced functionality of the `django-registration-redux` package.

Finally, you need to decommission existing user authentication code that you wrote in previous chapters. This will entail removing the `register()`, `user_login()` and `user_logout()` views from Rango's `views.py` module, the corresponding URL mappings from Rango's `urls.py` module, and templates from the `templates/rango/` directory. If you do not want to delete this code, simply comment them out. Remember, too, that there will be some redundant `import` statements at the top of `views.py`!

X> ### Exercise
X> - Using the `django-registration-redux` package, provide users of your Rango app with the ability to change their password.
X> - Add a link to Rango's `base.html` template that directs users to the new password changing functionality. Make sure only those who are logged in can view the link.

T> ### Hints
T> To help you with the exercises above, the following hints may be of some use to you.
T>
T> - Have a look at [Anders Hofstee's Templates](https://github.com/macdhuibh/django-registration-templates/tree/master/registration) to get yourself started. In particular, looking at this repository will be very helpful in figuring out what to call the two new templates you require for this exercise.
T> - Refer to the [table we provided earlier in this chapter](#section-redux-urls) to figure out what URLs and name mappings are required for this exercise.