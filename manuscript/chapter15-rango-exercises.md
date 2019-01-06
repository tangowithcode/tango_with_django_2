#Making Rango Tango! Exercises {#chapter-ex} 
So far we have been adding in different pieces of functionality to Rango. We've been building up the application in this manner to get you familiar with the Django Framework, and to learn about how to construct the various parts of an application. However, at the moment, Rango is not very cohesive or interactive. In this chapter, we challenge you to improve the application and its user experience by bringing together some of the functionality that we have already implemented along with some other features.

To make Rango more coherent, integrated and interactive, it would be nice to add the following functionality.

- Track the clicks on Categories and Pages, i.e.:
	- count the number of times a category is viewed
	- count the number of times a page is viewed via Rango, and
	- collect likes for categories (see [Django and Ajax Chapter](#chapter-ajax)).
- Integrate the browsing and searching within categories, i.e.:
	- instead of having a disconnected search page, let users search for pages on each specific category page, and
	- let users filter the set of categories shown in the side bar (see [Django and Ajax Chapter](#chapter-ajax)).
- Provide services for Registered Users, i.e.:
	- Assuming you have switched the `django-registration-redux`, we need to setup the registration form to collect the additional information (i.e. website, profile picture)
	- let users view their profile
	- let users edit their profile, and
	- let users see the list of users and their profiles.

I> ### Note
I> We won't be working through all of these tasks right now. Some will be taken care of in the [Django and Ajax Chapter]({#chapter-ajax}), while others will be left to you to complete as additional exercises.

Before we start to add this additional functionality we will make a todo list to plan our workflow for each task. Breaking tasks down into sub-tasks will greatly simplify the implementation so that we are attacking each one with a clear plan. In this chapter, we will provide you with the workflow for a number of the above tasks. From what you have learnt so far, you should be able to fill in the gaps and implement most of it on your own (except those requiring AJAX). In the following chapter, we have included hints, tips and code snippets elaborating on how to implement these features. Of course, if you get really stuck, you can always check out our implementation on GitHub.

## Track Page Clicks
Currently, Rango provides a direct link to external pages. This is not very good, because we wont know which pages people visit. So to count the number of times a page is viewed via Rango you will need to perform the following steps.

- Create a new view called `goto_url()`, and map it to URL `/rango/goto/` and name it `'name=goto'`.
- The `goto_url()` view will examine the HTTP `GET` request parameters and pull out the `page_id`. The HTTP `GET` requests will look something like `/rango/goto/?page_id=1`.
	- In the view, select/get the `page` with `page_id` and then increment the associated `views` field, and `save()` it.
	- Have the view redirect the user to the specified URL using Django's `redirect` method. Remember to include the import, `from django.shortcuts import redirect`
	- If no parameters are in the HTTP `GET` request for `page_id`, or the parameters do not return a `Page` object, redirect the user to Rango's homepage. Use the `reverse` method to get the URL string and then redirect. 
	- See [Django Shortcut Functions](https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/) for more on `redirect` and    
    [Django Reverse Function](ttps://docs.djangoproject.com/en/2.1/ref/urlresolvers/#django.urls.reverse) for more on `reverse`.
- Update the `category.html` so that it uses `/rango/goto/?page_id=XXX`.
	- Remember to use the `url` template tag instead of using the direct URL i.e. 
	
	{lang="python",linenos=off}
		<a href="{% url 'rango:goto' %}?page_id={{page.id}}"\>


I> ### `GET` Parameters Hint
I>
I> If you're unsure of how to retrieve the `page_id` *querystring* from the HTTP `GET` request, the following code sample should help you.
I>
I> {lang="python",linenos=off}
I> 		page_id = None
I> 		if request.method == 'GET':
I> 		    if 'page_id' in request.GET:
I> 		        page_id = request.GET['page_id']
I>
I> Always check the request method is of type `GET` first, then you can access the dictionary `request.GET` which contains values passed as part of the request. If `page_id` exists within the dictionary, you can pull the required value out with `request.GET['page_id']`.
I>
I> You could also do this without using a *querystring*, but through the URL instead, i.e. `/rango/goto/<page_id>/`. In which case you would need to create a `urlpattern` that pulls out the `page_id`, i.e. `'goto/<int:page_id>/'`.


## Searching Within a Category Page
Rango aims to provide users with a helpful directory of useful web pages. At the moment, the search functionality is essentially independent of the categories. It would be nicer to have search integrated within the categories. We will assume that a user will first browse through the category of interest. If they can't find a relevant page, they can then search. If they find a page that is relevant, then they can add it to the category. Let's focus on the first problem, of putting search on the category page. To do this, perform the following steps:

- Remove the generic *Search* link from the menu bar, i.e. we are decommissioning the global search functionality.
- Take the search form and results template markup from `search.html` and place it into `category.html`.
- Update the search form so that action refers back to the category page, i.e.:

{lang="html",linenos=off}
	<form class="form-inline" id="user_form" 
	    method="post" action="{% url 'rango:show_category'  category.slug %}">

- Update the category view to handle a HTTP `POST` request. The view must then include any search results in the context dictionary for the template to render.
- Also, lets make it so that only authenticated users can search. So to restrict access within the `category.html` template use:

{lang="python",linenos=off}
	{% if user.authenticated %} 
	    <!-- Insert search code here -->
	{% endif %}

## Create and View Profiles
If you have swapped over to the `django-registration-redux` package, then you'll have to collect the `UserProfile` data. To do this, instead of redirecting the user to the Rango index page, you will need to redirect them to a new form, to collect the user's profile picture and URL details. To add the UserProfile registration functionality, you need to:

- create a `profile_registration.html` which will display the `UserProfileForm`;
- create a `UserProfileForm` `ModelForm` class to handle the new form;
- create a `register_profile()` view to capture the profile details;
- map the view to a URL, i.e. `rango/register_profile/`; and
- in the `MyRegistrationView`, update the `get_success_url()` to point to `rango/add_profile/`.

Another useful feature is to let users inspect and edit their own profile. Undertake the following steps to add this functionality.

- First, create a template called `profile.html`. In this template, add in the fields associated with the user profile and the user (i.e. username, email, website and picture).
- Create a view called `profile()`. This view will obtain the data required to render the user profile template.
- Map the URL `/rango/profile/` to your new `profile()` view.
- In the base template add a link called *Profile* into the menu bar, preferably with other user-related links. This should only be available to users who are logged in (i.e. `{% if user.is_authenticated %}`).

To let users browse through user profiles, you can also create a users page that lists all the users. If you click on a user page, then you can see their profile. However, you must make sure that a user is only able to edit their profile!

T> ### Referencing Uploaded Content in Templates
T>
T> If you have successfully completed all of the [Templates and Media chapter](#section-templates-upload), your Django setup should be ready to deal with the uploading and serving of user media files. You should be able to reference the `MEDIA_URL` URL (defined in `settings.py`) in your templates through use of the `{{ MEDIA_URL }}` tag, provided by the [media template context processor](https://docs.djangoproject.com/en/2.1/howto/static-files/), e.g. `<img src="{{ MEDIA_URL}}cat.jpg">`.

In the next chapter, we provide a series of hints and tips to help you complete these features.