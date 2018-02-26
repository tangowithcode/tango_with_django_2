# User Authentication {#chapter-user}
Most web applications ask users to sign up and register - so that they can manage their account and have access to special features. For Rango, we want to control what actions are available to different users. So the aim of this next part of the tutorial is to get you familiar with the user authentication mechanisms provided by Django. We'll be using the `auth` app provided as part of a standard Django installation, located in package `django.contrib.auth`. According to the [Django  documentation on authentication](https://docs.djangoproject.com/en/2.0/topics/auth/), the application provides the following concepts and functionality.

- The concept of a *User* and the *User* Model.
- *Permissions*, a series of binary flags (e.g. yes/no) that determine what a user may or may not do.
- *Groups*, a method of applying permissions to more than one user.
- A configurable *password hashing system*, a must for ensuring data security.
- *Forms and view tools for logging in users*, or restricting content.

There's lots that Django can do for you regarding user authentication. In this chapter, we'll be covering the basics to get you started. This will help you build your confidence with the available tools and their underlying concepts. Note that we'll be showing you how to set up the user authentication manually, from first principles using Django, but in a later chapter we will show you how we can use a pre-made application that handles the registeration process for us.

## Setting up Authentication
Before you can begin to play around with Django's authentication offering, you'll need to make sure that the relevant settings are present in your Rango project's `settings.py` file.

Within the `settings.py` file find the `INSTALLED_APPS` list and check that `django.contrib.auth` and `django.contrib.contenttypes` are listed, so that it looks similar to the code below:

{lang="python",linenos=off}
	INSTALLED_APPS =[
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'rango',
	]

While `django.contrib.auth` provides Django with access to the provided authentication system, the package `django.contrib.contenttypes` is used by the authentication app to track models installed in your database.

I> ### Migrate, if necessary!
I> If you had to add `django.contrib.auth` and `django.contrib.contenttypes` applications to your `INSTALLED_APPS` tuple, you will need to update your database with the `$ python manage.py migrate` command. This will add the underlying tables to your database e.g. a table for the `User` model.
I>
I> It's generally good practice to run the `migrate` command whenever you add a new app to your Django project - the app could contain models that'll need to be synchronised to your underlying database.

