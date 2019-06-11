# Making Rango Tango! Hints {#chapter-hints}
Hopefully, you will have been able to complete the exercises given the workflows we provided. If not, or if you need a little help, have a look at the potential solutions we have provided below, and use them within your version of Rango.

I> ### Got a better solution?
I> The solutions provided in this chapter are only one way to solve each problem.
I> They are based on what we have learnt so far. However, if you implement them differently, 
I> feel free to share your solutions with us - and tweet links to @tangowithdjango for others to see.

## Track Page Clickthroughs
Currently, Rango provides a direct link to external pages. This is not very good if you want to track the number of times each page is clicked and viewed. To count the number of times a page is viewed via Rango, you'll need to perform the following steps.

### Creating a URL Tracking View
Create a new view called `goto_url()` in `/rango/views.py` which takes a parameterised HTTP `GET` request (i.e. `rango/goto/?page_id=1`) and updates the number of views for the page. The view should then redirect to the actual URL.

{lang="python",linenos=off}
	from django.shortcuts import redirect
	
	def goto_url(request):
	    page_id = None
	    url = '/rango/'
	    if request.method == 'GET':
	        if 'page_id' in request.GET:
	            page_id = request.GET['page_id']
	            
	            try:
	                page = Page.objects.get(id=page_id)
	                page.views = page.views + 1
	                page.save()
	                url = page.url
	            except:
	                pass
	                
	    return redirect(url)


Be sure that you import the `redirect()` function to `views.py` if it isn't included already!

{lang="python",linenos=off}
	from django.shortcuts import redirect

### Mapping URL
In `/rango/urls.py` add the following code to the `urlpatterns` tuple.

{lang="python",linenos=off}
	path('goto/', views.goto_url, name='goto'),


### Updating the Category Template
Update the `category.html` template so that it uses `rango/goto/?page_id=XXX` instead of providing the direct URL for users to click.

{lang="python",linenos=off}
	{% for page in pages %}
	     <li class="list-group-item">
	        <a href="{% url 'rango:goto' %}?page_id={{page.id}}">{{ page.title }}</a>
	        {% if page.views > 1 %}
	            ({{ page.views }} views)
	        {% elif page.views == 1 %}
	            ({{ page.views }} view)
	        {% endif %}
	    </li>
	{% endfor %}

Here you can see that in the template we have added some control statements to display `view`, `views` or nothing depending on the value of `page.views`.

### Updating Category View
Since we are tracking the number of clickthroughs you can now update the `category()` view, and have it order the pages by the number of views:

{lang="python",linenos=off}
	pages = Page.objects.filter(category=category).order_by('-views')

Now, confirm it all works, by clicking on links, and then going back to the category page. Don't forget to refresh or click to another category to see the updated page.

## Searching Within a Category Page
Rango aims to provide users with a helpful directory of page links. At the moment, the search functionality is essentially independent of the categories. It would be nicer however to have search integrated into category browsing. Let's assume that a user will first browse their category of interest first. If they can't find the page that they want, they can then search for it. If they find a page that is suitable, then they can add it to the category that they are in. Let's tackle the first part of this description here.

We first need to remove the global search functionality and only let users search within a category. This will mean that we essentially decommission the current search page and search view. After this, we'll need to perform the following.

### Decommissioning Generic Search
Remove the generic *Search* link from the menu bar by editing the `base.html` template. You can also remove or comment out the URL mapping in `rango/urls.py`.

### Creating a Search Form Template
Now in `category.html`, after the categories, add in a new `div` at the bottom of the template, and copy in the search form. This is very similar to the template code in the `search.html`, but we have updated the action to point to the `show_category` page. We also pass through a variable called `query`, so that the user can see what query has been issued.

{lang="html",linenos=off}
    <form class="form-inline" id="user_form" 
          method="post" action="{% url 'rango:show_category'  category.slug %}">
        {% csrf_token %}
        <div class="form-group">
            <input class="form-control" type="text" size="40" 
                   name="query" value="{{ query }}" id="query" />
        </div>
        <button class="btn btn-primary" type="submit" name="submit"
                value="Search">Search</button>
    </form>

