# Making Rango Tango Hints {#chapter-hints}
Hopefully, you will have been able to complete the exercises in the previous chapter using only the workflows we provided. If not, or if you need a little push in the right direction, this chapter is for you. We provide model solutions to each of the exercises we set, and you can incorporate them within your version of Rango if needs be.

I> ### Got a better solution?
I> The solutions provided in this chapter are only one way to solve each problem. There are many ways you could approach each problem, and use solutions that exclusively use techniques that we have learnt so far.
I> However, if you successfully implement them in a different way, please feel free to share your solution(s) with us -- and tweet links to [@tangowithdjango](https://www.twitter.com/tangowithdjango) for others to see!

## Track Page Clickthroughs
As we said when we introduced [this problem earlier](#chapter-ex-clickthroughs), Rango provides only a direct link to the pages of external pages saved to each category. This approach limits our ability to track (or simply count) the number of times a particular link is clicked. In order to be able to track clicks, we'll need to work on the following steps. The subsections we provide here correspond to the four main steps we [outlined earlier](#chapter-ex-clickthroughs) in our workflow.

### Creating a URL Tracking View
First, create a new view called `goto_url()` in Rango's `views.py` module. The view which takes a parameterised HTTP `GET` request (i.e. `rango/goto/?page_id=1`) and updates the number of views for the page. The view should then redirect to the actual URL.

{lang="python",linenos=off}
	def goto_url(request):
	    if request.method == 'GET':
	        page_id = request.GET.get('page_id')
	        
	        try:
	            selected_page = Page.objects.get(id=page_id)
	        except Page.DoesNotExist:
	            return redirect(reverse('rango:index'))
	        
	        selected_page.views = selected_page.views + 1
	        selected_page.save()
	        
	        return redirect(selected_page.url)
	    
	    return redirect(reverse('rango:index'))

Be sure that you import the `redirect()` function to `views.py` if it isn't included already! As the function defined above also makes use of `reverse()` to perform URL lookups, you'll want to make sure that is included, too -- it should be present from prior efforts, however.

{lang="python",linenos=off}
	from django.shortcuts import redirect
	from django.urls import reverse

### Mapping the View to a URL
The second major step involves mapping the new `goto_url()` view to the URL `/rango/goto/`. To do this, update Rango's `urls.py` module. Add the following code to the `urlpatterns` list.

{lang="python",linenos=off}
	path('goto/', views.goto_url, name='goto'),

Note that we are complying with specification in the previous chapter and using a mapping `name` of `goto`.

### Updating the `category.html` Template
The third step involves updating the `category.html` template. We were tasked to implement two changes, the first of which changed page links to use the new `goto_view()` view, rather than providing a direct URL link. Secondly, we were tasked to report back to users how many clicks each page had received.

Find the block of code that handles looping through the `pages` context variable. Update it accordingly.

{lang="python",linenos=off}
	{% for page in pages %}
	     <li>
	        <a href="{% url 'rango:goto' %}?page_id={{ page.id }}">{{ page.title }}</a>
	        {% if page.views > 1 %}
	            ({{ page.views }} views)
	        {% elif page.views == 1 %}
	            ({{ page.views }} view)
	        {% endif %}
	    </li>
	{% endfor %}

Notice the change to the URL's `href` attribute, and the inclusion of some new template code to control what is displayed immediately after the hyperlink -- a count on the number of views for the given page. As we also check how many clicks each page has received (one or more clicks?), we can also control our grammar, too!

### Updating Category View
The fourth and final step for this particular exercise was to update the `show_category()` view to reflect the change in the way we present our list of pages for each category. The specification now requires us to order the pages for each category by the number of clicks each page has received. This has to be descending, meaning the page with the largest number of clicks will appear first.

This involves the simple addition of chaining on an `order_by()` call to our ORM request. Find the line dealing with the `Page` model in `show_category()` and update it to look like the line shown below.

{lang="python",linenos=off}
	pages = Page.objects.filter(category=category).order_by('-views')

Now that this is all done, confirm it all works by clicking on categories and then pages. Go back to the category and refresh the page to see if the number of clicks has increased. Remember to refresh; the updated count may not show up straight away!

## Searching Within a Category Page
The main aim of Rango is to provide users of the app with a helpful directory of page links. At the moment, the search functionality is essentially independent of the categories. It would be better to integrate the search functionality within a category page.

Let us assume that a user will first navigate to and browse their category of interest first. If they cannot find the page that they want, they will then be able to search for it. Once they examine their search results and find the page they are looking for, they will be able to add the page to the category they are browsing.

We'll tackle the first part of the description here -- adding search functionality to the category page. In order to accomplish this, we first need to remove the [search functionality that we added in a previous chapter](#chapter-bing). This will essentially mean decommissioning the current search page and associated infrastructure (including the view and URL mapping). After this, there are several tasks we will need to undertake. The subsections listed here again correspond to the five main steps we outlined in the [previous chapter](#chapter-ex-searching).

W> ### Don't Delete your Code!
W> When decommissioning your existing search functionality, don't delete it. Simply comment things out where appropriate (such as in the `urls.py` module). You'll copying some of the code across to a new home later on, anyway.

### Decommissioning Generic Search
The first step for this exercise is to decommission the existing search functionality that you implemented in a [previous chapter](#chapter-bing).

1. First, open Rango's `base.html` template and find the navigation bar markup (found at the top of the page). Locate the `<li>` element for the `Search` link that you added earlier on and delete it. This needs to be deleted as you'll be commenting out the URL mapping shortly, meaning that a reverse URL lookup for `rango:search` will no longer work. Wrapping this with an HTML comment tag (`<!-- ... -->`) won't work either, as the Django template engine will still process what's inside of it!
2. Second, open Rango's `urls.py` module and locate the URL mapping for the `/rango/search/` URL. Comment this line out by adding a `#` to the start of the line. This will prevent users from reaching the `search` URL.
3. Finally, open Rango's `views.py` module and locate the `search()` view you implemented previously. Again, comment out this function by prepending a `#` to the start of each line.

You'll still have the `search.html` template in Rango's templates directory; don't remove this as we will be using the contents of this template as the basis for integrating search functionality within the category template.

### Migrating `search.html` to `category.html`
As we will be wanting provide search functionality to users who are browsing a category, we need to add in the search presentation functionality (e.g. displaying the search form and results area) to the `category.html` template. This is essentially a simple copy and paste job!

Let's split this into two main steps. First, open your decommissioned `search.html` template and locate the `<div>` element containing the entire search form. This will be the `<div>` whose child is a `<form>` element. Select and copy the `<div>` and its contents, then open Rango's `category.html` file.

We now need to paste the code from `search.html` into `category.html`. As the brief for this problem was to add the search functionality *underneath* the list of pages in the category, find and locate the link inside the `{% block body_block %}` to add a page. Paste the contents from `search.html` underneath that link.

You can then go back to `search.html` and repeat the process, this time selecting the `<div>` for displaying the results list. You can identify this by looking for the `<div>` with Django template code that iterates through the `result_list` list. Copy that and then move back over to `category.html`. Now paste that in underneath the `<div>` containing the form that you previously pasted in.

### Updating the `category.html` Search Form
Now that the markup required has been added to `category.html`, we need to make one simple change. Instead of submitting the contents of the search form to the `/rango/search/` URL which we decommissioned earlier, we instead will simply direct submitted responses to the Rango `/rango/category/<slug:category_name_slug>` URL instead. This is as simple as finding the `<form>` definition in `category.html` and changing the `action` attribute to Rango's `show_category()` URL mapping.

{lang="html",linenos=off}
	<form class="form-inline"
	      id="user-form"
	      method="post"
	      action="{% url 'rango:show_category' category.slug %}">

### Updating the `show_category()` View
You should have identified that since we are now redirecting search requests to the `show_category()` view, we'll need to make some changes within that view so that it can handle the processing of the search request, as well as being able to handle the generation of a list of pages for a given category.

This is again a relatively straightforward process in which we update the view based upon code from our decommissioned `search()` view. We provide the complete listing of our model `show_category()` view below. Notice the comments denoting the start of the code we have taken from our existing `search()` view.

{lang="python",linenos=on}
	def show_category(request, category_name_slug):
	    context_dict = {}
	    
	    try:
	        category = Category.objects.get(slug=category_name_slug)
	        pages = Page.objects.filter(category=category).order_by('-views')
	        
	        context_dict['pages'] = pages
	        context_dict['category'] = category
	    except Category.DoesNotExist:
	        context_dict['category'] = None
	        context_dict['pages'] = None
	    
	    # Start new search functionality code.
	    if request.method == 'POST':
	        if request.method == 'POST':
	            query = request.POST['query'].strip()
	            
	            if query:
	                context_dict['result_list'] = run_query(query)
	    # End new search functionality code.
	    
	    return render(request, 'rango/category.html', context_dict)

We keep the `show_category()` view the same at the top, and add in an additional block of code towards the end to handle the processing of a search request. If a `POST` request is made, we then attempt to take the `query` from the request and issue the query to the `run_query()` function we defined in the [Bing Search chapter](#sec-bing-pyfunc). This then returns a list of results which we put into the `context_dict` with a key of `result_list` -- exactly the variable name that is expected in the updated `category.html` template.

Search functionality should then all work as expected. Try it out! Navigate to a category page, and you should see a search box. Enter a search query, submit it, and see what happens.

### Restricting Access to Search Functionality
Our final requirement was to restrict the migrated search functionality only to those who are logged into Rango. This step is straightforward -- one can simply wrap the search-handling template code added to `category.html` with a conditional template check to determine if the user is authenticated.

{lang="python",linenos=off}
	{% if user.is_authenticated %}
	<div>
	    ....
	</div>
	{% endif %}

Too easy! You could also go further and add conditional checks within the `show_category()` view to ensure the search functionality part is not executed when the current use is not logged in. Be wary, though -- don't be inclined to add the `login_required()` decorator to the view. Doing so will restrict all category-viewing functionality to logged in users only -- you only want to restrict the *search* functionality!

### Query Box Exercise
At the end of the Bing Search API chapter, we set an exercise. We noted that in its current state, users would issue a query and then be presented with the results. However, the query box would then be blanked again -- thus making *query reformulation* more taxing.

In our code examples above, we've deliberately kept our model solution to this particular exercise out. How could you allow the results page to *'remember'* the query that was entered, and place it back in the search box?

The solution to this problem is to simply place the `query` variable into the `context_dict` of `show_category()`, and then make use of the variable within the `category.html` template by specifying its value as the `value` attribute for the search box `<input>` element.

In Rango's `show_category()` view, locate the coe block that deals with the search functionality, and add the `query` to the `context_dict`, like so.

{lang="python",linenos=off}
	# Start new search functionality code.
	if request.method == 'POST':
	    if request.method == 'POST':
	        query = request.POST['query'].strip()
	        
	        if query:
	            context_dict['result_list'] = run_query(query)
	            context_dict['query] = query
	# End new search functionality code.

Once this has been completed, open Rango's `category.html` template and modify the `query` `<input>` field like so.

{lang="html",linenos=off}
	<input class="form-control"
	       type="text"
	       size="50"
	       name="query"
	       value="{{ query }}"
	       id="query" />

Template variable `{{ query }}` will be replaced with the user's query, thus setting it to be the default value for the `<input>` field when the page loads.

Once everything has been completed, you should have a category page that looks similar to the example below. Well done!

{id="fig-exercises-categories"}
![Rango's updated category view, complete with Bing Search API search functionality. Note also the inclusion of the search terms in the query box -- they are still retained!](images/exercises-categories.png)

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