## Password Hashing
[*Storing passwords as plaintext within a database is something that should never be done under any circumstances.*](http://stackoverflow.com/questions/1197417/why-are-plain-text-passwords-bad-and-how-do-i-convince-my-boss-that-his-treasur) If the wrong person acquired a database full of user accounts to your app, they could wreak havoc. Fortunately, Django's `auth` app by default stores a [hash of user passwords](https://en.wikipedia.org/wiki/Cryptographic_hash_function) using the [PBKDF2 algorithm](http://en.wikipedia.org/wiki/PBKDF2), providing a good level of security for your user's data.  However, if you want more control over how the passwords are hashed, you can change the approach used by Django in your project's `settings.py` module, by adding in a tuple to specify the `PASSWORD_HASHERS`. An example of this is shown below.

{lang="python",linenos=off}
	PASSWORD_HASHERS = (
	    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
	)

Django considers the order of hashers specified as important, and will pick and use the first password hasher in `PASSWORD_HASHERS` (e.g. `settings.PASSWORD_HASHERS[0]`). If other password hashers are specified in the tuple, Django will also use these if the first hasher doesn't work.

If you want to use a more secure hasher, you can install [Bcrypt](https://pypi.python.org/pypi/bcrypt/) using `pip install bcrypt`, and then set the `PASSWORD_HASHERS` to be:

{lang="python",linenos=off}
	PASSWORD_HASHERS = [
	    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
	    'django.contrib.auth.hashers.BCryptPasswordHasher',
	    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
	]

As previously mentioned, Django by default uses the PBKDF2 algorithm to hash passwords. If you do not specify a `PASSWORD_HASHERS` tuple in `settings.py`, Django will use the `PBKDF2PasswordHasher` password hasher, by default. You can read more about password hashing in the [Django documentation on how Django stores passwords](https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#how-django-stores-passwords).


## Password Validators
As people may be tempted to enter a password that is comparatively easy to guess, Django provides a number of [password validation](https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators) methods. In your Django project's `settings.py` module, you will notice a list of nested dictionaries with the name `AUTH_PASSWORD_VALIDATORS`. From the nested dictionaries, you can clearly see that Django 1.9 comes with a number of pre-built password validators for common password checks, such as length. An `OPTIONS` dictionary can be specified for each validator, allowing for easy customisation. If, for example, you wanted to ensure accepted passwords are at least six characters long, you can set `min_length` of the `MinimumLengthValidator` password validator to `6`. This can be seen in the example shown below.

{lang="python",linenos=off}
	AUTH_PASSWORD_VALIDATORS = [
	    ...
	    {
	        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	        'OPTIONS': { 'min_length': 6, }
	    },
	    ...
	]
	
It is also possible to create your own password validators. Although we don't cover the creation of custom password validators in this tutorial, refer to the [official Django documentation on password validators](https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#password-validation) for more information.

## The `User` Model
The `User` object (located at `django.contrib.auth.models.User`) is considered to be the core of Django's authentication system. A `User` object represents each of the individuals interacting with a Django application. The [Django documentation on User objects](https://docs.djangoproject.com/en/2.0/topics/auth/default/#user-objects) states that they are used to allow aspects of the authentication system like access restriction, registration of new user profiles, and the association of creators with site content.

The `User` model has five key attributes. They are:

-   the *username* for the user account;
-   the account's *password*;
-   the user's *email address*;
-   the user's *first name*; and
-   the user's *surname*.

The `User` model also comes with other attributes such as `is_active`, `is_staff` and `is_superuser`. These are boolean fields used to denote whether the account is active, owned by a staff member, or has superuser privileges respectively.  Check out the [Django documentation on the user model](https://docs.djangoproject.com/en/2.0/ref/contrib/auth/#django.contrib.auth.models.User) for a full list of attributes provided by the base `User` model.

##Additional `User` Attributes
If you would like to include other user related attributes than what is provided by the `User` model, you will needed to create a model that is *associated* with the `User` model. For our Rango app, we want to include two more additional attributes for each user account. Specifically, we wish to include:

- a `URLField`, allowing a user of Rango to specify their own website; and
- a `ImageField`, which allows users to specify a picture for their user profile.

This can be achieved by creating an additional model in Rango's `models.py` file. Let's add a new model called `UserProfile`:

{lang="python",linenos=off}
	class UserProfile(models.Model):
	    # This line is required. Links UserProfile to a User model instance.
	    user = models.OneToOneField(User, on_delete=models.CASCADE)
	    
	    # The additional attributes we wish to include.
	    website = models.URLField(blank=True)
	    picture = models.ImageField(upload_to='profile_images', blank=True)
	    
	    def __str__(self):
	        return self.user.username

Note that we reference the `User` model using a one-to-one relationship. Since we reference the default `User` model, we need to import it within the `models.py` file:

{lang="python",linenos=off}
	from django.contrib.auth.models import User

For Rango, we've added two fields to complete our user profile, and provided a `__str__()` method to return a meaningful value when a unicode representation of a `UserProfile` model instance is requested. 

For the two fields `website` and `picture`, we have set `blank=True` for both. This allows each of the fields to be blank if necessary, meaning that users do not have to supply values for the attributes.

Furthermore, it should be noted that the `ImageField` field has an `upload_to` attribute. The value of this attribute is conjoined with the project's `MEDIA_ROOT` setting to provide a path with which uploaded profile images will be stored. For example, a `MEDIA_ROOT` of `<workspace>/tango_with_django_project/media/` and `upload_to` attribute of `profile_images` will result in all profile images being stored in the directory `<workspace>/tango_with_django_project/media/profile_images/`. Recall that in the [chapter on templates and media files](#chapter-templates-static) we set up the media root there. 

I> ### What about Inheriting to Extend?
I> It may have been tempting to add the additional fields defined above by inheriting from the `User` model directly. However, because other applications may also want access to the `User` model, it not recommended to use inheritance, but to instead use a one-to-one relationship within your database.

I> ### Take the PIL
I> The Django `ImageField` field makes use of the *Python Imaging Library (PIL)*. If you have not done so already, install PIL via Pip with the command `pip install pillow`. If you don't have `jpeg` support enabled, you can also install PIL with the command `pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"`.
I>
I> You can check what packages are installed in your (virtual) environment by issuing the command `pip list`.

To make the `UserProfile` model data accessible via the Django admin Web interface, import the new `UserProfile` model into Rango's `admin.py` module.

{lang="python",linenos=off}
	from rango.models import UserProfile

Now you can register the new model with the admin interface, with the following line.

{lang="python",linenos=off}
	admin.site.register(UserProfile)

I> ### Once again, Migrate!
I> Remember that your database must be updated with the creation of a new model. Run:
I> `$ python manage.py makemigrations rango` 
I> from your terminal or Command Prompt to create the migration scripts for the new `UserProfile` model. Then run:
I> `$ python manage.py migrate` 
I> to execute the migration which creates the associated tables within the underlying database.

##Creating a *User Registration* View and Template
With our authentication infrastructure laid out, we can now begin to build on it by providing users of our application with the opportunity to create user accounts. We can achieve this by creating a new view, template and URL mapping to handle user registrations.


I> ### Django User Registration Applications
I>
I> It is important to note that there are several off the shelf user registration applications available which reduce a lot of the hassle of building your own registration and login forms. 
I> 
I> However, it's a good idea to get a feeling for the underlying mechanics before using such applications. This will ensure that you have some sense of what is going on under the hood. *No pain, no gain.* It will also reinforce your understanding of working with forms, how to extend upon the `User` model, and how to upload media files.

To provide user registration functionality, we will now work through the following steps:

- create a `UserForm` and `UserProfileForm`;
- add a view to handle the creation of a new user;
- create a template that displays the `UserForm` and `UserProfileForm`; and
- map a URL to the view created.

As a final step to integrate our new registration functionality, we will also:

- link the index page to the register page.

### Creating the `UserForm` and `UserProfileForm`
In `rango/forms.py`, we now need to create two classes inheriting from `forms.ModelForm`. We'll be creating one for the base `User` class, as well as one for the new `UserProfile` model that we just created. The two `ModelForm`-inheriting classes allow us to display a HTML form displaying the necessary form fields for a particular model, taking away a significant amount of work for us.

In `rango/forms.py`, let's first create our two classes which inherit from `forms.ModelForm`. Add the following code to the module.

{lang="python",linenos=off}
	class UserForm(forms.ModelForm):
	    password = forms.CharField(widget=forms.PasswordInput())
	    
	    class Meta:
	        model = User
	        fields = ('username', 'email', 'password')
	    
	class UserProfileForm(forms.ModelForm):
	    class Meta:
	        model = UserProfile
	        fields = ('website', 'picture')

You'll notice that within both classes, we added a [nested](http://www.brpreiss.com/books/opus7/html/page598.html) `Meta` class. As [the name of the nested class suggests](http://www.webopedia.com/TERM/M/meta.html), anything within a nested `Meta` class describes additional properties about the particular class to which it belongs. Each `Meta` class must supply a `model` field. In the case of the `UserForm` class the associated model is the `User` model. You also need to specify the `fields` or the fields to `exclude`, to indicate which fields associated with the model should be present (or not) on the rendered form.

Here, we only want to show the fields `username`, `email` and `password` associated with the `User` model, and the `website` and `picture` fields associated with the `UserProfile` model. For the `user` field within `UserProfile` model, we will need to make this association when we register the user. This is because when we create a `UserProfile` instance, we won't yet have the `User` instance to refer to.

You'll also notice that `UserForm` includes a definition of the `password` attribute. While a `User` model instance contains a `password` attribute by default, the rendered HTML form element will not hide the password. If a user types a password, the password will be visible. By updating the `password` attribute, we can specify that the `CharField` instance should hide a user's input from prying eyes through use of the `PasswordInput()` widget.

Finally, remember to include the required classes at the top of the `forms.py` module! We've listed them below for your convenience.

{lang="python",linenos=off}
	from django import forms
	from django.contrib.auth.models import User
	from rango.models import Category, Page, UserProfile

### Creating the `register()` View
Next, we need to handle both the rendering of the form and the processing of form input data. Within Rango's `views.py`, add `import` statements for the new `UserForm` and `UserProfileForm` classes.

{lang="python",linenos=off}
	from rango.forms import UserForm, UserProfileForm

Once you've done that, add the following new view, `register()`.

{lang="python",linenos=off}
	def register(request):
	    # A boolean value for telling the template 
	    # whether the registration was successful.
	    # Set to False initially. Code changes value to 
	    # True when registration succeeds.
	    registered = False
	    
	    # If it's a HTTP POST, we're interested in processing form data.
	    if request.method == 'POST':
	        # Attempt to grab information from the raw form information.	
	        # Note that we make use of both UserForm and UserProfileForm.
	        user_form = UserForm(data=request.POST)
	        profile_form = UserProfileForm(data=request.POST)
	        
	        # If the two forms are valid...
	        if user_form.is_valid() and profile_form.is_valid():
	            # Save the user's form data to the database.
	            user = user_form.save()
	            
	            # Now we hash the password with the set_password method.
	            # Once hashed, we can update the user object.
	            user.set_password(user.password)
	            user.save()
	            
	            # Now sort out the UserProfile instance.
	            # Since we need to set the user attribute ourselves, 
	            # we set commit=False. This delays saving the model 
	            # until we're ready to avoid integrity problems.
	            profile = profile_form.save(commit=False)
	            profile.user = user
	            
	            # Did the user provide a profile picture?
	            # If so, we need to get it from the input form and 
	            #put it in the UserProfile model.
	            if 'picture' in request.FILES:
	                profile.picture = request.FILES['picture']
	            
	            # Now we save the UserProfile model instance.
	            profile.save()
	            
	            # Update our variable to indicate that the template
                # registration was successful.
	            registered = True
	        else:
	            # Invalid form or forms - mistakes or something else?
	            # Print problems to the terminal.
	            print(user_form.errors, profile_form.errors)
	    else:
	        # Not a HTTP POST, so we render our form using two ModelForm instances.
	        # These forms will be blank, ready for user input.
	        user_form = UserForm()
	        profile_form = UserProfileForm()
	    
	    # Render the template depending on the context.
	    return render(request,
	                  'rango/register.html',
	                  {'user_form': user_form,
                       'profile_form': profile_form, 
	                   'registered': registered})

While the view looks pretty complicated, it's actually very similar to how we implemented the [add category](#section-forms-addcategory) and [add page](#section-forms-addpage) views. However, here we have to also handle two distinct `ModelForm` instances - one for the `User` model, and one for the `UserProfile` model. We also need to handle a user's profile image, if he or she chooses to upload one.

Furthermore, we need to establish a link between the two model instances that we have created. After creating a new `User` model instance, we reference it in the `UserProfile` instance with the line `profile.user = user`. This is where we populate the `user` attribute of the `UserProfileForm` form, which we hid from users.

### Creating the *Registration* Template
Now we need to make the template that will be used by the new `register()` view. Create a new template file, `rango/register.html`, and add the following code.

{lang="html",linenos=on}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	
	{% block title_block %}
	    Register
	{% endblock %}
	
	{% block body_block %}
	    <h1>Register for Rango</h1>
	    {% if registered %}
	        Rango says: <strong>thank you for registering!</strong>
	        <a href="{% url 'rango:index' %}">Return to the homepage.</a><br />
	    {% else %}
	        Rango says: <strong>register here!</strong><br />
	        <form id="user_form" method="post" action="{% url 'rango:register' %}"
	              enctype="multipart/form-data">
	        
	        {% csrf_token %}
	        
	        <!-- Display each form  -->
	        {{ user_form.as_p }}
	        {{ profile_form.as_p }}
	        
	        <!-- Provide a button to click to submit the form. -->
	        <input type="submit" name="submit" value="Register" />
	    </form>
	    {% endif %}
	{% endblock %}

I> ### Using the `url` Template Tag
I> Note that we are using the `url` template tag in the above template code e.g. `{% url 'register' %}`. 
I> This means we will have to ensure that when we map the URL, we name it `register`.

The first thing to note here is that this template makes use of the `registered` variable we used in our view indicating whether registration was successful or not. Note that `registered` must be `False` in order for the template to display the registration form - otherwise the success message is displayed.

Next, we have used the `as_p` template function on the `user_form` and `profile_form`. This wraps each element in the form in a paragraph (denoted by the `<p>` HTML tag). This ensures that each element appears on a new line.

Finally, in the `<form>` element, we have included the attribute `enctype`. This is because if the user tries to upload a picture, the response from the form may contain binary data - and may be quite large. The response therefore will have to be broken into multiple parts to be transmitted back to the server. As such, we need to denote this with `enctype="multipart/form-data"`. This tells the HTTP client (the web browser) to package and send the data accordingly. Otherwise, the server won't receive all the data submitted by the user.

W> ### Multipart Messages and Binary Files
W> You should be aware of the `enctype` attribute for the `<form>` element. When you want users to upload files from a form, it's an absolute *must* to set `enctype` to `multipart/form-data`. This attribute and value combination instructs your browser to send form data in a special way back to the server. Essentially, the data representing your file is split into a series of chunks and sent. For more information, check out [this great Stack Overflow answer](http://stackoverflow.com/a/4526286).

Furthermore, remember to include the CSRF token, i.e. `{% csrf_token %}` within your `<form>` element! If you don't do this, Django's [cross-site forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) protection middleware layer will refuse to accept the form's contents, returning an error.

### The `register()` URL Mapping
With our new view and associated template created, we can now add in the URL mapping. In Rango's URLs module `rango/urls.py`, modify the `urlpatterns` tuple as shown below.
 
{lang="python",linenos=off}
	urlpatterns = [
	    path('', views.index, name='index'),
	    path('about/', views.about, name='about'),
	    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
	    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
	    path('add_category/', views.add_category, name='add_category'),
		path('register/', views.register, name='register'), # New pattern!

	]

The newly added pattern (at the bottom of the list) points the URL `/rango/register/` to the `register()` view. Also note the inclusion of a `name` for our new URL, `register`, which we used in the template when we used the `url` template tag, e.g. `{% url 'register' %}`.

### Linking Everything Together
Finally, we can add a link pointing to our new registration URL by modifying the `base.html` template. Update `base.html` so that the unordered list of links that will appear on each page contains a link allowing users to register for Rango.

{lang="html",linenos=off}
	<ul>
		<li><a href="{% url 'rango:add_category' %}">Add a New Category</a></li>
		<li><a href="{% url 'rango:about' %}">About</a></li>	
		<li><a href="{% url 'rango:index' %}">Index</a></li>
		<li><a href="{% url 'rango:register' %}">Sign Up</a></li>
	</ul>

### Demo
Now everything is plugged together, try it out. Start your Django development server and try to register as a new user. Upload a profile image if you wish. Your registration form should look like the one illustrated in the [figure below](#fig-rango-register-form).

{id="fig-ch9-user-register"}
![A screenshot illustrating the basic registration form you create as
part of this tutorial.](images/ch9-rango-register-form.png)

Upon seeing the message indicating your details were successfully registered, the database should have a new entry in the `User` and `UserProfile` models. Check that this is the case by going into the Django Admin interface.


## Implementing Login Functionality
With the ability to register accounts completed, we now need to provide users of Rango with the ability to login. To achieve this, we'll need to undertake the workflow below:

-   Create a login in view to handle the processing of user credentials
-   Create a login template to display the login form
-   Map the login view to a URL
-   Provide a link to login from the index page

### Creating the `login()` View
First, open up Rango's views module at `rango/views.py` and create a new view called `user_login()`. This view will handle the processing of data from our subsequent login form, and attempt to log a user in with the given details.

{lang="python",linenos=off}
	def user_login(request):
	    # If the request is a HTTP POST, try to pull out the relevant information.
	    if request.method == 'POST':
	        # Gather the username and password provided by the user.
	        # This information is obtained from the login form.
	        # We use request.POST.get('<variable>') as opposed
	        # to request.POST['<variable>'], because the
	        # request.POST.get('<variable>') returns None if the
	        # value does not exist, while request.POST['<variable>']
	        # will raise a KeyError exception.
	        username = request.POST.get('username')
	        password = request.POST.get('password')
	        
	        # Use Django's machinery to attempt to see if the username/password
	        # combination is valid - a User object is returned if it is.
	        user = authenticate(username=username, password=password)
	        
	        # If we have a User object, the details are correct.
	        # If None (Python's way of representing the absence of a value), no user
	        # with matching credentials was found.
	        if user:
	            # Is the account active? It could have been disabled.
	            if user.is_active:
	                # If the account is valid and active, we can log the user in.
	                # We'll send the user back to the homepage.
	                login(request, user)
	                return HttpResponseRedirect(reverse('index'))
	            else:
	                # An inactive account was used - no logging in!
	                return HttpResponse("Your Rango account is disabled.")
	        else:
	            # Bad login details were provided. So we can't log the user in.
	            print("Invalid login details: {0}, {1}".format(username, password))
	            return HttpResponse("Invalid login details supplied.")
	        
	    # The request is not a HTTP POST, so display the login form.
	    # This scenario would most likely be a HTTP GET.
	    else:
	        # No context variables to pass to the template system, hence the
	        # blank dictionary object...
	        return render(request, 'rango/login.html', {})

As before, this view may seem rather complex as it has to handle a variety of scenarios. As shown in previous examples, the `user_login()` view handles form rendering and processing - where the form this time contains `username` and `password` fields.

First, if the view is accessed via the HTTP `GET` method, then the login form is displayed. However, if the form has been posted via the HTTP `POST` method, then we can handle processing the form.

If a valid form is sent via a `POST` request, the username and password are extracted from the form. These details are then used to attempt to authenticate the user. The Django function `authenticate()` checks whether the username and password provided actually match to a valid user account. If a valid user exists with the specified password, then a `User` object is returned, otherwise `None` is returned.

If we retrieve a `User` object, we can then check if the account is active or inactive - if active, then we can issue the Django function  `login()`, which officially signifies to Django that the user is to be logged in.

However, if an invalid form is sent - due to the fact that the user did not add both a username and password - the login form is presented back to the user with error messages (i.e. an invalid username/password combination was provided).


You'll also notice that we make use of a new class, `HttpResponseRedirect`. As the name may suggest to you, the response generated by an instance of the `HttpResponseRedirect` class tells the client's Web browser to redirect to the URL you provide as the argument. Note that this will return a HTTP status code of `302`, which denotes a redirect, as opposed to an status code of `200` (success). See the [Django documentation on redirection](https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpResponseRedirect) to learn more.

Finally, we use another Django method called `reverse` to obtain the URL of the Rango application. This looks up the URL patterns in Rango's `urls.py` module to find a URL called `'index'`, and substitutes in the corresponding pattern. This means that if we subsequently change the URL mapping, our new view won't break.

Django provides all of these functions and classes. As such, you'll need to import them. The following `import` statements must now be added to the top of `rango/views.py`.

{lang="python",linenos=off}
	from django.contrib.auth import authenticate, login
	from django.http import HttpResponseRedirect, HttpResponse
	from django.urls import reverse

### Creating a *Login* Template
With our new view created, we'll need to create a new template, `login.html` allowing users to enter their credentials. While we know that the template will live in the `templates/rango/` directory, we'll leave you to figure out the name of the file. Look at the code example above to work out the name based upon the code for the new `user_login()` view. In your new template file, add the following code.

{lang="html",linenos=off}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	
	{% block title_block %}
	    Login
	{% endblock %}
	
	{% block body_block %}
	<h1>Login to Rango</h1>
	<form id="login_form" method="post" action="{% url 'login' %}">
	    {% csrf_token %}
	    Username: <input type="text" name="username" value="" size="50" />
	    <br />
	    Password: <input type="password" name="password" value="" size="50" />
	    <br />
	    <input type="submit" value="submit" />
	</form>
	{% endblock %}

Ensure that you match up the input `name` attributes to those that you specified in the `user_login()` view. For example, `username` matches to the username, and `password` matches to the user's password. Don't forget the `{% csrf_token %}`, either!

### Mapping the Login View to a URL
With your login template created, we can now match up the `user_login()` view to a URL. Modify Rango's `urls.py` module so that the `urlpatterns` list contains the following mapping.

{lang="python",linenos=off}
	path('login/', views.user_login, name='login'),

### Linking Together
Our final step is to provide users of Rango with a handy link to access the login page. To do this, we'll edit the `base.html` template inside of the `templates/rango/` directory. Add the following link to your list.

{lang="html",linenos=off}
	<ul>
	    ...
	    <li><a href="{% url 'rango:login' %}">Login</a></li>
	</ul>

If you like, you can also modify the header of the index page to provide a personalised message if a user is logged in, and a more generic message if the user isn't. Within the `index.html` template, find the message, as shown in the code snippet below.

{lang="html",linenos=off}
	hey there partner!

This line can then be replaced with the following code.

{lang="html",linenos=off}
	{% if user.is_authenticated %}
	    howdy {{ user.username }}!
	{% else %}
	    hey there partner!
	{% endif %}

As you can see, we have used Django's template language to check if the user is authenticated with `{% if user.is_authenticated %}`. If a user is logged in, then Django gives us access to the `user` object. We can tell from this object if the user is logged in (authenticated). If he or she is logged in, we can also obtain details about him or her. In the example about, the user's username will be presented to them if logged in - otherwise the generic `hey there partner!` message will be shown.

### Demo
Start the Django development server and attempt to login to the application. The [figure below](#fig-ch9-user-login) shows the screenshots of the login and index page.

{id="fig-ch9-user-login"}
![Screenshots illustrating the header users receive when not logged in, and logged in with username `somebody`.](images/ch9-rango-login-message.png)

With this completed, user logins should now be working. To test everything out, try starting Django's development server and attempt to register a new account. After successful registration, you should then be able to login with the details you just provided.

## Restricting Access
Now that users can login to Rango, we can now go about restricting access to particular parts of the application as per the specification, i.e. that only registered users can add categories and pages. With Django, there are several ways in which we can achieve this goal.

- In the template, we could use the `{% if user.authenticated %}` template tag to modify how the page is rendered (shown already).
- In the View, we could directly examine the `request` object and check if the user is authenticated.
- Or, we could use a *decorator* function `@login_required` provided by Django that checks if the user is authenticated.

The direct approach checks to see whether a user is logged in, via the `user.is_authenticated()` method. The `user` object is available via the `request` object passed into a view. The following example demonstrates this approach.

{lang="python",linenos=off}
	def some_view(request):
	    if not request.user.is_authenticated():
	        return HttpResponse("You are logged in.")
	    else:
	        return HttpResponse("You are not logged in.")

The third approach uses [Python decorators](http://wiki.python.org/moin/PythonDecorators). Decorators
are named after a [software design pattern by the same name](http://en.wikipedia.org/wiki/Decorator_pattern). They can dynamically alter the functionality of a function, method or class without having to directly edit the source code of the given function, method or class.

Django provides a decorator called `login_required()`, which we can attach to any view where we require the user to be logged in. If a user is not logged in and attempts to access a view decorated with `login_required()`, they are then redirected to another page ([that you can set](https://docs.djangoproject.com/en/2.0/ref/settings/#login-url)) - typically the login page.

### Restricting Access with a Decorator

To try this out, create a view in Rango's `views.py` module called `restricted()`, and add the following code

{lang="python",linenos=off}
	@login_required
	def restricted(request):
	    return HttpResponse("Since you're logged in, you can see this text!")

Note that to use a decorator, you place it *directly above* the function signature, and put a `@` before naming the decorator. Python will execute the decorator before executing the code of your function/method. As a decorator is still a function, you'll still have to import it if it resides within an external module. As `login_required()` exists elsewhere, the following `import` statement is required at the top of `views.py`.

{lang="python",linenos=off}
	from django.contrib.auth.decorators import login_required

We'll also need to add in another pattern to Rango's `urlpatterns` list in the `urls.py` file. Add the following line of code.

{lang="python",linenos=off}
	path('restricted/', views.restricted, name='restricted'),
	

And then in `base.html` add in the reference to the restricted page.
{lang="html",linenos=off}
	<ul>
	    ...
		<li><a href="{% url 'rango:restricted' %}">Restricted</a></li>	
	</ul>


We'll also need to handle the scenario where a user attempts to access the `restricted()` view, but is not logged in. What do we do with the user? The simplest approach is to redirect them to a page they can access, e.g. the registration page. Django allows us to specify this in our project's `settings.py` module, located in the project configuration directory. In `settings.py`, define the variable `LOGIN_URL` with the URL you'd like to redirect users to that aren't logged in, i.e. the login page located at `/rango/login/`:

{lang="python",linenos=off}
	LOGIN_URL = '/rango/login/'

This ensures that the `login_required()` decorator will redirect any user not logged in to the URL `/rango/login/`.

##Logging Out
To enable users to log out gracefully, it would be nice to provide a logout option to users. Django comes with a handy `logout()` function that takes care of ensuring that the users can properly and securely log out. The `logout()` function will ensure that their session is ended, and that if they subsequently try to access a view that requires authentication then they will not be able to access it, unless they log back in.

To provide logout functionality in `rango/views.py`, add the view called `user_logout()` with the following code.

{lang="python",linenos=off}
	# Use the login_required() decorator to ensure only those logged in can
	# access the view.
	@login_required
	def user_logout(request):
	    # Since we know the user is logged in, we can now just log them out.
	    logout(request)
	    # Take the user back to the homepage.
	    return HttpResponseRedirect(reverse('index'))

You'll also need to import the `logout` function at the top of `views.py`.

{lang="python",linenos=off}
	from django.contrib.auth import logout

With the view created, map the URL `/rango/logout/` to the `user_logout()` view by modifying the `urlpatterns` list in Rango's `urls.py`.

{lang="python",linenos=off}
	path('logout/', views.user_logout, name='logout'),

Now that all the machinery for logging a user out has been completed, we can add some finishing touches. It'd be handy to provide a link from the homepage to allow users to simply click a link to logout. However, let's be smart about this: is there any point providing the logout link to a user who isn't logged in? Perhaps not - it may be more beneficial for a user who isn't logged in to be given the chance to register, for example.

Like in the previous section, we'll be modifying Rango's `base.html` template and making use of the `user` object in the template's context to determine what links we want to show. Find your growing list of links at the bottom of the page, and replace it with the following code. Note we also add a link to our restricted page at `/rango/restricted/`.

{lang="html",linenos=off}
	<ul>
	{% if user.is_authenticated %}
	    <li><a href="{% url 'rango:restricted' %}">Restricted Page</a></li>
	    <li><a href="{% url 'rango:logout' %}">Logout</a></li>	
	{% else %}
	    <li><a href="{% url 'rango:login' %}">Sign In</a></li>
	    <li><a href="{% url 'rango:register' %}">Sign Up</a></li>			
	{% endif %}
	    <li><a href="{% url 'rango:add_category' %}">Add a New Category</a></li>
	    <li><a href="{% url 'rango:about' %}">About</a></li>	
	    <li><a href="{% url 'rango:index' %}">Index</a></li>
	</ul>

This code states that when a user is authenticated and logged in, he or she can see the `Restricted Page` and `Logout` links. If he or she isn't logged in, `Register Here` and `Login` are presented. As `About` and `Add a New Category` are not within the template conditional blocks, these links are available to both anonymous and logged in users.

## Taking it Further
In this chapter, we've covered several important aspects of managing user authentication within Django. We've covered the basics of installing Django's `django.contrib.auth` application into our project. Additionally, we have also shown how to implement a user profile model that can provide additional fields to the base `django.contrib.auth.models.User` model. We have also detailed how to setup the functionality to allow user registrations, login, logout, and to control access. For more information about user authentication and registration consult the [Django documentation on authentication](https://docs.djangoproject.com/en/2.0/topics/auth/).

Many Web applications however take the concepts of user authentication further. For example, you may require different levels of security when registering users, by ensuring a valid e-mail address is supplied. While we could implement this functionality, why reinvent the wheel when such functionality already exists? The `django-registration-redux` app has been developed to greatly simplify the process of adding extra functionality related to user authentication. We cover how you can use this package in a [following chapter](#chapter-redux).

X> ### Exercises
X> For now, work on the following two exercises to reinforce what you've learnt in this chapter.
X>
X> - Customise the application so that only registered users can add categories and pages, while unregistered can only view or use the categories and pages. You'll also have to ensure that the link to add pages appears only if the user browsing the website is logged in.
X> - Provide informative error messages when users incorrectly enter their username or password.
X> - Keep your templating know-how up to date by converting the restricted page view to use a template. Call the template `restricted.html`, and ensure that it too extends from Rango's `base.html` template.