After the search form, we need to provide a space where the results are rendered. Again, this code is similar to the template code in `search.html`.

{lang="html",linenos=off}
    {% if result_list %}
    <h3>Results</h3>
    <!-- Display search results in an ordered list -->
    <div class="list-group">
    {% for result in result_list %}
        <div class="list-group-item">
            <h4 class="list-group-item-heading">
                <a href="{{ result.link }}">{{ result.title }}</a>
                </h4>
                <p class="list-group-item-text">{{ result.summary }}</p>
        </div>
    {% endfor %}
    </div>
    {% endif %}
	

Remember to wrap the search form and search results with `{% if user.is_authenticated %}` and `{% endif %}`, so that only authenticated users can search. You don't want random users to be wasting your monthly search API's quota! And remember to encase the search box and results in a div containter and div row 	`<div class="container p-4"><div class="row">` ... `</div></div>`.

### Updating the Category View
Update the category view to handle a HTTP `POST` request (i.e. when the user submits a search) and inject the results list into the context. The following code demonstrates this new functionality.

{lang="python",linenos=off}
	def show_category(request, category_name_slug):
	    # Create a context dictionary that we can pass
	    # to the template rendering engine.
	    context_dict = {}
	    
	    try:
	        # Can we find a category name slug with the given name?
	        # If we can't, the .get() method raises a DoesNotExist exception.
	        # So the .get() method returns one model instance or raises an exception.
	        category = Category.objects.get(slug=category_name_slug)
	        # Retrieve all of the associated pages.
	        # Note that filter() returns a list of page objects or an empty list
	        pages = Page.objects.filter(category=category)
	        # Adds our results list to the template context under name pages.
	        context_dict['pages'] = pages
	        # We also add the category object from
	        # the database to the context dictionary.
	        # We'll use this in the template to verify that the category exists.
	        context_dict['category'] = category
	        # We get here if we didn't find the specified category.
	        # Don't do anything -
	        # the template will display the "no category" message for us.
	    except Category.DoesNotExist:
	        context_dict['category'] = None
	        context_dict['pages'] = None
	    
	    # New code added here to handle a POST request
	    
	    # create a default query based on the category name
	    # to be shown in the search box
	    context_dict['query'] = category.name
	    
	    result_list = []
	    if request.method == 'POST':
	        query = request.POST['query'].strip()
	        
	        if query:
	            # Run our search API function to get the results list!
	            result_list = run_query(query)
	            context_dict['query'] = query
	            context_dict['result_list'] = result_list
	    
	    
	    # Go render the response and return it to the client.
	    return render(request, 'rango/category.html', context_dict)

Notice that the `context_dict` now includes the `result_list` and `query`. If there is no query, we provide a default query, i.e. the category name. The query box then displays this value.

{id="fig-exercises-categories"}
![Rango's updated category view, complete with search API search functionality.](images/exercises-categories.png)

## Creating a `UserProfile` Instance {#section-hints-profiles}
This section provides a solution for creating Rango `UserProfile` accounts. Recall that the standard Django `auth` `User` object contains a variety of standard information regarding an individual user, such as a username and password. We however chose to implement an additional `UserProfile` model to store additional information such as a user's Website and a profile picture. Here, we'll go through how you can implement this, using the following steps.

- Create a `profile_registration.html` that will display the `UserProfileForm`.
- Create a `UserProfileForm` `ModelForm` class to handle the new form.
- Create a `register_profile()` view to capture the profile details.
- Map the view to a URL, i.e. `rango/register_profile/`.
- In the `MyRegistrationView` defined in the [Django `registration-redux` chapter](#section-redux-templates-flow), update the `get_success_url()` to point to `rango/add_profile/`.


The basic flow for a registering user here would be:

- clicking the `Register` link;
- filling out the initial Django `registration-redux` form (and thus registering);
- filling out the new `UserProfileForm` form; and
- completing the registration.

This assumes that a user will be registered with Rango *before* the profile form is saved.

### Creating a Profile Registration Template
First, let's create a template that'll provide the necessary markup for displaying an additional registration form. In this solution, we're going to keep the Django `registration-redux` form separate from our Profile Registration form - just to delineate between the two. 

Create a template in Rango's templates directory called `profile_registration.html`. Within this new template, add the following markup and Django template code.

{lang="html",linenos=off}
	{% extends "rango/base.html" %}
	
	{% block title_block %}
	    Registration - Step 2
	{% endblock %}
	
	{% block body_block %}
        <div class="jumbotron p-4">
        <div class="container">
            <h1 class="jumbotron-heading">Registration - Step 2</h1>
            </div>
        </div>
        <div class="container">
        <div class="row">
            <form method="post" action="." enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <input type="submit" value="Submit" />
            </form>
        </div>
        </div>
	{% endblock %}

Much like the previous Django `registration-redux` form that we [created previously](#section-redux-templates-login), this template inherits from our `base.html` template, which incorporates the basic layout for our Rango app. We also create an HTML `form` inside the `body_block` block. This will be populated with fields from a `form` object that we'll be passing into the template from the corresponding view (see below).

W> ### Don't Forget `multipart/form-data`!
W> When creating your form, don't forget to include the `enctype="multipart/form-data"` attribute in the `<form>` tag. We need to set this to [instruct the Web browser and server that no character encoding should be used](http://stackoverflow.com/questions/4526273/what-does-enctype-multipart-form-data-mean) - as we are performing *file uploads*. If you don't include this attribute, the image upload component will not work.

### Creating the `UserProfileForm` Class
Looking at Rango's `models.py` module, you should see a `UserProfile` model that you implemented previously. We've included it below to remind you of what it contains - a reference to a Django `django.contrib.auth.User` object, and fields for storing a Website and profile image.

{lang="python",linenos=off}
	class UserProfile(models.Model):
	    # This line is required. Links UserProfile to a User model instance.
	    user = models.OneToOneField(User)
	    # The additional attributes we wish to include.
	    website = models.URLField(blank=True)
	    picture = models.ImageField(upload_to='profile_images', blank=True)
	    
	    # Override the __unicode__() method to return out something meaningful!
	    def __str__(self):
	        return self.user.username

In order to provide the necessary HTML markup on the fly for this model, we need to implement a Django `ModelForm` class, based upon our `UserProfile` model. Looking back to the [chapter detailing Django forms](#chapter-forms), we can implement a `ModelForm` for our `UserProfile` as shown in the example below. Perhaps unsurprisingly, we call this new class `UserProfileForm`.

{lang="python",linenos=off}
	class UserProfileForm(forms.ModelForm):
	    website = forms.URLField(required=False)
	    picture = forms.ImageField(required=False)
	    
	    class Meta:
	        model = UserProfile
	        exclude = ('user',)

Note the inclusion of optional (through `required=False`) `website` and `picture` HTML form fields - and the nested `Meta` class that associates the `UserProfileForm` with the `UserProfile` model. The `exclude` attribute instructs the Django form machinery to *not* produce a form field for the `user` model attribute. As the newly registered user doesn't have reference to their `User` object, we'll have to manually associate this with their new `UserProfile` instance when we create it later.

### Creating a Profile Registration View
Next, we need to create the corresponding view to handle the processing of a `UserProfileForm` form, the subsequent creation of a new `UserProfile` instance, and instructing Django to render any response with our new `profile_registration.html` template. By now, this should be pretty straightforward to implement. Handling a form means being able to handle a request to render the form (via a HTTP `GET`), and being able to process any entered information (via a HTTP `POST`). A possible implementation for this view is shown below.

{lang="python",linenos=off}
	@login_required
	def register_profile(request):
	    form = UserProfileForm()
	    
	    if request.method == 'POST':
	        form = UserProfileForm(request.POST, request.FILES)
	        if form.is_valid():
	            user_profile = form.save(commit=False)
	            user_profile.user = request.user
	            user_profile.save()
	            
	            return redirect('index')
	        else:
	            print(form.errors)
	
	    context_dict = {'form':form}
	    
	    return render(request, 'rango/profile_registration.html', context_dict)

Upon creating a new `UserProfileForm` instance, we then check our `request` object to determine if a `GET` or `POST` was made. If the request was a `POST`, we then recreate the `UserProfileForm`, using data gathered from the `POST` request. As we are also handling a file image upload (for the user's profile image), we also need to pull the uploaded file from `request.FILES`. We then check if the submitted form was valid - meaning that form fields were filled out correctly. In this case, we only really need to check if the URL supplied is valid - since the URL and profile picture fields are marked as optional.

With a valid `UserProfileForm`, we can then create a new instance of the `UserProfile` model with the line `user_profile = form.save(commit=False)`. Setting `commit=False` gives us time to manipulate the `UserProfile` instance before we commit it to the database. This is where can then add in the necessary step to associate the new `UserProfile` instance with the newly created `User` object that has been just created (refer to the [flow at the top of this section](#section-hints-profiles) to refresh your memory). After successfully saving the new `UserProfile` instance, we then redirect the newly created user to Rango's `index` view, using the URL pattern name. If form validation failed for any reason, errors are simply printed to the console. You will probably in your own code want to make the handling of errors more robust.

If the request sent was a HTTP `GET`, the user simply wants to request a blank form to fill out - so we respond by `render`ing the `profile_registration.html` template created above with a blank instance of the `UserProfileForm`, passed to the rendering context dictionary as `form` - thus satisfying the requirement we created in our template. This solution should therefore handle all required scenarios for creating, parsing and saving data from a `UserProfileForm` form.

E> ### Can't find `login_required`?
E> Remember, once a newly registered user hits this view, they will have had a new account created for them - so we can safely assume that he or she is now logged into Rango. This is why we are using the `@login_required` decorator at the top of our view to prevent individuals from accessing the view when they are unauthorised to do so.
E> 
E> If you are receiving an error stating that the `login_required()` function (used as a decorator to our new view) cannot be located, ensure that you have the following `import` statement at the top of your `view.py` module.
E>
E> {lang="python",linenos=off}
E> 	from django.contrib.auth.decorators import login_required
E> 
E> See the [Django Documentation for more details about Authentication](https://docs.djangoproject.com/en/2.1/topics/auth/default/) .

### Mapping the View to a URL
Now that our template `ModelForm` and corresponding view have all been implemented, a seasoned Djangoer should now be thinking: *map it!* We need to map our new view to a URL, so that users can access the newly created content. Opening up Rango's `urls.py` module and adding the following line to the `urlpatterns` list will achieve this.

{lang="python",linenos=off}
	path('register_profile/', views.register_profile, name='register_profile'),

This maps our new `register_profile()` view to the URL `/rango/register_profile/`. Remember, the `/rango/` part of the URL comes from your project's `urls.py` module - the remainder of the URL is then handled by the Rango app's `urls.py` module.

### Modifying the Registration Flow
Now that everything is (almost) working, we need to tweak the process that users undertake when registering. Back in the [Django `registration-redux` chapter](#section-redux-templates-flow), we created a new class-based view called `MyRegistrationView` that changes the URL that users are redirected to upon a successful registration. This needs to be changes from redirecting a user to the Rango homepage (with URL name `index`) to our new user profile registration URL. From the previous section, we gave this the name `register_profile`. This means changing the `MyRegistrationView` class in `tango_with_dango_project/urls.py` to look be:

{lang="python",linenos=off}
	class MyRegistrationView(RegistrationView):
	    def get_success_url(self, user):
	        return reverse('rango:register_profile')

Now when a user registers, they should be then redirected to the profile registration form -- and upon successful completion of that -- be redirected to the Rango homepage. Hopefully everything will connect together and you'll be collecting more details about the users.


## Class Based Views {#section-hints-class-based-views}

In the previous subsection, we mentioned something called **class-based views**. Class based views are a different, and more elegant, but more sophisticated mechanism, for handling requests. Rather than taking a functional approach as we have done in this tutorial, that is, in our `views.py` we have written functions to handle each request, the class based approach mean inheriting and implementing a series methods to handle the requests. For example, rather than checking if a request was a `get` or a `post`, in the class based approach, you would need to implement a `get()` and `post()` method within the class. When your project and handlers become more complicated, using the Class based approach is more preferable. See the [Django Documentation for more information about Class Based Views](https://docs.djangoproject.com/en/2.1/topics/class-based-views/).


To get you started here is how we can convert the About view function to a class based view. First, in `rango\views.py` define a class called `AboutView` which inherits from `View` which we need to import from `django.views`:

{lang="python",linenos=off}
    from django.views import View

    class AboutView(View):
        def get(self, request):
            # view logic
            visitor_cookie_handler(request)
            return render(request, 'rango/about.html',
                context={'visits': request.session['visits']})
        
Next, in `rango\urls.py`, update the path, and import the `AboutView` from your views.

{lang="python",linenos=off}
    from rango.views import AboutView
    
    ...
    
    urlpatterns = [
        ...
        # Updated path that points to the About View.
        path('about/', AboutView.as_view(), name='about'),
        ...
    ]
    
    
Now, for such a simple view it is doesn't really save much time or space, but now that you have the imported the classes, and get the idea you can now update more complex views, which need to handle both `get`s and `post`s. For example, we can create an `AddCategoryView` class based view to replace the `add_category` as shown below.

{lang="python",linenos=off}
    from django.utils.decorators import method_decorator
    
    class AddCategoryView(View):

     @method_decorator(login_required)
     def get(self, request):
         form = CategoryForm()
         return render(request, 'rango/add_category.html', {'form': form})

     @method_decorator(login_required)
     def post(self, request):
         form = CategoryForm()
         form = CategoryForm(request.POST)
         if form.is_valid():
             form.save(commit=True)
             return index(request)
         else:
             print(form.errors)
         return render(request, 'rango/add_category.html', {'form': form})

Notice that to ensure that users can only add categories if they are logged in, we needed to import `method_decorator` and then decorate the `get` and `post` methods with `@method_decorator(login_required)`.
         
Next, in `rango\urls.py` we can import the class e.g. `from rango.views import AboutView, AddCategoryView` and update the path e.g. `path('add_category/', AddCategoryView.as_view(), name='add_category'),`. Without having to deal with the condition to test if the request is a post or not, we can more elegant code up how the view should respond in the different circumstances.


X> ### Class Based View Exercises
X> - Go through the Django Documentation and study how to create Class-Based Views.
X> - Update the Rango application to use Class-Based Views.
X> - Tweet how awesome you are and let us know @tangowithdjango.



## Viewing your Profile  {#section-hints-profileview}
With the creation of a `UserProfile` object now complete, let's implement the functionality to allow a user to view his or her profile and edit it. The process is again pretty similar to what we've done before. We'll need to consider the following aspects:

- the creation of a new template, `profile.html`;
- creating a new view called `profile()` that uses the `profile.html` template; and
- mapping the `profile()` view to a new URL (`/rango/profile`).

We'll also need to provide a new hyperlink in Rango's `base.html` template to access the new view. For this solution, we'll be creating a generalised view that allows you to access the information of any user of Rango. The code will allow logged in users to also edit their profile; but only *their* profile - thus satisfying the requirements of the exercise.

### Creating the Template
First, let's create a simple template for displaying a user's profile. The following HTML markup and Django template code should be placed within the new `profile.html` template within Rango's template directory.

{lang="html",linenos=off}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	{% block title %}{{ selecteduser.username }} Profile{% endblock %}
	{% block body_block %}
	<div class="jumbotron p-4">
		<div class="container">
	 		<h1 class="jumbotron-heading">{{selecteduser.username}} Profile</h1>
        </div>
    </div>
    <div class="container">
    	<div class="row">
	<img src="{{ MEDIA_URL }}{{userprofile.picture }}"
	     width="300"
	     height="300"
	     alt="{{selecteduser.username}}" />
	<br/>
	<div>
	    {% if selecteduser.username == user.username %}
	        <form method="post" action="." enctype="multipart/form-data">
	             {% csrf_token %}
	            {{ form.as_p }}
	            <input type="submit" value="Update" />
	        </form>
	    {% else %}
	    <p><strong>Website:</strong> <a href="{{userprofile.website}}">
	        {{userprofile.website}}</a></p>
	    {% endif %}
	</div>
	<div id="edit_profile"></div>
    </div>
    </div>
    {% endblock %}

Note that there are a few variables (`selecteduser`, `userprofile` and `form`) that we need to define in the template's context - we'll be doing so in the next section.

The fun part of this template is within the `body_block` block. The template shows the user's profile image at the top. Underneath, the template shows a form allowing the user to change his or her details, which is populated from the `form` variable. This form however is *only shown* when the selected user matches the user that is currently logged in, thus only allowing the presently logged in user to edit his or her profile. If the selected user does not match the currently logged in user, then the selected user's website is displayed - but it cannot be edited.

You should also take not of the fact that we again use `enctype="multipart/form-data"` in the form due to the fact image uploading is used.

### Creating the `profile()` View
Based upon the template created above, we can then implement a simple view to handle the viewing of user profiles and submission of form data. In Rango's `views.py` module, create a new class based view called `ProfileView`.

{lang="python",linenos=off}
    from rango.models import UserProfile
    from django.contrib.auth.models import User

    class ProfileView(View):
    
        def get_user_details(self, username):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return redirect('index')
            
            userprofile = UserProfile.objects.get_or_create(user=user)[0]
            form = UserProfileForm({'website': userprofile.website,
                'picture': userprofile.picture})
            return (user, userprofile, form)
    
        @method_decorator(login_required)
        def get(self, request,  username):
            (user, userprofile, form) = self.get_user_details(username)
            return render(request, 'rango/profile.html',
                {'userprofile': userprofile, 'selecteduser': user, 'form': form})
        
        @method_decorator(login_required)
        def post(self, request,  username):
            (user, userprofile, form) = self.get_user_details(username)
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if form.is_valid():
                form.save(commit=True)
                return redirect('profile', user.username)
            else:
                print(form.errors)
            return render(request, 'rango/profile.html',
                {'userprofile': userprofile, 'selecteduser': user, 'form': form})
            


This class based view requires that a user be logged in - hence the use of the `@method_decorator(login_required)` decorator, and we also need to import the `User` and `UserProfile` models. In the class, we created a helper method that both `get` and `post` use, so we dont repeat ourselves. 

The helper methods begins by selecting the selected `django.contrib.auth.User` from the database - if it exists.  If it doesn't, we perform a simple redirect to Rango's homepage rather than greet the user with an error message. We can't display information for a non-existent user! If the user does exist, we can select the user's `UserProfile` instance. If it doesn't exist, we can create a blank one. We then populate a `UserProfileForm` object with the selected user's details if we require it. The `user`, `userprofile` and populated `form` are then returned. 

In the `post` method, we handle the case where a user wants to update their accoutn information. So we  extract information from the form into a `UserProfileForm` instance that is able to reference to the `UserProfile` model instance that it is saving to, rather than creating a new `UserProfile` instance each time. Remember, we are *updating*, not creating *new*. A valid form is then saved. An invalid form or a HTTP `GET` request triggers the rendering of the `profile.html` template with the relevant variables that are passed through to the template via its context.

X> ### Authentication Exercise
X> How can we change the code above to prevent unauthorised users from changing the details of a user account that isn't theirs? What conditional statement do we need to add to enforce this additional check?

### Mapping the View to a URL
We then need to map our new `ProfileView` to a URL. First import the class, `from rango.views import ProfileView`, and then add in the path within the `urlpatterns` list.

{lang="python",linenos=off}
	path('profile/<username>/', ProfileView.as_view(), name='profile')

Note the inclusion of a `username` variable which is matched to anything after `/profile/` - meaning that the URL `/rango/profile/maxwelld90/` would yield a `username` of `maxwelld90`, which is in turn passed to the `profile()` view as parameter `username`. This is how we are able to determine what user the current user has selected to view.

### Tweaking the Base Template
Everything should now be working as expected - but it'd be nice to add a link in Rango's `base.html` template to link the currently logged in user to their profile, providing them with the ability to view or edit it. In Rango's `base.html` template, find the code that lists a series of links in the navigation bar of the page when the *user is logged in*. Add the following hyperlink to this collection.

{lang="html",linenos=off}
    <li class="nav-item ">
    <a class="nav-link" href="{% url 'rango:profile' user.username %}">Profile</a>
    </li>


{id="fig-exercises-profile"}
![Rango's complete user profile page.](images/exercises-profile.png)

## Listing all Users
Our final challenge is to create another page that allows one to view a list of all users on the Rango app. This one is relatively straightforward - we need to implement another template, view and URL mapping - but the view in this instance is very simplistic. We'll be creating a list of users registered to Rango - and providing a hyperlink to view their profile using the code we implemented in the previous section.

### Creating a Template for User Profiles
In Rango's templates directory, create a template called `list_profiles.html`, within the file, add the following HTML markup and Django template code.

{lang="html",linenos=off}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	{% block title %}User Profiles{% endblock %}
	{% block body_block %}
	<div class="jumbotron p-4">
		<div class="container">
	 	<h1 class="jumbotron-heading">User Profiles</h1>
        </div>
    </div>
    <div class="container">
    	<div class="row">
	    {% if userprofile_list %}
	    <div class="panel-heading">
	        <!-- Display search results in an ordered list -->
	        <div class="panel-body">
	            <div class="list-group">
	            {% for listuser in userprofile_list %}
	                <div class="list-group-item">
	                <h4 class="list-group-item-heading">
	                <a href="{% url 'rango:profile' listuser.user.username %}">
	                {{ listuser.user.username }}</a>
	                </h4>
	                </div>
	            {% endfor %}
	            </div>
	        </div>
	    </div>
	    {% else %}
	        <p>There are no users for the site.</p>
	    {% endif %}
	</div>
    </div>
	{% endblock %}

This template is relatively straightforward - we created a series of `<div>` tags using various Bootstrap classes to style the list. For each user, we display their username and provide a link to their profile page. Notice since we pass through a list of `UserProfile` objects, to access the username of the user, we need to go view the `user` property of the `UserProfile` object to get `username`.

### Creating the View
With our template created, we can now create the corresponding view that selects all users from the `UserProfile` model. We also make the assumption that the current user must be logged in to view the other users of Rango. The following view `list_profiles()` can be added to Rango's `views.py` module to provide this functionality.

{lang="python",linenos=off}
	@login_required
	def list_profiles(request):
	    userprofile_list = UserProfile.objects.all()  
	    return render(request, 'rango/list_profiles.html',
	        {'userprofile_list' : userprofile_list})


### Mapping the View and Adding a Link
Our final step is to map a URL to the new `list_profiles()` view. Add the following to the `urlpatterns` list in Rango's `urls.py` module to do this.

{lang="python",linenos=off}
    path('profiles/', views.list_profiles, name='list_profiles'),

We could also add a new hyperlink to Rango's `base.html` template, allowing users *who are logged in* to view the new page. Like before, add the following markup to the base template which provides links only to logged in users.

{lang="html",linenos=off}
    <li class="nav-item ">
    <a class="nav-link" href="{% url 'rango:list_profiles' %}">List Profiles</a>
    </li>

With this link added you should be able to view the list of user profiles, and view specific profiles. 

X> ### Profile Page Exercise
X>
X> - Update the profile list to include a thumbnail of the user's profile picture.
X> - If a user does not have a profile picture, then insert a substitute picture by using the [service provide by LoremPixel](ttp://lorempixel.com/) that lets you automatically generate images.
X> Hint: you can use
X> [`<img width="64" height="64" src="http://lorempixel.com/64/64/people/"/>`](http://lorempixel.com/64/64/people/) 
X>  from LoremPixel to get a picture of `people` that is 64x64 in size. Note that it might take a few seconds for the picture to download.



